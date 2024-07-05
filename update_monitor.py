#!/usr/bin/python3

import os
import subprocess
import requests
import re
import logging

# Configure logging
logging.basicConfig(filename='/var/log/update_monitor.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Read Pushover configuration from environment variables
PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')
PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
    raise ValueError("Update Monitor] Pushover user key and API token must be set as environment variables.")

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Update Monitor] Command failed: {command}\nError: {result.stderr}")
    return result.stdout

def send_pushover_notification(message):
    """Send a notification using Pushover."""
    data = {
        'token': PUSHOVER_API_TOKEN,
        'user': PUSHOVER_USER_KEY,
        'message': message
    }
    response = requests.post(PUSHOVER_URL, data=data)
    response.raise_for_status()

def main():
    try:
        logging.info("[Update Monitor] Updating package list...")
        run_command("sudo apt update")

        logging.info("[Update Monitor] Checking for package upgrades...")
        upgrade_check = run_command("sudo apt -s upgrade")
        if "upgraded," in upgrade_check:
            logging.info("[Update Monitor] Upgrading packages...")
            run_command("sudo apt upgrade -y")

            logging.info("[Update Monitor] Upgrading Pi-hole...")
            run_command("sudo PIHOLE_SKIP_OS_CHECK=true pihole -up")

            logging.info("[Update Monitor] Running autoremove...")
            autoremove_output = run_command("sudo apt-get autoremove -y")

            removed_packages = re.findall(r"Removing.*linux-image|Removing.*linux-headers|initramfs", autoremove_output)
            if removed_packages:
                message = "[Update Monitor] System reboot initiated due to updates. Changes: " + ", ".join(removed_packages)
                logging.info(message)

                logging.info("[Update Monitor] Sending Pushover notification...")
                send_pushover_notification(message)

                logging.info("[Update Monitor] Rebooting system...")
                run_command("sudo systemctl reboot")
            else:
                logging.info("[Update Monitor] No kernel updates or initramfs changes detected. No reboot needed.")
        else:
            logging.info("[Update Monitor] No package upgrades available.")

    except Exception as e:
        error_message = f"[Update Monitor] An error occurred: {str(e)}"
        logging.error(error_message)
        try:
            send_pushover_notification(error_message)
        except Exception as push_error:
            logging.error(f"[Update Monitor] Failed to send Pushover notification: {str(push_error)}")

if __name__ == "__main__":
    main()
