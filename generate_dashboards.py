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
                        key, val = p.split('=', 1)
                        envs.append({"variable": key, "value": val, "status": "Active" if val else "Missing"})
    return envs if envs else [{"variable":"N/A","value":"N/A","status":"Missing"}]

# Process each branch
for branch in branches:
    # Parse AppSettings JSON
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

    # Parse Dockerfile
    docker_path = f"tmp_{branch}/Dockerfile"
    docker_vars = parse_dockerfile(docker_path)

    # Store for Jinja template
    all_env_data[branch] = {
        "appsettings": app_vars,
        "docker": docker_vars
    }

# Render HTML using Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('env_dashboard_template.html')

rendered = template.render(all_env_data=all_env_data)

# Ensure dashboard directory exists
os.makedirs("dashboard", exist_ok=True)

# Save HTML
with open("dashboard/environment_dashboard.html", "w") as f:
    f.write(rendered)

print("✅ HTML dashboard created successfully!")

