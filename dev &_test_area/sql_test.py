import sqlite3


def query_database(db_path, query):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Close the connection
        conn.close()
        
        return results
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    database_path = "/home/julian/julian_v1.db"  # Change to your database path
    sql_query = 'SELECT * FROM "julian_meds";'  # Change to your SQL query
    
    results = query_database(database_path, sql_query)
    
    if results:
        for row in results:
            print(row)
