import { Request, Response, NextFunction } from 'express';

export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  // Mock authentication - in real app, verify JWT token
  // For development, allow requests without auth header
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    // In development, allow requests without auth
    // In production, uncomment the following:
    // return res.status(401).json({ error: 'Unauthorized' });
    
    // Mock user for development
    (req as any).user = {
      id: 'user123',
      role: 'student',
    };
    return next();
  }

  // Mock user - in real app, decode JWT and get user from database
  // Try to extract role from header if provided
  const role = req.headers['x-user-role'] as string || 'student';
  
  (req as any).user = {
    id: 'user123',
    role: role, // 'student', 'instructor', or 'admin'
  };

  next();
};

