import React, { ReactNode } from 'react';
import { Permission, Role } from '../../types/auth';
import { useAuth } from '../../context/AuthContext';

interface AccessGuardProps {
  children: ReactNode;
  roles?: Role | Role[];
  permissions?: Permission | Permission[];
  fallback?: ReactNode;
}

/**
 * A unified component that conditionally renders children based on user roles and/or permissions
 * Replaces both RoleGuard and PermissionGuard with a single, more flexible component
 */
export const AccessGuard: React.FC<AccessGuardProps> = ({ 
  children, 
  roles = [], 
  permissions = [], 
  fallback = null 
}) => {
  const { user, can } = useAuth();
  
  // If no user, deny access
  if (!user) {
    return fallback ? <>{fallback}</> : null;
  }
  
  const hasAccess = () => {
    // Normalize roles/permissions to arrays
    const requiredRoles = Array.isArray(roles) ? roles : roles ? [roles] : [];
    const requiredPermissions = Array.isArray(permissions) ? permissions : permissions ? [permissions] : [];
    
    // If neither roles nor permissions specified, grant access
    if (requiredRoles.length === 0 && requiredPermissions.length === 0) {
      return true;
    }
    
    // Check roles if specified
    if (requiredRoles.length > 0 && !requiredRoles.includes(user.role)) {
      return false;
    }
    
    // Check permissions if specified
    if (requiredPermissions.length > 0) {
      const hasAllPermissions = requiredPermissions.every(permission => can(permission));
      if (!hasAllPermissions) {
        return false;
      }
    }
    
    // All checks passed
    return true;
  };

  return hasAccess() ? <>{children}</> : <>{fallback}</>;
};

export default AccessGuard;