import json

with open("filtered_issues.json") as f:
    issues = json.load(f)

for issue in issues:
    print(f"Issue #{issue['number']}: {issue['title']}")
