#!/bin/sh
# Start Samba in the background
/usr/sbin/smbd -F &

# Start Flask with Waitress
/opt/venv/bin/python /run.py
