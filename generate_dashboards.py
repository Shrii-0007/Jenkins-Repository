import os
import json
from jinja2 import Template

# HTML template for dashboard
HTML_TEMPLATE = """
<html>
<head>
    <title>Branch Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; }
        h2 { color: #16a085; }
        table { border-collapse: collapse; width: 60%; margin-bottom: 30px; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background-color: #2c3e50; color: white; }
    </style>
</head>
<body>
<h1>Branch Environment Dashboard</h1>
{% for branch, env_vars in data.items() %}
    <h2>{{ branch }}</h2>
    <table>
        <tr><th>Key</th><th>Value</th></tr>
        {% for k, v in env_vars.items() %}
            <tr><td>{{ k }}</td><td>{{ v }}</td></tr>
        {% endfor %}
    </table>
{% endfor %}
</body>
</html>
"""

def load_env(branch_file):
    try:
        with open(branch_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Could not read {branch_file}: {e}")
        return {}

def main():
    data = {}
    for file in os.listdir("."):
        if file.startswith("appsettings.") and file.endswith(".json"):
            branch = file.replace("appsettings.", "").replace(".json", "")
            data[branch] = load_env(file)

    template = Template(HTML_TEMPLATE)
    html = template.render(data=data)

    with open("dashboard.html", "w") as f:
        f.write(html)

    print("✅ Dashboard generated: dashboard.html")

if __name__ == "__main__":
    main()

