import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from huggingface_hub import hf_hub_download

# Setting
pd.set_option("display.max_columns", 50)
sns.set(style="whitegrid")


# 1. Load AIDev-pop data

def load_aidev_pop():
    repo_id = "hao-li/AIDev"

    # Using hf:// scheme with pyarrow/fsspec support
    pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pull_request.parquet")
    issue_df = pd.read_parquet("hf://datasets/hao-li/AIDev/issue.parquet")
    rel_df = pd.read_parquet("hf://datasets/hao-li/AIDev/related_issue.parquet")
    commit_details_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commit_details.parquet")

    print("pull_request shape:", pr_df.shape)
    print("issue shape:", issue_df.shape)
    print("related_issue shape:", rel_df.shape)
    print("pr_commit_details shape:", commit_details_df.shape)

    return pr_df, issue_df, rel_df, commit_details_df


# 2. Build time-based efficiency metrics

def build_time_features(pr_df, issue_df, rel_df):

    # Convert time columns to datetime
    for col in ["created_at", "closed_at", "merged_at"]:
        if col in pr_df.columns:
            pr_df[col] = pd.to_datetime(pr_df[col], errors="coerce")
    if "created_at" in issue_df.columns:
        issue_df["created_at"] = pd.to_datetime(issue_df["created_at"], errors="coerce")

    # Keep only closed PRs
    closed_pr = pr_df[pr_df["state"] == "closed"].copy()

    # Keep only Agentic-PRs (agent is not null)
    agent_pr = closed_pr[closed_pr["agent"].notna()].copy()

    # Join related_issue with issue to get issue creation time
    # Assumes related_issue has columns: issue_id, pr_id
    # and issue has: id, created_at
    rel_issue = rel_df.merge(
        issue_df[["id", "created_at"]],
        left_on="issue_id",
        right_on="id",
        how="left",
        suffixes=("", "_issue")
    )

    rel_issue.rename(columns={"created_at": "issue_created_at"}, inplace=True)
    rel_issue = rel_issue[["pr_id", "issue_created_at"]]

    # Attach issue creation time to PR
    agent_pr = agent_pr.merge(rel_issue, left_on="id", right_on="pr_id", how="inner")

    # Compute time differences in days
    agent_pr["issue_to_pr_create_days"] = (
        agent_pr["created_at"] - agent_pr["issue_created_at"]
    ).dt.total_seconds() / 86400.0

    agent_pr["issue_to_pr_close_days"] = (
        agent_pr["closed_at"] - agent_pr["issue_created_at"]
    ).dt.total_seconds() / 86400.0

    # Only defined when merged_at is not null
    agent_pr["issue_to_pr_merge_days"] = np.where(
        agent_pr["merged_at"].notna(),
        (agent_pr["merged_at"] - agent_pr["issue_created_at"]).dt.total_seconds() / 86400.0,
        np.nan,
    )

    return agent_pr


# 3. Build change-based metrics (additions / deletions / changes)

def build_change_features(agent_pr_df, commit_details_df):
    commit = commit_details_df.copy()
    # Ensure numeric columns for additions/deletions
    for col in ["additions", "deletions"]:
        if col in commit.columns:
            commit[col] = commit[col].fillna(0).astype(float)
        else:
            raise KeyError(
                f"Column '{col}' does not exist in pr_commit_details. "
                f"Actual columns: {list(commit.columns)}"
            )

    commit["file_changes"] = commit["additions"] + commit["deletions"]

    pr_change = commit.groupby("pr_id").agg(
        total_additions=("additions", "sum"),
        total_deletions=("deletions", "sum"),
        total_changes=("file_changes", "sum"),
    ).reset_index()

    merged = agent_pr_df.merge(pr_change, left_on="id", right_on="pr_id", how="left")
    merged[["total_additions", "total_deletions", "total_changes"]] = (
        merged[["total_additions", "total_deletions", "total_changes"]].fillna(0.0)
    )

    return merged


# 4. Descriptive statistics and visualizations
def descriptive_stats(df):
    print("\n=== Descriptive statistics for time-based metrics (days) ===")
    print(
        df[
            [
                "issue_to_pr_create_days",
                "issue_to_pr_close_days",
                "issue_to_pr_merge_days",
            ]
        ].describe()
    )

    print("\n=== Descriptive statistics for code change metrics (lines) ===")
    print(
        df[["total_additions", "total_deletions", "total_changes"]].describe()
    )


def plot_distributions(df):
    # Histogram for issue → PR close time
    plt.figure(figsize=(7, 4))
    sns.histplot(df["issue_to_pr_close_days"].dropna(), bins=40)
    plt.title("Distribution of Issue → PR Close Time (days)")
    plt.xlabel("Days from issue created to PR closed")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    # Boxplot of total code changes
    plt.figure(figsize=(6, 4))
    sns.boxplot(y=df["total_changes"])
    plt.title("Total Code Changes per Agentic-PR")
    plt.ylabel("Lines added + deleted")
    plt.tight_layout()
    plt.show()

    # Histogram for issue → PR merge time (only where merge time exists)
    merged_only = df[df["issue_to_pr_merge_days"].notna()]
    if not merged_only.empty:
        plt.figure(figsize=(7, 4))
        sns.histplot(merged_only["issue_to_pr_merge_days"], bins=40)
        plt.title("Distribution of Issue → PR Merge Time (days)")
        plt.xlabel("Days from issue created to PR merged")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()


# 5. logistic regression on merge decision

def main():
    # 1. Load AIDev-pop data
    pr_df, issue_df, rel_df, commit_details_df = load_aidev_pop()

    # 2. Build time-based features (task completion duration)
    agent_pr_time = build_time_features(pr_df, issue_df, rel_df)

    # 3. Build code-change features (additions / deletions / changes)
    agent_pr_full = build_change_features(agent_pr_time, commit_details_df)

    # 4. Descriptive statistics
    descriptive_stats(agent_pr_full)

    # 5. Visualization
    plot_distributions(agent_pr_full)

if __name__ == "__main__":
    main()
