// Authentication and authorization service

import { User, Role, Permission } from '../types/auth';

// Role definitions with associated permissions
export const ROLES: Record<Role, { name: string; description: string; permissions: Permission[] }> = {
  patient: {
    name: 'Patient',
    description: 'Regular patient user with access to their own data and appointments',
    permissions: [
      'view_own_profile',
      'view_own_appointments',
      'create_own_appointments', 
      'view_own_documents',
      'upload_own_documents',
      'delete_own_documents',
      'view_own_therapists'
    ]
  },
  doctor: {
    name: 'Doctor/Therapist',
    description: 'Medical professional with access to assigned patients',
    permissions: [
      'view_own_profile',
      'view_own_appointments',
      'view_assigned_patients',
      'view_patient_documents',
      'upload_patient_documents',
      'create_patient_notes',
      'complete_appointments',
      'generate_ai_summaries'
    ]
  },
  admin: {
    name: 'Administrator',
    description: 'System administrator with full access',
    permissions: [
      'view_all_profiles',
      'edit_all_profiles',
      'view_all_appointments',
      'create_all_appointments',
      'delete_all_appointments',
      'view_all_documents',
      'upload_all_documents',
      'delete_all_documents',
      'manage_users',
      'manage_roles',
      'manage_permissions',
      'system_configuration'
    ]
  }
};

// Permission descriptions
export const PERMISSION_DESCRIPTIONS: Record<Permission, string> = {
  // Profile permissions
  view_own_profile: 'View your own profile information',
  view_all_profiles: 'View all user profiles',
  edit_all_profiles: 'Edit all user profiles',
  
  // Appointment permissions
  view_own_appointments: 'View your own appointments',
  view_assigned_patients: 'View appointments for assigned patients',
  view_all_appointments: 'View all appointments in the system',
  create_own_appointments: 'Create appointments for yourself',
  create_all_appointments: 'Create appointments for any user',
  delete_all_appointments: 'Delete any appointment',
  complete_appointments: 'Mark appointments as completed',
  
  // Document permissions
  view_own_documents: 'View your own documents',
  view_patient_documents: 'View documents for assigned patients',
  view_all_documents: 'View all documents in the system',
  upload_own_documents: 'Upload your own documents',
  upload_patient_documents: 'Upload documents for patients',
  upload_all_documents: 'Upload documents for any user',
  delete_own_documents: 'Delete your own documents',
  delete_all_documents: 'Delete any document in the system',
  generate_ai_summaries: 'Generate AI summaries of documents',
  create_patient_notes: 'Create notes for patients',
  
  // User management
  view_own_therapists: 'View your assigned therapists',
  manage_users: 'Create, edit, and disable user accounts',
  manage_roles: 'Assign and manage user roles',
  manage_permissions: 'Configure system permissions',
  
  // System
  system_configuration: 'Modify system-wide settings'
};

// AWS Amplify Authentication
import { Auth } from 'aws-amplify';
import { CognitoUser } from '@aws-amplify/auth';

// Authenticate with credentials using Cognito
export const loginWithCredentials = async (
  email: string,
  password: string
): Promise<{ user: User; token: string } | null> => {
  try {
    // Sign in with Cognito
    const cognitoUser = await Auth.signIn(email, password);
    
    // Get the JWT token
    const session = cognitoUser.getSignInUserSession();
    const token = session?.getIdToken().getJwtToken();
    
    if (!token) {
      throw new Error('Authentication failed - no token received');
    }
    
    // Get user attributes from Cognito token
    const payload = session?.getIdToken().decodePayload();
    const userGroups = payload['cognito:groups'] || [];
    
    // Map Cognito group to role
    let role: Role = 'patient';
    if (userGroups.includes('Admins')) {
      role = 'admin';
    } else if (userGroups.includes('Doctors')) {
      role = 'doctor';
    }
    
    // Get permissions for this role
    const rolePermissions = ROLES[role].permissions;
    
    // Create user object from Cognito attributes
    const user: User = {
      id: cognitoUser.getUsername(),
      email: payload.email,
      name: payload.name || payload.email,
      role: role,
      permissions: rolePermissions,
      metadata: {
        sub: payload.sub,
        ...payload['custom:metadata'] && JSON.parse(payload['custom:metadata'])
      }
    };
    
    // Store user data in HTTP-only cookie via API instead of localStorage
    // This is more secure than localStorage
    await fetch('/api/auth/session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ token })
    });
    
    return {
      user,
      token
    };
  } catch (error) {
    console.error('Login error:', error);
    return null;
  }
};

