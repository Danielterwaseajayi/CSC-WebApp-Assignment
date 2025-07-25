from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

def get_wifi_password(ssid):
    try:
        # Run netsh command to get WiFi profile details
        result = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear'],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in result.splitlines():
            if "Key Content" in line:
                return line.split(":")[1].strip()
        return None  # No password found
    except subprocess.CalledProcessError:
        return None

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/check', methods=['POST'])
def check_password():
    ssid = request.form.get('wifi')
    if not ssid:
        return render_template('home.html', error="SSID is required")

    password = get_wifi_password(ssid)
    if password:
        return render_template('home.html', ssid=ssid, password=password)
    else:
        return render_template('home.html', ssid=ssid, error="Password not found or SSID doesn't exist.")

if __name__ == '__main__':
    app.run(debug=True)
