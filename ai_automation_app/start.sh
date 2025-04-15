#\!/bin/bash
# Consolidated startup script
# Usage: ./start.sh [local|docker|app]

MODE=${1:-local}

case $MODE in
  local)
    echo "Starting in local mode..."
    # Contents from start-local.sh
    ;;
  docker)
    echo "Starting in docker mode..."
    # Contents from run-docker.sh
    ;;
  app)
    echo "Starting application..."
    # Contents from start-app.sh
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Usage: ./start.sh [local|docker|app]"
    exit 1
    ;;
esac