// SSO authentication using Cognito's federated identity providers
export const loginWithSSO = async (provider: 'Google' | 'Facebook' | 'Apple'): Promise<{ user: User; token: string } | null> => {
  try {
    // Use Cognito's federated sign-in
    await Auth.federatedSignIn({ provider: provider as any });
    
    // Get the current session once the redirect completes
    const session = await Auth.currentSession();
    const token = session.getIdToken().getJwtToken();
    
    // Get user attributes from Cognito token
    const payload = session.getIdToken().decodePayload();
    const userGroups = payload['cognito:groups'] || [];
    
    // Map Cognito group to role (default to patient for SSO)
    let role: Role = 'patient';
    if (userGroups.includes('Admins')) {
      role = 'admin';
    } else if (userGroups.includes('Doctors')) {
      role = 'doctor';
    }
    
    // Get permissions for this role
    const rolePermissions = ROLES[role].permissions;
    
    // Create user object from Cognito attributes
    const user: User = {
      id: payload.sub,
      email: payload.email,
      name: payload.name || payload.email,
      role: role,
      permissions: rolePermissions,
      metadata: {
        sub: payload.sub,
        identityProvider: provider,
        ...payload['custom:metadata'] && JSON.parse(payload['custom:metadata'])
      }
    };
    
    // Store user data in HTTP-only cookie via API instead of localStorage
    await fetch('/api/auth/session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ token })
    });
    
    return {
      user,
      token
    };
  } catch (error) {
    console.error('SSO login error:', error);
    return null;
  }
};

// Gets the current authenticated session from Cognito
export const getCurrentSession = async (): Promise<{ user: User; token: string } | null> => {
  try {
    // Check current authentication state with Cognito
    const cognitoUser = await Auth.currentAuthenticatedUser();
    const session = cognitoUser.getSignInUserSession();
    const token = session?.getIdToken().getJwtToken();
    
    if (!token) {
      return null;
    }
    
    // Get user attributes from Cognito token
    const payload = session.getIdToken().decodePayload();
    const userGroups = payload['cognito:groups'] || [];
    
    // Map Cognito group to role
    let role: Role = 'patient';
    if (userGroups.includes('Admins')) {
      role = 'admin';
    } else if (userGroups.includes('Doctors')) {
      role = 'doctor';
    }
    
    // Get permissions for this role
    const rolePermissions = ROLES[role].permissions;
    
    // Create user object from Cognito attributes
    const user: User = {
      id: cognitoUser.getUsername(),
      email: payload.email,
      name: payload.name || payload.email,
      role: role,
      permissions: rolePermissions,
      metadata: {
        sub: payload.sub,
        ...payload['custom:metadata'] && JSON.parse(payload['custom:metadata'])
      }
    };
    
    return {
      user,
      token
    };
  } catch (error) {
    // User is not authenticated
    return null;
  }
};

// Logs out the current user from Cognito
export const logout = async (): Promise<void> => {
  try {
    // Sign out from Cognito
    await Auth.signOut();
    
    // Clear session cookie
    await fetch('/api/auth/logout', {
      method: 'POST'
    });
  } catch (error) {
    console.error('Logout error:', error);
  }
};

// Checks if a user has a specific permission
export const hasPermission = (user: User, permission: Permission): boolean => {
  return user.permissions.includes(permission);
};

// Ensures a user has all the permissions required for their role
export const ensureUserHasRolePermissions = (user: User): User => {
  const roleName = user.role;
  const rolePermissions = ROLES[roleName].permissions;
  
  // Create a new set of permissions that includes all the role's standard permissions
  // while preserving any custom permissions the user might have
  const updatedPermissions = Array.from(new Set([
    ...user.permissions,
    ...rolePermissions
  ]));
  
  return {
    ...user,
    permissions: updatedPermissions
  };
};

// Checks if the current user can access specific patient data
export const canAccessPatientData = (
  user: User,
  patientId: string
): boolean => {
  // Admins can access all patient data
  if (user.role === 'admin') {
    return true;
  }
  
  // Patients can only access their own data
  if (user.role === 'patient') {
    return user.id === patientId || user.metadata.patientId === patientId;
  }
  
  // Doctors can access data for their assigned patients
  if (user.role === 'doctor' && user.metadata.patients) {
    return (user.metadata.patients as string[]).includes(patientId);
  }
  
  return false;
};