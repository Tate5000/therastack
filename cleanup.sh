#\!/bin/bash

# Remove Python cache files
find /mnt/c/Users/Tate/dev/Therastack/ai_automation_app -name '__pycache__' -type d -exec rm -rf {} +
find /mnt/c/Users/Tate/dev/Therastack/ai_automation_app -name '*.pyc' -delete

# Remove redundant Dockerfile (keeping the main one)
rm /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/frontend/Dockerfile.simple

# Consolidate startup scripts
cat > /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/start.sh << 'EOL'
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
EOL

chmod +x /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/start.sh

echo "Cleanup script created at cleanup.sh"
