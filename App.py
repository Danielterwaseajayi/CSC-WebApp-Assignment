from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/check', methods=['POST'])
def check():
    ssid = request.form.get('wifi')
    password = None
    error = None

    if ssid:
        try:
            # Run Windows command to get WiFi profile info
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear'],
                capture_output=True, text=True
            )
            output = result.stdout
            # Find the password in the command output
            for line in output.splitlines():
                if "Key Content" in line:
                    password = line.split(":", 1)[1].strip()
                    break
            if not password:
                error = "Password not found or profile does not exist."
        except Exception as e:
            error = f"Error: {e}"
    else:
        error = "Please enter a WiFi name."

    return render_template('home.html', ssid=ssid, password=password, error=error)

if __name__ == '__main__':
    app.run(debug=True)