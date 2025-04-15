#\!/bin/bash

echo "Starting deep cleanup of unnecessary files..."

# Remove all node_modules directories (can be reinstalled with npm install)
find /mnt/c/Users/Tate/dev/Therastack -name "node_modules" -type d -exec rm -rf {} +

# Remove all Python virtual environments (can be recreated)
find /mnt/c/Users/Tate/dev/Therastack -name "venv" -type d -exec rm -rf {} +
find /mnt/c/Users/Tate/dev/Therastack -name "__pycache__" -type d -exec rm -rf {} +
find /mnt/c/Users/Tate/dev/Therastack -name "*.pyc" -delete

# Remove build artifacts
find /mnt/c/Users/Tate/dev/Therastack -name "build" -type d -exec rm -rf {} +
find /mnt/c/Users/Tate/dev/Therastack -name "dist" -type d -exec rm -rf {} +
find /mnt/c/Users/Tate/dev/Therastack -name ".next" -type d -exec rm -rf {} +

# Remove temporary files
find /mnt/c/Users/Tate/dev/Therastack -name ".cache" -type d -exec rm -rf {} +
find /mnt/c/Users/Tate/dev/Therastack -name "*.log" -delete
find /mnt/c/Users/Tate/dev/Therastack -name ".DS_Store" -delete

# Remove duplicate configuration files
find /mnt/c/Users/Tate/dev/Therastack -name "Dockerfile.simple" -delete

echo "Deep cleanup completed\!"
