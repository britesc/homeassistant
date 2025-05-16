import sqlite3
import paho.mqtt.client as mqtt
from datetime import timedelta, date, datetime

DRUGNAME_IDX = 0
DRUGDATE_IDX = 1
DRUGHAVE_IDX = 2
DRUGDOSE_IDX = 3

DATABASE_PATH = "users/julian/julian_v1.db"
SQL_QUERY = 'SELECT "drug_name", "date_updated", "pack_quantity", SUM("dose_00" + "dose_01" + "dose_02" + "dose_03" + "dose_04" + "dose_05" + "dose_06" + "dose_07" + "dose_08" + "dose_09" + "dose_10" + "dose_11" + "dose_12" + "dose_13" + "dose_14" + "dose_15" + "dose_16" + "dose_17" + "dose_18" + "dose_19" + "dose_20" + "dose_21" + "dose_22" + "dose_23") FROM "julian_meds" WHERE "drug_name" = \'Monoprost\';'
# MQTT Broker Configuration
BROKER = "192.168.8.70"  # Change to your broker address
PORT = 1883  # Default MQTT port (use 8883 for TLS)
# TOPIC = "homeassistant/julian/medicine/drugname/expiry"
# PAYLOAD = "04/04/2025"  # Example payload
QOS = 1  # Quality of Service level (0, 1, or 2)
RETAIN = True  # Retain flag enabled

# Get the date for the Drug 
def query_database(db_path, query):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all results
        results = cursor.fetchone()
        
        # Close the connection
        conn.close()
        
        return results
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

def days_since(date_str):
    try:
        past_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        if past_date > today:
            print("The given date is in the future. Please provide a past date.")
            return 0
        delta = today - past_date
        print(f"Number of days since {past_date}: {delta.days}")
        return delta.days
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return 0

def get_doses_used(num_days, dose_per_day):
    try:
        return dose_per_day * num_days
    except ValueError:
        print("Impossible Dose")
        return 0

def get_doses_left(dose_total, used_dose):
    try:
        return dose_total - used_dose
    except ValueError:
        print("Impossible Dose")
        return 0

def get_days_left(num_days, dose_per_day):
    try:
        return int(num_days / dose_per_day)       
    except ValueError:
        print("Impossible Dose")
        return 0

def dates_left(date_str, days_left):
    try:
        past_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Add days left
        if days_left >= 0:
            expiry_date = past_date_obj + timedelta(days=days_left)

        renewal_date = date_obj + timedelta(days=(days_left-7))
    except ValueError:
        print("Impossible Dose")
        return 0

if __name__ == "__main__":
    results = query_database(DATABASE_PATH, SQL_QUERY)

    print(results)
    print(results[DRUGNAME_IDX])
    print(results[DRUGDATE_IDX])
    print(results[DRUGHAVE_IDX])
    print(results[DRUGDOSE_IDX])

    num_days = days_since(results[DRUGDATE_IDX])
    print(num_days)
    used_dose = get_doses_used(num_days, results[DRUGDOSE_IDX])
    print(used_dose)
    dose_left = get_doses_left(results[DRUGHAVE_IDX], used_dose)    
    print(dose_left)
    days_left = get_days_left(num_days, results[DRUGDOSE_IDX])
    print(days_left)
