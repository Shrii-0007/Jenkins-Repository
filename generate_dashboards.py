import os
import json
import re
from jinja2 import Environment, FileSystemLoader

branches = ['Development', 'QA', 'UAT', 'Production']
all_env_data = {}

# Function to parse Dockerfile ENV/ARG variables
def parse_dockerfile(path):
    if not os.path.exists(path):
        return [{"variable":"N/A","value":"N/A"}]
    
    envs = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^(ENV|ARG)\s+(.*)$', line)
            if m:
                rest = m.group(2)
                # Support multiple variables in one ENV line
                parts = re.findall(r'(\w+)=("[^"]*"|\S+)', rest)
                for key, val in parts:
                    envs.append({"variable": key, "value": val})
    return envs if envs else [{"variable":"N/A","value":"N/A"}]

for branch in branches:
    # Read AppSettings
    app_path = f"tmp_{branch}/appsettings.{branch}.json"
    app_vars = []
    if os.path.exists(app_path):
        with open(app_path) as f:
            data = json.load(f)
            for app in data.get("AppSettings", []):
                for s in app.get("Settings", []):
                    app_vars.append({
                        "variable": s.get("Name", "N/A"),
                        "value": s.get("Value", "N/A")
                    })
    else:
        app_vars = [{"variable":"N/A","value":"N/A"}]

    # Read Dockerfile
    docker_path = f"tmp_{branch}/Dockerfile.{branch}"
    docker_vars = parse_dockerfile(docker_path)

    all_env_data[branch] = {
        "appsettings": app_vars,
        "docker": docker_vars
    }

# Render dashboard
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('env_dashboard_template.html')
output = template.render(all_env_data=all_env_data)

# Ensure output folder exists
os.makedirs("dashboard", exist_ok=True)
with open("dashboard/environment_dashboard.html", "w") as f:
    f.write(output)

print("✅ Dashboard created successfully!")

