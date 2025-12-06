# DATA542-Project
## Group 4
## Members:
## Andre Gnandt 59616136
## Bingzheng Jin 66900523  
  
## Execution Instructions:  
### RQ2  
All of the RQ2 code is located in the RQ2 directory. To execute this code and obtain results, simply run the jupyter notebook RQ2.jpynb (all cells) located in the RQ2 directory.  
  
### RQ3  
All of the RQ3 code is located in the RQ3 directory. To execute this code and obtain results, simply run the python file RQ3.py in the RQ3 directory.  
  
## Project Overview  
### Research Question 1: 
We want to investigate the frequency in which AI agents contribute tests to their respective projects and repo’s. Considering that AI agents pose a risk of contributing code that contains errors, it is important for some form of a safeguard or error check to take place on their code. We would like to explore the rate at which AI agents contribute tests in relation to changes made to the codebase. You can call this the test-to-code churn ratio. If we have extra time, then more details will be explored, such as the metrics for the different types of tests (unit, integration etc.) contributed. 
  
**Methodologies:**  
We will use pandas to explore the various tables in the dataset. Firstly, the PR’s that include tests need to be located. Such pull requests can be located by querying for matching keywords (like ‘test’, ‘unit-test’ etc.) in the columns ‘title’ and/or ‘body’ in the pull_request table, or for similar keywords in the ‘message’ column of the pr_commits table (with possibility of many commits per single PR). The total records of testing PR’s can be compared to the total number of PRs to obtain metrics on frequency (test to code churn ratio). Individual metrics for individual repos or individual AI Agent ‘users’ may also be calculated for further analysis (by isolating on user ID and/or repo ID). If time permits, then we may go further to compare record counts for PR’s that match specific test types by their keywords in the commit or PR descriptions. Pie charts and graphs will be constructed in python to help visualize and compare these various metrics and form our conclusions.
  
### Research Question 2:  
We want to investigate how often code errors or code quality issues appear in the AI agents pull requests. More specifically, we want to explore what kind of errors or issues are most common amongst the AI agents. If we have extra time, we will explore the possible reasons as to why such code issues occur frequently in AI agents.  
  
**Methodologies:**  
There are several methods that can be used to retrieve problematic PRs and the details surrounding them. Such PRs can be retrieved by querying the pr_review and pr_review_comments tables for records with ‘body’ content that resemble keywords or text related to code issues, and with a ‘CHANGES_REQUESTED’ state. Similarly, the pr_comments table can be examined in an identical way to find more code issues. This is amongst some of the techniques that will be used to obtain the data that relates to agent code issues, we can compare the count of these issues to the total PR records to determine the rate and frequency at which code issues are made. From the body content of these records, we can extract the issues into certain categories based on keywords and obtain metrics for the most common issues. Pie charts and graphs will be constructed in python to help visualize and compare these various metrics and form our conclusions.  
  
### Research Question 3:  
We want to explore the rate at which AI agents produce code contributions. It would be interesting to examine just how efficient at producing correct and reliable code these agents are, and the overall time it takes for an agent to complete its task and for its PR to be approved.  
  
**Methodologies:**  
Several techniques will be used to examine the efficiency of AI agents. Some of these will include comparing the ‘issue’ tables created_at date to its linked PR’s created_at, closed_at and merged_at dates. From these timestamp values we can determine the amount of time it takes for the agent to create, fix and finish the coding tasks. We can obtain averages for all such comparison values in the dataset to estimate the efficiency of Ai agents at completing tasks. To go in more detail and if we have extra time, we may consider including the values for ‘additions’, ‘deletions’ and ‘changes’ in the pr_commit_details table within these measurements, to get an estimate of how many lines of code or how many ‘changes’ the agents can make in a certain amount of time. Pie charts and graphs will be constructed in python to help visualize and compare these various metrics and form our conclusions.
