import pyodbc
conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS01;DATABASE=YourDatabaseName;Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.tables")
tables = cursor.fetchall()
for table in tables:
    print(table)
