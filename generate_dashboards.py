import json
import os
from jinja2 import Environment, FileSystemLoader

branches = ['Development', 'QA', 'UAT', 'Production']
all_data = {}

for branch in branches:
    branch_data = {'appsettings': [], 'docker_env': []}

    # Read AppSettings JSON
    appsettings_file = f'appsettings.{branch}.json'
    if os.path.exists(appsettings_file):
        with open(appsettings_file) as f:
            try:
                data = json.load(f)
                for app in data.get("AppSettings", []):
                    for s in app.get("Settings", []):
                        branch_data['appsettings'].append({
                            'sql': s.get("Dev_MySql_Connection_String", "N/A"),
                            'logging': s.get("Logging", "N/A")
                        })
            except Exception as e:
                branch_data['appsettings'].append({'sql': 'Parse error', 'logging': str(e)})
    else:
        branch_data['appsettings'].append({'sql': 'Missing', 'logging': 'Missing'})

    # Read Dockerfile ENV
    dockerfile_name = f'Dockerfile.{branch}'
    if os.path.exists(dockerfile_name):
        with open(dockerfile_name) as f:
            for line in f:
                line = line.strip()
                if line.startswith('ENV'):
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        key_val = parts[1].split('=', 1)
                        if len(key_val) == 2:
                            branch_data['docker_env'].append({'key': key_val[0], 'value': key_val[1]})
    else:
        branch_data['docker_env'].append({'key': 'Missing', 'value': 'Missing'})

    all_data[branch] = branch_data

# Render HTML
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('env_dashboard_template.html')

html_output = template.render(branches=branches, all_data=all_data)

# Write dashboard
os.makedirs('dashboard', exist_ok=True)
with open('dashboard/environment_dashboard.html', 'w') as f:
    f.write(html_output)

print("✅ HTML dashboard created with AppSettings + Dockerfile ENV")
