import json
import os

# Example structure: Replace with your logic to fetch JSONs per branch
branches = ['Development', 'QA', 'UAT', 'Production']
all_env_data = {}

# Fetch environment variables from each branch JSON
for branch in branches:
    try:
        with open(f"tmp_{branch}/appsettings.{branch}.json", "r") as f:
            data = json.load(f)
            env_vars = []
            for app in data.get("AppSettings", []):
                for s in app.get("Settings", []):
                    env_vars.append({
                        "variable": s.get("Name", "N/A"),
                        "value": s.get("Value", "N/A"),
                        "status": "Active" if s.get("Value") else "Missing"
                    })
            all_env_data[branch] = env_vars
    except FileNotFoundError:
        all_env_data[branch] = [{"variable": "N/A", "value": "N/A", "status": "Missing"}]

# HTML dashboard creation
html_content = """
<html>
<head>
<style>
body { font-family: Arial, sans-serif; background-color: #f7f7f7; }
h2 { color: #2E8B57; }
table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
th { background-color: #4CAF50; color: white; padding: 8px; text-align: left; }
td { border: 1px solid #ddd; padding: 8px; }
tr:nth-child(even){ background-color: #f2f2f2; }
tr:hover { background-color: #ddd; }
.status-active { color: green; font-weight: bold; }
.status-missing { color: red; font-weight: bold; }
</style>
</head>
<body>
<h2>Environment Variables Dashboard</h2>
"""

for branch, vars_list in all_env_data.items():
    html_content += f"<h3>{branch} Environment</h3>\n<table>\n<tr><th>Variable</th><th>Value</th><th>Status</th></tr>\n"
    for var in vars_list:
        status_class = "status-active" if var["status"] == "Active" else "status-missing"
        html_content += f"<tr><td>{var['variable']}</td><td>{var['value']}</td><td class='{status_class}'>{var['status']}</td></tr>\n"
    html_content += "</table>\n"

html_content += "</body></html>"

# Ensure dashboard directory exists
os.makedirs("dashboard", exist_ok=True)

with open("dashboard/env_dashboard.html", "w") as f:
    f.write(html_content)

print("✅ HTML dashboard with colors created successfully!")
