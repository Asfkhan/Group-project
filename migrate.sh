#!/bin/sh

echo "Running database migrations..."
flask db upgrade
echo "Database migrations complete."

