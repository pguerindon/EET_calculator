# EET Calculator Server Administration

This document describes the most common administration tasks for an EET Calculator server running on Ubuntu with Gunicorn and systemd.

## Service Management

### Check the service status

```bash
sudo systemctl status eet
```

Displays whether the service is running, when it was started, the associated Gunicorn processes and the latest log messages.

---

### Stop the service

```bash
sudo systemctl stop eet
```

Stops Gunicorn and the EET Calculator application.

---

### Start the service

```bash
sudo systemctl start eet
```

Starts the EET Calculator service.

---

### Restart the service

```bash
sudo systemctl restart eet
```

Restarts the service.

Use this command after:

- updating the application
- modifying Python code
- modifying templates
- updating translations
- changing configuration files

## Logs

### Follow the service log

```bash
sudo journalctl -u eet -f
```

Displays log messages in real time.

Press **Ctrl+C** to stop.

---

### Display the last 50 log entries

```bash
sudo journalctl -u eet -n 50
```

---

### Display the log since the last boot

```bash
sudo journalctl -u eet -b
```

## Automatic Startup

Check whether the service starts automatically after boot.

```bash
sudo systemctl is-enabled eet
```

Expected result:

```text
enabled
```

## Scheduled Maintenance

The server uses cron for periodic maintenance tasks.

Current scheduled jobs:

- hourly GoAccess statistics update
- daily removal of TEST calculations older than 7 days
- yearly removal of calculations from season N-2 (1 July)

Display the current cron configuration:

```bash
sudo crontab -l
```

Edit the cron configuration:

```bash
sudo crontab -e
```

## Purge Log

The yearly purge writes a log file:

```text
/opt/eet_calculator/logs/purge.log
```

Each execution records:

- execution date and time
- purged season
- deleted Calculation Keys
- total number of deleted calculations

## Application Update

1. Copy the new application files into:

```text
/opt/eet_calculator
```

2. Restart the service:

```bash
sudo systemctl restart eet
```

3. Verify the deployment:

```bash
sudo systemctl status eet
```

## Frequently Used Commands

```bash
sudo systemctl restart eet
sudo systemctl status eet
sudo journalctl -u eet -f
sudo crontab -l
```