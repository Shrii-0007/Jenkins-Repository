import json
import os
import re
from jinja2 import Environment, FileSystemLoader

# List of branches to process
branches = ['Development', 'QA', 'UAT', 'Production']
all_env_data = {}

# Function to parse Dockerfile ENV/ARG variables
def parse_dockerfile(path):
    if not os.path.exists(path):
        return [{"variable":"N/A","value":"N/A","status":"Missing"}]
    
    envs = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^(ENV|ARG)\s+(.*)$', line)
            if m:
                rest = m.group(2)
                parts = re.split(r'\s+', rest)
                for p in parts:
                    if '=' in p:
                        key, val = p.split('=',1)
                        envs.append({
                            "variable": key,
                            "value": val,
                            "status": "Active" if val else "Missing"
                        })
    return envs if envs else [{"variable":"N/A","value":"N/A","status":"Missing"}]

# Process each branch
for branch in branches:
    # appsettings JSON
    app_path = f"tmp_{branch}/appsettings.{branch}.json"
    try:
        with open(app_path, "r") as f:
            data = json.load(f)
            app_vars = []
            for app in data.get("AppSettings", []):
                for s in app.get("Settings", []):
                    app_vars.append({
                        "variable": s.get("Name", "N/A"),
                        "value": s.get("Value", "N/A"),
                        "status": "Active" if s.get("Value") else "Missing"
                    })
    except FileNotFoundError:
        app_vars = [{"variable":"N/A","value":"N/A","status":"Missing"}]
    
    # Dockerfile env (branch-specific)
    docker_path = f"tmp_{branch}/Dockerfile.{branch}"
    docker_vars = parse_dockerfile(docker_path)
    
    # Store combined
    all_env_data[branch] = {
        "appsettings": app_vars,
        "docker": docker_vars
    }

# Ensure dashboard directory exists
os.makedirs("dashboard", exist_ok=True)

# Jinja2 template setup
env = Environment(loader=FileSystemLoader('.'), autoescape=True)
template_content = """
<html>
<head>
    <title>Jenkins Environment Dashboard</title>
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
<h1>Jenkins Environment Dashboard</h1>

{% for branch, data in all_env_data.items() %}
    <h2>{{ branch }} Environment - AppSettings</h2>
    <table>
        <tr><th>Variable</th><th>Value</th><th>Status</th></tr>
        {% for var in data.appsettings %}
            <tr>
                <td>{{ var.variable }}</td>
                <td>{{ var.value }}</td>
                <td class="{{ 'status-active' if var.status=='Active' else 'status-missing' }}">{{ var.status }}</td>
            </tr>
        {% endfor %}
    </table>

    <h2>{{ branch }} Environment - Dockerfile ENV</h2>
    <table>
        <tr><th>Variable</th><th>Value</th><th>Status</th></tr>
        {% for var in data.docker %}
            <tr>
                <td>{{ var.variable }}</td>
                <td>{{ var.value }}</td>
                <td class="{{ 'status-active' if var.status=='Active' else 'status-missing' }}">{{ var.status }}</td>
            </tr>
        {% endfor %}
    </table>
{% endfor %}

</body>
</html>
"""

template = env.from_string(template_content)
rendered = template.render(all_env_data=all_env_data)

# Save the HTML dashboard
out_file = os.path.join("dashboard", "environment_dashboard.html")
with open(out_file, "w") as f:
    f.write(rendered)

print("✅ HTML dashboard generated with branch-wise AppSettings and Dockerfile ENV!")

