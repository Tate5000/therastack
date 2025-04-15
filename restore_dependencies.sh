#\!/bin/bash

echo "Restoring essential dependencies..."

# Restore frontend dependencies
cd /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/frontend
npm install --production

# Restore backend dependencies
cd /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Dependencies restored. You may need to run 'npm install' to restore development dependencies if needed."
