from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import ssl
from urllib.parse import quote_plus, urlparse, urlunparse

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        import codecs
        if hasattr(sys.stdout, 'detach'):
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    except:
        pass

# Load .env file from backend directory
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

# Global database instance
db = MongoDB()

def escape_mongodb_url(url: str) -> str:
    """
    Properly escape username and password in MongoDB connection string.
    Handles both mongodb:// and mongodb+srv:// formats.
    """
    if not url or "://" not in url:
        return url
    
    # Parse the URL
    parsed = urlparse(url)
    
    # If there's no username/password, return as is
    if not parsed.username and not parsed.password:
        return url
    
    # Escape username and password using quote_plus (RFC 3986)
    username = quote_plus(parsed.username) if parsed.username else ""
    password = quote_plus(parsed.password) if parsed.password else ""
    
    # Reconstruct the netloc with escaped credentials
    if username and password:
        netloc = f"{username}:{password}@{parsed.hostname}"
        # Only add port if it exists (mongodb+srv:// doesn't have ports)
        if parsed.port:
            netloc += f":{parsed.port}"
    elif username:
        netloc = f"{username}@{parsed.hostname}"
        if parsed.port:
            netloc += f":{parsed.port}"
    else:
        netloc = parsed.netloc
    
    # Reconstruct the full URL
    escaped_url = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    
    return escaped_url

async def connect_to_mongo():
    """Create database connection"""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "learning_platform")
    
    # Escape username and password in the connection string
    mongodb_url = escape_mongodb_url(mongodb_url)
    
    # Check if using MongoDB Atlas (mongodb+srv://)
    if "mongodb+srv://" in mongodb_url:
        print("🔗 Connecting to MongoDB Atlas...")
        # For MongoDB Atlas, we need to handle SSL/TLS
        # Create SSL context that doesn't verify certificates (for development)
        # In production, you should use proper certificate verification
        try:
            import certifi
            # Use certifi certificates if available
            tls_ca_file = certifi.where()
            db.client = AsyncIOMotorClient(
                mongodb_url,
                tlsCAFile=tls_ca_file,
                tlsAllowInvalidCertificates=False
            )
        except ImportError:
            # If certifi is not installed, disable certificate verification (development only)
            print("⚠️  Warning: certifi not found. SSL verification disabled (development mode)")
            db.client = AsyncIOMotorClient(
                mongodb_url,
                tlsAllowInvalidCertificates=True
            )
    else:
        print("🔗 Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(mongodb_url)
    
    db.database = db.client[database_name]
    
    # Test connection
    try:
        await db.client.admin.command('ping')
        print(f"✅ Connected to MongoDB Atlas: {database_name}")
        print(f"📍 Database: {database_name}")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("💡 Make sure:")
        print("   1. Your MongoDB Atlas connection string is correct")
        print("   2. Your IP address is whitelisted in MongoDB Atlas")
        print("   3. Your database user password is correct")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("✅ MongoDB connection closed")

def get_database():
    """Get database instance"""
    return db.database

def get_database_by_name(database_name: str):
    """Get a specific database by name"""
    if db.client is None:
        return None
    return db.client[database_name]

