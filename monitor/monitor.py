import os
import time
import subprocess
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database configuration
db_user = os.getenv('POSTGRES_USER', 'user')
db_password = os.getenv('POSTGRES_PASSWORD', 'password')
db_name = os.getenv('POSTGRES_DB', 'netmon_db')
db_host = os.getenv('DB_HOST', 'db')

DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def ping_device(ip_address):
    """Ping a device and return status and latency."""
    try:
        # Use ping -c 1 (Linux) or -n 1 (Windows)
        # In Docker (Linux), we use -c 1
        start_time = time.time()
        # Using a timeout of 2 seconds
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '2', ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        latency = (time.time() - start_time) * 1000
        
        if result.returncode == 0:
            return 'Online', latency
        else:
            return 'Offline', None
    except Exception as e:
        print(f"Error pinging {ip_address}: {e}")
        return 'Offline', None

def monitor():
    print("Monitoring service started...")
    while True:
        session = Session()
        try:
            # Get all devices
            result = session.execute(text("SELECT id, name, ip_address FROM device"))
            devices = result.fetchall()
            
            for device_id, name, ip_address in devices:
                print(f"Checking {name} ({ip_address})...")
                status, latency = ping_device(ip_address)
                
                # Update status in DB
                session.execute(
                    text("UPDATE device SET status = :status, latency = :latency, last_seen = :last_seen WHERE id = :id"),
                    {
                        'status': status,
                        'latency': latency,
                        'last_seen': datetime.now(),
                        'id': device_id
                    }
                )
            
            session.commit()
            print("Status updated successfully.")
        except Exception as e:
            print(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()
        
        # Wait for 30 seconds before next check
        time.sleep(30)

if __name__ == '__main__':
    # Wait for DB to be ready
    print("Waiting for database...")
    time.sleep(10)
    monitor()
