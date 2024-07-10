from flask import Flask, request, jsonify
import paramiko
from ftplib import FTP

app = Flask(__name__)

@app.route('/check_access', methods=['GET'])
def check_access():
    ip = request.args.get('ip')
    port = int(request.args.get('port'))
    username = request.args.get('username')
    password = request.args.get('password')
    protocol = request.args.get('protocol').lower()

    if protocol == 'ssh':
        success = check_ssh_access(ip, port, username, password)
    elif protocol == 'ftp':
        success = check_ftp_access(ip, port, username, password)
    else:
        return jsonify({"status": "error", "message": "Invalid protocol"}), 400

    return jsonify({"status": "success" if success else "failure"}), 200

def check_ssh_access(ip, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        client.connect(ip, port=port, username=username, password=password)

        return True
    except Exception as e:
        print(f"Failed to connect to the SSH server: {e}")
        return False
    finally:
        client.close()

def check_ftp_access(ip, port, username, password):
    try:
        ftp = FTP()
        ftp.connect(ip, port)
        ftp.login(user=username, passwd=password)

        return True
    except Exception as e:
        print(f"Failed to connect to the FTP server: {e}")
        return False
    finally:
        ftp.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
