# merge_datasets.py
import pandas as pd
import os

# Paths
BASE_DIR = r"D:\grievance-analyzer\data"
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
OUTPUT_FILE = os.path.join(CLEANED_DIR, "merged_summary.csv")

# Load cleaned datasets
consumer_file = os.path.join(CLEANED_DIR, "cleaned_consumer_complaints.csv")
police_file = os.path.join(CLEANED_DIR, "cleaned_police_tweets.csv")
governance_file = os.path.join(CLEANED_DIR, "cleaned_governance.csv")

print("🔹 Loading cleaned datasets...")
consumer_df = pd.read_csv(consumer_file, parse_dates=["date_received"])
police_df = pd.read_csv(police_file, parse_dates=["tweet_date"])
governance_df = pd.read_csv(governance_file)

# -------------------------
# Aggregate consumer complaints
# -------------------------
if "state" in consumer_df.columns:
    consumer_df["state_ut"] = consumer_df["state"]
else:
    # If state column not present, skip state-based aggregation
    consumer_df["state_ut"] = "Unknown"

consumer_agg = (
    consumer_df.groupby(["state_ut", consumer_df["date_received"].dt.to_period("M")])
    .size()
    .reset_index(name="complaints_count")
)
consumer_agg["month_year"] = consumer_agg["date_received"].astype(str)
consumer_agg = consumer_agg.drop(columns=["date_received"])

# -------------------------
# Aggregate police tweets
# -------------------------
if "state_ut" in police_df.columns:
    police_df["state_ut"] = police_df["state_ut"].fillna("Unknown")
else:
    police_df["state_ut"] = "Unknown"

police_agg = (
    police_df.groupby(["state_ut", police_df["tweet_date"].dt.to_period("M")])
    .size()
    .reset_index(name="tweets_count")
)
police_agg["month_year"] = police_agg["tweet_date"].astype(str)
police_agg = police_agg.drop(columns=["tweet_date"])

# -------------------------
# Prepare governance dataset
# -------------------------
governance_df.columns = [c.lower().replace(" ", "_") for c in governance_df.columns]
if "state/ut" in governance_df.columns:
    governance_df = governance_df.rename(columns={"state/ut": "state_ut"})

# -------------------------
# Merge all datasets
# -------------------------
merged = pd.merge(consumer_agg, police_agg, on=["state_ut", "month_year"], how="outer")
merged = pd.merge(merged, governance_df, on="state_ut", how="left")

# Fill missing counts with 0
merged["complaints_count"] = merged["complaints_count"].fillna(0).astype(int)
merged["tweets_count"] = merged["tweets_count"].fillna(0).astype(int)

# Save merged summary
merged.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"✅ Merged summary saved at: {OUTPUT_FILE}")
print(merged.head())
