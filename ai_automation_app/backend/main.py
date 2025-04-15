from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import boto3
import json
import logging
import os
import time
from jose import jwt, JWTError
from mangum import Mangum
import uvicorn

# Import AWS SDK for Cognito
from botocore.exceptions import ClientError

# Import service routers
from services.calendar_dynamodb.calendar_api import router as calendar_router
from services.messages_dynamodb.message_api import router as message_router
from services.call_manager.call_manager_api import router as call_manager_router
from services.billing.billing_api import router as billing_router
from services.payments.payments_api import router as payments_router
from services.ai_assistant.ai_assistant_api import router as ai_assistant_router

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize FastAPI
app = FastAPI(
    title="TheraStack API",
    description="Backend API for the TheraStack healthcare platform",
    version="0.1.0"
)

# Get environment vars
STAGE = os.environ.get('STAGE', 'dev')
REGION = os.environ.get('AWS_REGION', 'us-east-2')
USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
APP_CLIENT_ID = os.environ.get('COGNITO_APP_CLIENT_ID')

# Define allowed origins based on environment
FRONTEND_DOMAIN = os.environ.get('FRONTEND_DOMAIN', 'app.therastack.com')
ALLOWED_ORIGINS = [
    f"https://{FRONTEND_DOMAIN}",
    f"https://api.{FRONTEND_DOMAIN}"
]

# Add localhost origins for development
if STAGE == 'dev':
    ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004"
    ])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security setup
security = HTTPBearer()

# JWT validation function
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validates the JWT token from Cognito"""
    try:
        token = credentials.credentials
        
        # In production environment, validate with Cognito
        if STAGE != 'local' and USER_POOL_ID:
            # Initialize Cognito client
            cognito = boto3.client('cognito-idp', region_name=REGION)
            
            try:
                # Validate token with Cognito
                response = cognito.get_user(AccessToken=token)
                username = response['Username']
                
                # Get user's groups (roles)
                user_groups = []
                try:
                    group_response = cognito.admin_list_groups_for_user(
                        Username=username,
                        UserPoolId=USER_POOL_ID
                    )
                    user_groups = [group['GroupName'] for group in group_response.get('Groups', [])]
                except ClientError as e:
                    logger.warning(f"Could not get user groups: {str(e)}")
                
                return {"sub": username, "groups": user_groups}
            except ClientError as e:
                logger.error(f"Token validation error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired token"
                )
        else:
            # For local development with no Cognito, just decode the token
            try:
                payload = jwt.decode(token, options={"verify_signature": False})
                return payload
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token format"
                )
    except Exception as e:
        logger.error(f"Auth error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Include API routers
app.include_router(calendar_router)
app.include_router(message_router)
app.include_router(call_manager_router)
app.include_router(billing_router)
app.include_router(payments_router)
app.include_router(ai_assistant_router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to TheraStack API",
        "version": "0.1.0",
        "environment": STAGE
    }

# Health check endpoint for deployment verification
@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
        "service": "TheraStack API",
        "timestamp": int(time.time()),
        "environment": STAGE
    }

# Create handler for AWS Lambda
handler = Mangum(app)

# For local development
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)