from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import json
import os
import json
import os
import ssl
import socket

from flask_apscheduler import APScheduler

from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"




# Path to JSON file
DOMAIN_FILE = "domain.json"
 



  


# Initialize APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Define job ID and default interval
SEARCH_JOB_ID = "search_domains"
DEFAULT_INTERVAL = 3600  # 1 hour in seconds

def perform_search():
    """Task to check domain status and SSL info."""
    domains = load_domains()
    for domain in domains:
        domain["status"] = check_domain_status(domain["domain"])
        ssl_info = get_ssl_info(domain["domain"])
        domain["ssl_expiration"] = ssl_info["ssl_expiration"]
        domain["ssl_issuer"] = ssl_info["ssl_issuer"]
    save_domains(domains)
    print(f"Domain monitoring executed at {datetime.now()}")

# Add the default job
scheduler.add_job(
    id=SEARCH_JOB_ID,
    func=perform_search,
    trigger="interval",
    seconds=DEFAULT_INTERVAL,
)

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    """Update the search frequency or schedule."""
    data = request.get_json()
    frequency_type = data.get("frequency_type")
    value = data.get("value")

    try:
        # Remove existing job
        scheduler.remove_job(SEARCH_JOB_ID)

        # Add new job based on the schedule type
        if frequency_type == "interval":
            interval_seconds = max(int(value), 3600)  # Minimum interval: 1 hour
            scheduler.add_job(
                id=SEARCH_JOB_ID,
                func=perform_search,
                trigger="interval",
                seconds=interval_seconds,
            )
        elif frequency_type == "time":
            schedule_time = datetime.strptime(value, "%H:%M").time()
            scheduler.add_job(
                id=SEARCH_JOB_ID,
                func=perform_search,
                trigger="cron",
                hour=schedule_time.hour,
                minute=schedule_time.minute,
            )
        return jsonify({"message": "Schedule updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500






def load_domains():
    """Load domains from the JSON file."""
    if os.path.exists(DOMAIN_FILE):
        with open(DOMAIN_FILE, "r") as file:
            return json.load(file)
    return []


def save_domains(domains):
    """Save domains to the JSON file."""
    with open(DOMAIN_FILE, "w") as file:
        json.dump(domains, file, indent=4)


def get_ssl_info(domain):
    """Retrieve SSL expiration and issuer information for a domain."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                ssl_expiration = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                ssl_issuer = dict(x[0] for x in cert['issuer'])
                return {
                    "ssl_expiration": ssl_expiration.strftime("%Y-%m-%d"),
                    "ssl_issuer": ssl_issuer.get("organizationName", "Unknown")
                }
    except Exception:
        return {
            "ssl_expiration": "N/A",
            "ssl_issuer": "Unknown"
        }


def check_domain_status(domain):
    """Check if a domain is alive or down."""
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        return "Up" if response.status_code == 200 else f"Down ({response.status_code})"
    except requests.RequestException:
        return "Down"

# Load users from JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return []


# Save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        users = load_users()
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            session["user"] = username
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        users = load_users()
        if any(u['username'] == username for u in users):
            return jsonify({"message": "Username already exists!"}), 409

        users.append({"username": username, "password": password})
        save_users(users)
        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# @app.route('/dashboard')
# def dashboard():
#     if 'user' in session:
#         return f"Welcome, {session['user']}! <a href='/logout'>Logout</a>"
#     return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
@app.route('/get_domains', methods=['GET'])
def get_domains():
    """Return the list of domains."""
    return jsonify(load_domains())

@app.route('/dashboard')
def dashboard():
    """Render the main page."""
    return render_template('domain.html')

@app.route('/add_domain', methods=['POST'])
def add_domain():
    """Add a domain to the monitoring list."""
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain is required."}), 400

    domains = load_domains()

    if any(d["domain"] == domain for d in domains):
        return jsonify({"error": "Domain already exists."}), 400

    # Check domain status and SSL information
    status = check_domain_status(domain)
    ssl_info = get_ssl_info(domain)

    domain_entry = {
        "domain": domain,
        "status": status,
        "ssl_expiration": ssl_info["ssl_expiration"],
        "ssl_issuer": ssl_info["ssl_issuer"]
    }

    domains.append(domain_entry)
    save_domains(domains)

    return jsonify(domain_entry)


@app.route('/remove_domain', methods=['POST'])
def remove_domain():
    """Remove a domain from the monitoring list."""
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain is required."}), 400

    domains = load_domains()
    updated_domains = [d for d in domains if d["domain"] != domain]

    if len(updated_domains) == len(domains):
        return jsonify({"error": "Domain not found."}), 404

    save_domains(updated_domains)
    return jsonify({"message": f"Domain {domain} removed successfully."})

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
