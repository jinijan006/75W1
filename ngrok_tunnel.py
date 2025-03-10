import os
import time
import subprocess
import requests

def get_ngrok_tcp_url():
    try:
        # Fetch the ngrok TCP URL from the ngrok API
        response = requests.get("http://localhost:4040/api/tunnels")
        response.raise_for_status()
        tunnels = response.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == 'tcp':
                return tunnel['public_url']
    except Exception as e:
        print(f"Error fetching ngrok TCP URL: {e}")
    return None

def main():
    # Start ngrok tunnel
    ngrok_process = subprocess.Popen(["./ngrok/ngrok.exe", "tcp", "3389"])

    try:
        # Wait for ngrok to start and fetch the TCP URL
        tcp_url = None
        while not tcp_url:
            time.sleep(5)  # Wait for ngrok to initialize
            tcp_url = get_ngrok_tcp_url()
            if tcp_url:
                print(f"ngrok TCP URL: {tcp_url}")
                # Write the TCP URL to a file for GitHub Actions
                with open("ngrok_tcp_url.txt", "w") as f:
                    f.write(tcp_url)
            else:
                print("Waiting for ngrok to start...")

        # Keep the tunnel active for 6 hours
        time.sleep(6 * 60 * 60)  # 6 hours

    finally:
        # Terminate the ngrok process
        ngrok_process.terminate()
        ngrok_process.wait()

if __name__ == "__main__":
    main()