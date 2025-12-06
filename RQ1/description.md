We want to investigate the frequency in which AI agents contribute tests to their respective projects and repo’s. Considering that AI agents pose a risk of contributing code that contains errors, it is important for some form of a safeguard or error check to take place on their code. We would like to explore the rate at which AI agents contribute tests in relation to changes made to the codebase. You can call this the test-to-code churn ratio. If we have extra time, then more details will be explored, such as the metrics for the different types of tests (unit, integration etc.) contributed.   
  
**Methodologies:**
	We will use pandas to explore the various tables in the dataset. Firstly, the PR’s that include tests need to be located. Such pull requests can be located by querying for matching keywords (like ‘test’, ‘unit-test’ etc.) in the columns ‘title’ and/or ‘body’ in the pull_request table, or for similar keywords in the ‘message’ column of the pr_commits table (with possibility of many commits per single PR). The total records of testing PR’s can be compared to the total number of PRs to obtain metrics on frequency (test to code churn ratio). Individual metrics for individual repos or individual AI Agent ‘users’ may also be calculated for further analysis (by isolating on user ID and/or repo ID). If time permits, then we may go further to compare record counts for PR’s that match specific test types by their keywords in the commit or PR descriptions. Pie charts and graphs will be constructed in python to help visualize and compare these various metrics and form our conclusions.


To investigate the rate at which AI agents contribute tests to their repositories, we analyze pull requests (PRs) and commit-level data in the AIDev dataset. Our goal is to determine how often test-related changes appear relative to overall code churn, and to quantify differences across repositories.

1. Data Loading

We use three primary tables from the AIDev dataset:
1.1 pull_request.parquet – contains PR-level metadata such as titles, bodies, authors, and repository IDs.
1.2 pr_commits.parquet – contains commit messages linked to each PR.
1.3 pr_commit_details.parquet – includes additions and deletions per commit, enabling calculation of code churn.

All tables are loaded into pandas DataFrames and merged on the pr_id field when necessary.

2. Identifying Test-Related Pull Requests

We classify a PR as “test-related” if any part of the PR contains test-associated keywords.
We define a regular expression that matches commonly used test terms:
“test”,

“unit-test”,

“pytest”,

“testing”,

“integration-test”, etc.

A helper function applies this regex to text fields after converting to lowercase.

Detection Across Multiple Sources
We check for test-related keywords in three locations:

2.1  PR title – Indicates intentional test addition or modification.
2.2 PR body – Often describes changes including test procedures.
2.3 Commit messages – Important because a PR may contain many commits with test-related changes even if the title/body does not mention them.

For commit-level matches, we aggregate by PR (groupby(pr_id).any()) to determine whether any commit in a PR references tests.

Finally, we combine the signals:

is_test_pr = has_test_in_title V has_test_in_body V has_test_commit

A PR is considered test-related if any of these fields are true.

3. Computing Code Churn

To contextualize test contributions relative to code changes, we compute code churn for each PR.

For every commit, churn is:

churn = additions + deletions

We sum churn values across all commits in a PR to produce a PR-level total_churn metric.
Missing values (e.g., PRs without matching commit details) are treated as zero.

4. Calculating the Test-to-Code Contribution Ratio

We calculate both global and repository-level metrics:

Overall ratio

Test-to-Code Ratio = # test PRs / # total PRs​

This ratio measures how frequently AI agents submit PRs that appear to involve tests.

Repository-level analysis

For each repository (repo_id), we compute:
4.1 total number of PRs
4.2 number of test-related PRs
4.3 average code churn
4.4 repository-specific test ratio

Repo Test Ratio = test_pr / total_pr
	​
This highlights differences between projects, including repos where test generation is unusually high or extremely rare.

5. Visualization

We create two primary visualizations:

5.1 Bar chart comparing the number of test PRs vs non-test PRs.
Quickly illustrates how uncommon test contributions are.

5.2 Histogram showing the distribution of test ratios across repositories.
Reveals whether testing behavior is consistent or highly skewed across projects.

These plots support interpretation of testing frequency and help identify repositories that deviate significantly from typical behavior.

6. Interpretation

The resulting metrics allow us to evaluate how often AI agents include tests relative to their overall code contributions. A low test ratio indicates:

6.1 limited test writing by AI agents

6.2 potential risk of missing safeguards

6.3 a need for stronger review requirements or automated test generation tools

Repository-level variation further reveals how project structure or maintainers’ guidelines influence agents’ testing behavior.
