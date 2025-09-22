import json
import os
import re
from jinja2 import Environment, FileSystemLoader

# Branch list
branches = ['Development', 'QA', 'UAT', 'Production']
all_env_data = {}

# Root workspace
ROOT = os.getcwd()
TEMPLATE_DIR = os.path.join(ROOT, 'dashboard', 'templates')
OUT_DIR = os.path.join(ROOT, 'dashboard')

# Parse Dockerfile ENV/ARG variables
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
                parts = re.split(r'\s+', m.group(2))
                for p in parts:
                    if '=' in p:
                        key, val = p.split('=', 1)
                        envs.append({"variable": key, "value": val, "status": "Active" if val else "Missing"})
    return envs if envs else [{"variable":"N/A","value":"N/A","status":"Missing"}]

# Process each branch
for branch in branches:
    # AppSettings JSON
    app_path = os.path.join(ROOT, f"tmp_{branch}", f"appsettings.{branch}.json")
    try:
        with open(app_path, "r") as f:
            data = json.load(f)
            app_vars = [{"variable": s.get("Name", "N/A"),
                         "value": s.get("Value", "N/A"),
                         "status": "Active" if s.get("Value") else "Missing"}
                        for app in data.get("AppSettings", []) for s in app.get("Settings", [])]
            if not app_vars:
                app_vars = [{"variable":"N/A","value":"N/A","status":"Missing"}]
    except FileNotFoundError:
        app_vars = [{"variable":"N/A","value":"N/A","status":"Missing"}]

    # Dockerfile
    docker_path = os.path.join(ROOT, f"tmp_{branch}", "Dockerfile")
    docker_vars = parse_dockerfile(docker_path)

    # Combine
    all_env_data[branch] = {"appsettings": app_vars, "docker": docker_vars}

# Render Jinja2 template
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
template = env.get_template('env_dashboard_template.html')
rendered = template.render(all_env_data=all_env_data)

# Save dashboard
os.makedirs(OUT_DIR, exist_ok=True)
out_file = os.path.join(OUT_DIR, 'environment_dashboard.html')
with open(out_file, 'w') as f:
    f.write(rendered)

print("✅ HTML dashboard with appsettings + Dockerfile ENV created successfully!")

