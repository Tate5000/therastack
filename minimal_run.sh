#\!/bin/bash

# This script provides a minimal way to run the application after extreme cleanup
# It only installs the absolute minimum dependencies needed

FRONTEND_DIR="/mnt/c/Users/Tate/dev/Therastack/ai_automation_app/frontend"
BACKEND_DIR="/mnt/c/Users/Tate/dev/Therastack/ai_automation_app/backend"

# Create a minimal package.json with only essential dependencies
echo "Setting up minimal frontend dependencies..."
mkdir -p $FRONTEND_DIR/minimal
cat > $FRONTEND_DIR/minimal/package.json << 'EOF'
{
  "name": "therastack-minimal",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "next": "^13.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
EOF

# Create a minimal backend setup
echo "Setting up minimal backend dependencies..."
mkdir -p $BACKEND_DIR/minimal
cat > $BACKEND_DIR/minimal/requirements.txt << 'EOF'
fastapi==0.95.0
uvicorn==0.21.1
pydantic==1.10.7
EOF

# Create a minimal docker-compose
echo "Creating minimal docker-compose.yml..."
cat > /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/minimal-docker-compose.yml << 'EOF'
version: '3'

services:
  frontend:
    build:
      context: ./frontend/minimal
    ports:
      - "3000:3000"
    command: npm run dev
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public

  backend:
    build:
      context: ./backend/minimal
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --reload
    volumes:
      - ./backend:/app
EOF

echo "Minimal setup completed\!"
echo "To run the application:"
echo "1. cd /mnt/c/Users/Tate/dev/Therastack/ai_automation_app"
echo "2. docker-compose -f minimal-docker-compose.yml up"
