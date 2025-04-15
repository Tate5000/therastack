#\!/bin/bash

# Remove the original services now that they've been consolidated
echo "Removing original services after consolidation..."

# Remove billing and payments services (now consolidated into financial)
rm -rf /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/backend/services/billing
rm -rf /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/backend/services/payments

# Remove redundant auth guard components (now consolidated into AccessGuard)
rm -f /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/frontend/components/auth/PermissionGuard.tsx
rm -f /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/frontend/components/auth/RoleGuard.tsx

# Remove redundant start scripts (now consolidated into start.sh)
rm -f /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/start-app.sh
rm -f /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/start-local.sh
rm -f /mnt/c/Users/Tate/dev/Therastack/ai_automation_app/run-docker.sh

echo "Cleanup complete\!"
