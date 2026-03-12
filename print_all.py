import json

with open("all_good_first_issues.json") as f:
    issues = json.load(f)

for issue in issues[:15]:
    print(f"Issue #{issue['number']}: {issue['title']} (Labels: {', '.join(issue['labels'])})")
