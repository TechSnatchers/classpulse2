"""
Setup script to create .env file for MongoDB Atlas
"""
import os

def create_env_file():
    """Create .env file from user input"""
    print("=" * 60)
    print("MongoDB Atlas Environment Setup")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled. Keeping existing .env file.")
            return
    
    # Get MongoDB password
    print("Enter your MongoDB Atlas database user password:")
    print("(The password for user: shawmi3030_db_user)")
    password = input("Password: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    # Get port (optional)
    port = input("Port (default: 3001): ").strip() or "3001"
    
    # Get database name (optional)
    db_name = input("Database name (default: learning_platform): ").strip() or "learning_platform"
    
    # Create .env content
    env_content = f"""# Server Configuration
PORT={port}

# MongoDB Atlas Configuration
MONGODB_URL=mongodb+srv://shawmi3030_db_user:{password}@m0.zcjoclr.mongodb.net/?appName=M0
DATABASE_NAME={db_name}
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print()
        print("✅ .env file created successfully!")
        print()
        print("📝 Next steps:")
        print("   1. Make sure your IP is whitelisted in MongoDB Atlas")
        print("   2. Run: python src/database/seed.py (to seed initial data)")
        print("   3. Run: python main.py (to start the server)")
        print()
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()

