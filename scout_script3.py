import json

try:
    with open("filtered_issues_all.json") as f:
        issues = json.load(f)

    if issues:
        for issue in issues:
            print(f"Issue #{issue['number']}: {issue['title']} (Opened: {issue['created_at']}, Assignee: {issue['assignee']})")
    else:
        print("No issues found in page 2 and 3")
except Exception as e:
    print(e)
