#!/bin/bash

# Check if port 8000 is in use
PORT=8000
PID=$(lsof -t -i:$PORT)

# If the port is in use, kill the process
if [ ! -z "$PID" ]; then
    echo "Port $PORT is in use by process $PID. Killing the process..."
    kill -9 $PID
else
    echo "Port $PORT is free."
fi

# Start Django server
echo "Starting Django server on port $PORT..."
python manage.py runserver
