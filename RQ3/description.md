We want to explore the rate at which AI agents produce code contributions. It would be interesting to examine just how efficient at producing correct and reliable code these agents are, and the overall time it takes for an agent to complete its task and for its PR to be approved.  
  
**Methodologies:**  
  Several techniques will be used to examine the efficiency of AI agents. Some of these will include comparing the ‘issue’ tables created_at date to its linked PR’s created_at, closed_at and merged_at dates. From these timestamp values we can determine the amount of time it takes for the agent to create, fix and finish the coding tasks. We can obtain averages for all such comparison values in the dataset to estimate the efficiency of Ai agents at completing tasks. To go in more detail and if time permits, we may consider including the values for ‘additions’, ‘deletions’ and ‘changes’ in the pr_commit_details table within these measurements, to get an estimate of how many lines of code or how many ‘changes’ the agents can make in a certain amount of time. Pie charts and graphs will be constructed in python to help visualize and compare these various metrics and form our conclusions.


To evaluate the efficiency of AI agents in producing code contributions, we will analyze several timing- and change-based indicators that describe how quickly and effectively agents complete software development tasks. Our primary focus is to measure (1) how long agents take to generate and finalize a coding task, and (2) how much code is produced or modified before the corresponding pull request (PR) is approved.

1. Measuring Task Completion Time

We estimate AI agent task duration by linking issue creation timestamps to their associated PR timestamps. Specifically, we compute:

Issue → PR creation time:
PR.created_at – Issue.created_at
Represents how long the agent takes to produce an initial solution after the task is issued.

Issue → PR closing time:
PR.closed_at – Issue.created_at
Indicates the total time required for the agent to complete and finalize the task.

Issue → PR merging time (if merged):
PR.merged_at – Issue.created_at
Measures the full lifecycle from problem creation to an accepted solution.

These values allow us to estimate the agent’s efficiency in producing and completing coding tasks across different repositories.

2. Measuring Code Change Volume

To further assess productivity and task complexity, we analyze file-level change information from the pr_commit_details table, using:

additions: total lines of code added

deletions: total lines of code removed

changes: sum of additions and deletions

These metrics provide insight into how substantial each agent-generated code contribution is, and how extensively an agent modifies the target codebase during its work.

3. Aggregation and Comparison

For each of the above measurements, we compute:

time durations for each PR

average and median times across all agent-generated PRs

distribution of additions, deletions, and total changes

These aggregated statistics allow us to understand general efficiency trends across many PRs rather than relying on single examples.

4. Visualization

To clearly compare and interpret the results, we will generate visualizations such as:

histograms of task duration

bar charts or boxplots of additions/deletions/total changes

pie charts summarizing PR outcomes (e.g., merged vs. closed)

These visuals help interpret how quickly agents respond to tasks, how much code they generate, and how often their contributions are accepted.
