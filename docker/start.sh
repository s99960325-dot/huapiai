#!/bin/bash
set -e

cd /app

export DATA_PATH="${DATA_PATH:-/app/data}"
export CONFIG_PATH="${CONFIG_PATH:-$DATA_PATH/config.yaml}"

# Copy default data
# check if data directory exists
if [ ! -d "$DATA_PATH" ]; then
    echo "Data directory does not exist, creating..."
    mkdir -p "$DATA_PATH"
fi

# check if data directory empty
if [ -z "$(ls -A "$DATA_PATH")" ]; then
    echo "Data directory is empty, copying default data..."
    cp -r /tmp/data/. "$DATA_PATH"
fi

# create default config
if [ ! -f "$CONFIG_PATH" ]; then
    echo "Config file does not exist, creating..."
    mkdir -p "$(dirname "$CONFIG_PATH")"
    # 必须配置 web，否则无法访问
    cat <<EOF > "$CONFIG_PATH"
web:
    host: 0.0.0.0
    port: 8080
EOF
fi

python -m huapir