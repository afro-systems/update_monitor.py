# update_monitor.py

`update_monitor.py` is a Python3 script that automates package updates on Linux.

## Features

- Updates the package list.
- Checks for available package upgrades.
- Performs available package upgrades.
- Updates Pi-hole.
- Runs `autoremove` to clean up unnecessary packages.
- Sends notifications via Pushover.
- Initiates a system reboot if kernel updates or initramfs changes are detected.

## Requirements

- Python 3
- Pushover account (user key and API token)
- Linux system with `apt` package manager
- Pi-hole installed (optional)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/update-monitor.git
    cd update-monitor
    ```

2. Install required Python packages:
    ```bash
    pip install requests
    ```

3. Set up environment variables for Pushover:
    ```bash
    export PUSHOVER_USER_KEY=your_pushover_user_key
    export PUSHOVER_API_TOKEN=your_pushover_api_token
    ```

4. Make the script executable:
    ```bash
    sudo chmod +x update_monitor.py
    sudo chmod u+s update_monitor.py
    ```

## Usage

Run the script manually:
```bash
./update_monitor.py
```

Or, set up a cron job to run the script periodically. Open your crontab editor:
```bash
crontab -e
```

Add the following lines to run the script daily at 2 AM:
```bash
export PUSHOVER_USER_KEY=your_pushover_user_key
export PUSHOVER_API_TOKEN=your_pushover_api_token
0 2 * * * /path/to/update_monitor.py
```
## Logging

The script logs its activities to /var/log/update_monitor.log.
**NOTE:** Make sure the script has the appropriate __permissions__ to write to this file.

```bash
sudo touch /var/log/update_monitor.log
sudo chown user:user /var/log/update_monitor.log
```

## Pushover Notifications

Ensure that the `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` environment variables are set correctly.

Notifications will be sent for the following events:
- When the system updates require a reboot.
- When an error occurs during the update process.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
