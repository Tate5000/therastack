import { NextApiRequest, NextApiResponse } from 'next';
import { Auth } from 'aws-amplify';
import cookie from 'cookie';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Parse the cookie from the request
    const cookies = cookie.parse(req.headers.cookie || '');
    const token = cookies.auth_token;

    if (!token) {
      return res.status(401).json({ error: 'No authentication token found' });
    }

    // Initialize AWS Amplify with the token
    // This would be done globally in a real app
    const isValid = await validateTokenWithCognito(token);
    
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }

    return res.status(200).json({ isValid: true });
  } catch (error) {
    console.error('Token validation error:', error);
    return res.status(401).json({ error: 'Authentication failed' });
  }
}

async function validateTokenWithCognito(token: string): Promise<boolean> {
  try {
    // In a real implementation, you would verify the token with Cognito
    // For development, we'll just check if it's a non-empty string
    return token.length > 0;
    
    // Production implementation would be:
    // const user = await Auth.currentAuthenticatedUser();
    // return !!user;
  } catch (error) {
    return false;
  }
}