import os
import subprocess
import pyodbc
from typing import List

# Setup connection to your target SQL Server instance (Local or Network Instance)
# Switch server string to "192.168.1.254\\FARMERSDESKLTD" if targeting the network server
SERVER_INSTANCE = "localhost\\SQLEXPRESS01"

def get_all_databases() -> List[str]:
    """Connects to the system master database to discover all user databases."""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER_INSTANCE};"
        f"DATABASE=master;"
        f"Trusted_Connection=yes;"
    )
    
    databases = []
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        
        # Query system tables while filtering out default Microsoft system databases
        cursor.execute("""
            SELECT name 
            FROM sys.databases 
            WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb', 'ReportServer', 'ReportServerTempDB')
        """)
        databases = [row[0] for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        print(f"Error querying SQL Server instance: {e}")
    
    return databases

def generate_python_models(db_name: str):
    """Uses sqlacodegen to dynamically write the Python ORM mapping classes."""
    print(f"\n[1/2] Generating Python models for database: '{db_name}'...")
    
    output_filename = f"{db_name.lower()}_models.py"
    
    # We use URL-encoded syntax (%5C) for the backslash to prevent command-line parsing failures
    server_escaped = SERVER_INSTANCE.replace("\\", "%5C")
    connection_url = f"mssql+pyodbc://@localhost/{db_name}?driver=ODBC+Driver+17+for+SQL+Server&server={server_escaped}"
    
    command = f"sqlacodegen {connection_url} --outfile={output_filename}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"  ✅ Code architecture compiled successfully to: {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to generate python models: {e}")

def extract_database_data(db_name: str):
    """Dynamically reads tables, columns, and rows from the selected database."""
    print(f"\n[2/2] Extracting raw table structural data from: '{db_name}'...")
    
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_INSTANCE};DATABASE={db_name};Trusted_Connection=yes;"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Query the information schema for the targeted database
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"  Found {len(tables)} tables in {db_name}:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
            row_count = cursor.fetchone()[0]
            print(f"   -> [dbo].[{table:<20}] containing {row_count} records.")
            
        conn.close()
        print(f"\nData mapping for '{db_name}' complete!")
    except Exception as e:
        print(f"  ❌ Data read failed: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("       UNIVERSAL SQL SERVER DATA CODESYNC        ")
    print("==================================================")
    
    # 1. Fetch available target databases on the system
    db_list = get_all_databases()
    
    if not db_list:
        print("No user databases found or instance is unreachable.")
    else:
        print("\nAvailable Databases discovered on the instance:")
        for idx, db_name in enumerate(db_list, start=1):
            print(f" [{idx}] {db_name}")
            
        # 2. Let the user choose which database they want to target dynamically
        try:
            choice = int(input("\nEnter the number of the database you want to map: "))
            if 1 <= choice <= len(db_list):
                selected_db = db_list[choice - 1]
                
                # 3. Process the chosen target database automatically
                generate_python_models(selected_db)
                extract_database_data(selected_db)
            else:
                print("Invalid choice selection.")
        except ValueError:
            print("Please enter a valid numeric choice option.")
