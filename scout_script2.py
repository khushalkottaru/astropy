import json

with open("filtered_issues2.json") as f:
    issues = json.load(f)

for issue in issues:
    print(f"Issue #{issue['number']}: {issue['title']} (Opened: {issue['created_at']}, Assignee: {issue['assignee']})")
