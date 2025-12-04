import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


# Direct parquet load version:
pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pull_request.parquet")
commit_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commits.parquet")
pr_reviews = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_reviews.parquet")

# 1. Identify “test-related” PRs

TEST_KEYWORDS = r"(test|unit[-_ ]?test|pytest|testing|integration[-_ ]?test)"
def contains_test(text):
    if pd.isna(text):
        return False
    return bool(re.search(TEST_KEYWORDS, text.lower()))

# A: Match title/body
pr_df["has_test_in_title"] = pr_df["title"].apply(contains_test)
pr_df["has_test_in_body"] = pr_df["body"].apply(contains_test)

# B: Match in commit messages (many commits may belong to one PR)
commit_df["has_test_msg"] = commit_df["message"].apply(contains_test)

# Aggregate commit-level info
test_commits = (
    commit_df.groupby("pr_id")["has_test_msg"]
    .any()
    .rename("has_test_commit")
    .reset_index()
)

# Merge into PR table
pr_df = pr_df.merge(test_commits, left_on="id", right_on="pr_id", how="left")

pr_df["has_test_commit"] = (
    pr_df["has_test_commit"]
    .fillna(False)
    .astype(bool)
)

# Final flag: PR contains test contribution
pr_df["is_test_pr"] = (
    pr_df["has_test_in_title"] |
    pr_df["has_test_in_body"] |
    pr_df["has_test_commit"]
)

# 2. Compute test-to-code-churn ratio
# Code churn = additions + deletions (from commit details)
churn_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commit_details.parquet")
churn_df["code_churn"] = churn_df["additions"] + churn_df["deletions"]

churn_pr = (
    churn_df.groupby("pr_id")["code_churn"]
    .sum()
    .rename("total_churn")
    .reset_index()
)

pr_df = pr_df.merge(churn_pr, left_on="id", right_on="pr_id", how="left")
pr_df["total_churn"] = pr_df["total_churn"].fillna(0)

# Compute ratio
test_pr_count = pr_df["is_test_pr"].sum()
total_pr_count = len(pr_df)
test_ratio = test_pr_count / total_pr_count

# 3. Repo-level analysis (optional but recommended for Milestone)

repo_stats = (
    pr_df.groupby("repo_id")
    .agg(
        total_pr=("id", "count"),
        test_pr=("is_test_pr", "sum"),
        avg_churn=("total_churn", "mean")
    )
)
repo_stats["test_ratio"] = repo_stats["test_pr"] / repo_stats["total_pr"]
repo_stats = repo_stats.sort_values("test_ratio", ascending=False)

# 4. Visualization

plt.figure(figsize=(8, 4))
sns.barplot(x=["Test PRs", "Other PRs"], y=[test_pr_count, total_pr_count - test_pr_count])
plt.title("Distribution of Test vs Non-Test PRs")
plt.ylabel("Count")
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(repo_stats["test_ratio"], bins=20, kde=True)
plt.title("Distribution of Test-to-Code Contribution Ratio across Repos")
plt.xlabel("Test Ratio")
plt.ylabel("Repo Count")
plt.show()


# 5. Key summary output

print("RQ1 Summary")
print(f"Total PRs: {total_pr_count}")
print(f"Test-related PRs: {test_pr_count}")
print(f"Overall Test-to-Code Contribution Ratio: {test_ratio:.4f}")
print("\nTop 5 repos with highest test ratio:")
print(repo_stats.head())
