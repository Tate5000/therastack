# Auth Guards Refactoring Plan

## Current Structure
- /frontend/components/auth/PermissionGuard.tsx
- /frontend/components/auth/RoleGuard.tsx

## Consolidated Structure
- /frontend/components/auth/AccessGuard.tsx

## Migration Steps
1. Create the new AccessGuard component that accepts both roles and permissions as props
2. Update all imports and usages across the application
3. Test the consolidated guard component
4. Remove the old components after successful testing

## Example Implementation
```tsx
interface AccessGuardProps {
  children: React.ReactNode;
  roles?: string[];
  permissions?: string[];
  fallback?: React.ReactNode;
}

export const AccessGuard: React.FC<AccessGuardProps> = ({ 
  children, 
  roles = [], 
  permissions = [], 
  fallback = null 
}) => {
  const { user } = useAuth();
  
  const hasAccess = () => {
    // Check roles if specified
    if (roles.length > 0 && \!roles.some(role => user?.roles.includes(role))) {
      return false;
    }
    
    // Check permissions if specified
    if (permissions.length > 0 && \!permissions.some(perm => user?.permissions.includes(perm))) {
      return false;
    }
    
    // If no roles or permissions specified, or all checks passed
    return true;
  };

  return hasAccess() ? <>{children}</> : <>{fallback}</>;
};
```
