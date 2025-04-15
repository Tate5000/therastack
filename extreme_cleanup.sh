#\!/bin/bash

echo "Starting extreme cleanup to drastically reduce file count..."

# DANGER: This will remove ALL node_modules directories
echo "Removing ALL node_modules directories..."
find /mnt/c/Users/Tate/dev/Therastack -name "node_modules" -type d -print -exec rm -rf {} \; 2>/dev/null || true

# Remove Python virtual environments and caches
echo "Removing Python virtual environments and caches..."
find /mnt/c/Users/Tate/dev/Therastack -name "venv" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "__pycache__" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "*.pyc" -print -delete 2>/dev/null || true

# Remove all git repositories
echo "Removing .git directories..."
find /mnt/c/Users/Tate/dev/Therastack -name ".git" -type d -print -exec rm -rf {} \; 2>/dev/null || true

# Remove build artifacts
echo "Removing build artifacts..."
find /mnt/c/Users/Tate/dev/Therastack -name "build" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "dist" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name ".next" -type d -print -exec rm -rf {} \; 2>/dev/null || true

# Remove package locks (but preserve package.json)
echo "Removing package locks..."
find /mnt/c/Users/Tate/dev/Therastack -name "package-lock.json" -print -delete 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "yarn.lock" -print -delete 2>/dev/null || true

# Remove temporary files
echo "Removing temporary files..."
find /mnt/c/Users/Tate/dev/Therastack -name ".cache" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "*.log" -print -delete 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name ".DS_Store" -print -delete 2>/dev/null || true

# Remove test directories
echo "Removing test directories..."
find /mnt/c/Users/Tate/dev/Therastack -name "tests" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "__tests__" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "test" -type d -print -exec rm -rf {} \; 2>/dev/null || true

# Remove docs directories
echo "Removing documentation directories..."
find /mnt/c/Users/Tate/dev/Therastack -name "docs" -type d -print -exec rm -rf {} \; 2>/dev/null || true
find /mnt/c/Users/Tate/dev/Therastack -name "examples" -type d -print -exec rm -rf {} \; 2>/dev/null || true

echo "Extreme cleanup completed\! This should have drastically reduced the file count."
