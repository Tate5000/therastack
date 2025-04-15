import { NextApiRequest, NextApiResponse } from 'next';
import { serialize } from 'cookie';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Clear the auth cookie by setting it to expire in the past
    res.setHeader(
      'Set-Cookie',
      serialize('auth_token', '', {
        httpOnly: true,
        secure: process.env.NODE_ENV !== 'development',
        sameSite: 'strict',
        maxAge: -1, // Expire immediately
        path: '/',
      })
    );

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Error clearing session:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}