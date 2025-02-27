#!/usr/bin/env python
import getpass
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv


def reset_database():
    """Reset the PostgreSQL database using direct commands."""
    
    # Try to load environment variables from .env.local
    script_dir = Path(__file__).resolve().parent
    api_dir = script_dir.parent
    env_path = api_dir / '.env'
    
    print(f"Looking for .env.local at: {env_path}")
    if env_path.exists():
        print(f".env.local file found at {env_path}")
        load_dotenv(env_path)
    else:
        print(f"Warning: .env.local file not found at {env_path}")
    
    # Get database connection details from environment or prompt
    db_name = os.getenv('DB_DATABASE')
    if db_name:
        print(f"Using database name from .env.local: {db_name}")
    else:
        db_name = input("Enter database name: ")
    
    db_user = os.getenv('DB_USERNAME')
    if db_user:
        print(f"Using username from .env.local: {db_user}")
    else:
        db_user = input("Enter database username [postgres]: ") or "postgres"
    
    db_password = os.getenv('DB_PASSWORD')
    if db_password:
        print("Using password from .env.local")
    
    # If password not in env, prompt for it securely
    if not db_password:
        db_password = getpass.getpass(f"Enter password for user {db_user}: ")
    
    db_host = os.getenv('DB_HOST')
    if db_host:
        print(f"Using host from .env.local: {db_host}")
    else:
        db_host = input("Enter database host [localhost]: ") or "localhost"
    
    db_port = os.getenv('DB_PORT')
    if db_port:
        print(f"Using port from .env.local: {db_port}")
    else:
        db_port = input("Enter database port [5432]: ") or "5432"
    
    # Confirm before proceeding
    print(f"\nAbout to reset database '{db_name}' on {db_host}:{db_port}")
    confirm = input("This will DELETE ALL DATA. Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    # Set password environment variable for PostgreSQL commands
    os.environ['PGPASSWORD'] = db_password
    
    # Build connection string for PostgreSQL commands
    pg_conn = f"postgresql://{db_user}@{db_host}:{db_port}/postgres"
    
    try:
        # Terminate existing connections to the database
        print(f"Terminating existing connections to {db_name}...")
        terminate_cmd = f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{db_name}'
        AND pid <> pg_backend_pid();
        """
        subprocess.run(
            ["psql", pg_conn, "-c", terminate_cmd],
            check=True
        )
        
        # Drop the database
        print(f"Dropping database {db_name}...")
        subprocess.run(
            ["psql", pg_conn, "-c", f"DROP DATABASE IF EXISTS {db_name};"],
            check=True
        )
        
        # Create the database again
        print(f"Creating database {db_name}...")
        subprocess.run(
            ["psql", pg_conn, "-c", f"CREATE DATABASE {db_name};"],
            check=True
        )
        
        print(f"\nDatabase '{db_name}' has been reset successfully!")
        print("\nIf you're using migrations, you may need to run:")
        print("flask db stamp head  # Mark migrations as complete")
        print("flask db migrate     # Create new migration if needed")
        print("flask db upgrade     # Apply migrations")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("\nMake sure PostgreSQL is running and your credentials are correct.")
    finally:
        # Clear password from environment for security
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']


if __name__ == "__main__":
    reset_database() 