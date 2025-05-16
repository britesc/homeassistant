#!/usr/bin/env python3
# coding: utf-8
# drug_class.py :- Used to Operate with Drugs on Home Assistant
"""
    HA Drugs Class.
    
    This class is Used to Operate with Drugs on Home Assistant
    Version: 2.0.0
    Dated: 20250508
    Author: jB
"""
# Python Standard Libraries
import subprocess
import sys
from datetime import timedelta, date, datetime
import time
import logging as logger


def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Package '{package}' installed.")

# Python Specialist Libraries
ensure_package("sqlite3")
ensure_package("paho.mqtt.client")

import sqlite3
import paho.mqtt.client as mqtt


# Define Class
class HA_Drugs:

# Start Class Intrinsic Functions    
    def __init__(self, user: str) -> None:
        """
            Class __init__ function.
        """
        self.user = user

        self.APP = {}
        self.APP['AUTHOR']  = "Julian"
        self.APP['VERSION'] = "Dev 1.0.0"

        self.ERRORS_DICTIONARY = {}
        self.ERRORS_DICTIONARY['ERROR_CODE']            = 0 
        self.ERRORS_DICTIONARY['ERROR_MESSAGE']         = "No Errors."

        self.DB_DICTIONARY = {}
        self.DB_DICTIONARY['DATABASE_PATH']             = f"/config/users/{self.user}/{self.user}_v1.db"
        self.DB_DICTIONARY['TABLE_NAME']                = "Medicine"
        self.DB_DICTIONARY['EXISTS_TABLE']              = f'''SELECT name FROM sqlite_master
                                                        WHERE type='table' 
                                                        AND name='{self.DB_DICTIONARY['TABLE_NAME']}';
                                                        '''
        self.DB_DICTIONARY['CREATE_TABLE']              = f'''CREATE TABLE IF NOT EXISTS {self.DB_DICTIONARY['TABLE_NAME']} (
                                                        'drug_name' TEXT  PRIMARY KEY,
                                                        'date_updated' DATETIME NOT NULL DEFAULT (CURRENT_DATE),
                                                        'pack_quantity' INTEGER DEFAULT 0,
                                                        'dose_00' INTEGER DEFAULT 0,
                                                        'dose_01' INTEGER DEFAULT 0,
                                                        'dose_02' INTEGER DEFAULT 0,
                                                        'dose_03' INTEGER DEFAULT 0,
                                                        'dose_04' INTEGER DEFAULT 0,
                                                        'dose_05' INTEGER DEFAULT 0,
                                                        'dose_06' INTEGER DEFAULT 0,
                                                        'dose_07' INTEGER DEFAULT 0,
                                                        'dose_08' INTEGER DEFAULT 0,
                                                        'dose_09' INTEGER DEFAULT 0,
                                                        'dose_10' INTEGER DEFAULT 0,
                                                        'dose_11' INTEGER DEFAULT 0,
                                                        'dose_12' INTEGER DEFAULT 0,
                                                        'dose_13' INTEGER DEFAULT 0,
                                                        'dose_14' INTEGER DEFAULT 0,
                                                        'dose_15' INTEGER DEFAULT 0,
                                                        'dose_16' INTEGER DEFAULT 0,
                                                        'dose_17' INTEGER DEFAULT 0,
                                                        'dose_18' INTEGER DEFAULT 0,
                                                        'dose_19' INTEGER DEFAULT 0,
                                                        'dose_20' INTEGER DEFAULT 0,
                                                        'dose_21' INTEGER DEFAULT 0,
                                                        'dose_22' INTEGER DEFAULT 0,
                                                        'dose_23' INTEGER DEFAULT 0,
                                                        WITHOUT ROWID);'''
        self.DB_DICTIONARY['MONOPROST']                 = f'''
                                                        INSERT OR REPLACE INTO {self.DB_DICTIONARY['TABLE_NAME']}
                                                        ('drug_name',
                                                        'pack_quantity',
                                                        'dose_23')
                                                        VALUES ('Monoprost', '30', '1');
                                                        '''
        self.DB_DICTIONARY['SQL_QUERY']                 = None
        self.DB_DICTIONARY['DRUG_NAME']                 = None
        self.DB_DICTIONARY['DRUG_UPDATE']               = None
        self.DB_DICTIONARY['DRUG_QUANTITY']             = None
        self.DB_DICTIONARY['DRUG_DOSE']                 = None
        self.DB_DICTIONARY['DRUG_DAYS_SINCE']           = None
        self.DB_DICTIONARY['DRUG_DOSES_USED']           = None
        self.DB_DICTIONARY['DRUG_DOSES_REMAIN']         = None
        self.DB_DICTIONARY['DRUG_DAYS_LEFT']            = None
        self.DB_DICTIONARY['DRUG_DOSE_DAYS']            = None
        self.DB_DICTIONARY['DRUG_EXPIRY_DATE']          = None
        self.DB_DICTIONARY['DRUG_RENEWAL_DATE']         = None
        self.DB_DICTIONARY['DRUG_MESSAGE']              = "Sufficient"

        self.MQTT_DICTIONARY = {}
        self.MQTT_DICTIONARY['MQTT_CLIENT_ID']          = "HA_MED_JULIAN"
        self.MQTT_DICTIONARY['MQTT_BROKER_ADDDRESS']    = "10.10.20.10"
        self.MQTT_DICTIONARY['MQTT_BROKER_PORT']        = 1883
        self.MQTT_DICTIONARY['MQTT_QOS']                = 1   # Quality of Service level (0, 1, or 2)
        self.MQTT_DICTIONARY['MQTT_RETAIN']             = True  # Retain flag enabled
        self.MQTT_DICTIONARY['MQTT_TIMEOUT']            = 5
        self.MQTT_DICTIONARY['MQTT_TOPIC']              = f"homeassistant/julian/{self.DB_DICTIONARY['TABLE_NAME']}/"
        self.MQTT_DICTIONARY['MQTT_PAYLOAD']            =  None

        logger.basicConfig(level=logger.INFO)  
        logger.info("drug_class.py invoked at {}".format(time.time()))      

# Create Setters
    def setMQTTBroker(self, broker, port) -> None:
        """
            Define the MQTT Broker
        """ 
        self.MQTT_DICTIONARY['MQTT_BROKER_ADDDRESS'] = broker
        self.MQTT_DICTIONARY['MQTT_BROKER_PORT']     = port

# Create Getters
    def getMQTTBroker(self) -> dict:
        """
            Return the MQTT Broker
        """
        return self.MQTT_DICTIONARY

    def getdBInfo(self) -> dict:
        """
            Return the dB Information.
        """
        return self.DB_DICTIONARY

    def getErrorInfo(self) -> dict:
        """
            Return the Error Information.
        """
        return self.ERRORS_DICTIONARY

    def get_days_since(self) -> None:
        """
            Get the Number of Days since last update
        """        
        try:
            past_date = datetime.strptime(self.DB_DICTIONARY['DRUG_UPDATE'], "%Y-%m-%d").date()
            today = datetime.today().date()
            if past_date > today:
                self.ERRORS_DICTIONARY['ERROR_CODE']     = 100 
                self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "The given date is in the future. Please provide a past date."
                exit(self.ERRORS_DICTIONARY['ERROR_CODE'])
            delta = today - past_date
            self.DB_DICTIONARY['DRUG_DAYS_SINCE'] = delta.days
        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 101 
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Invalid date format. Use YYYY-MM-DD."
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def get_doses_used(self) -> None:
        """
            Get the Number of Doses Used.
        """
        try:
            self.DB_DICTIONARY['DRUG_DOSES_USED'] = self.DB_DICTIONARY['DRUG_DOSE'] * self.DB_DICTIONARY['DRUG_DAYS_SINCE']
        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 102
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible Dose"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def get_doses_left(self) -> None:
        """
            Get the Number of Doses Left.
        """
        try:
            self.DB_DICTIONARY['DRUG_DOSES_REMAIN'] = self.DB_DICTIONARY['DRUG_QUANTITY'] - self.DB_DICTIONARY['DRUG_DOSES_USED']
        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 103
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible Dose"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def get_days_left(self) -> None:
        """
            Get the Number of Days Left.
        """
        try:
            self.DB_DICTIONARY['DRUG_DAYS_LEFT'] = int(self.DB_DICTIONARY['DRUG_DOSES_REMAIN'] / self.DB_DICTIONARY['DRUG_DOSE'])       
        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 104
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible Dose"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def get_drug_days_left(self) -> None:
        """
            Get the Number of Days by Dose.
        """
        try:
            self.DB_DICTIONARY['DRUG_DOSE_DAYS'] = int(self.DB_DICTIONARY['DRUG_QUANTITY'] / self.DB_DICTIONARY['DRUG_DOSE'])       
        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 105
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible Dose"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def get_renewal_dates(self) -> None:
        """
            Get te Renewal Dates.
        """        
        try:
            # Convert string to datetime object
            date_obj = datetime.strptime(self.DB_DICTIONARY['DRUG_UPDATE'], "%Y-%m-%d")
            # Add Dose days and Renewal (-7)
            new_date = date_obj + timedelta(days=self.DB_DICTIONARY['DRUG_DOSE_DAYS'])
            self.DB_DICTIONARY['DRUG_EXPIRY_DATE'] = new_date.strftime("%a %d %b %Y")
            new_date = date_obj + timedelta(days=(self.DB_DICTIONARY['DRUG_DOSE_DAYS']-7))
            self.DB_DICTIONARY['DRUG_RENEWAL_DATE'] = new_date.strftime("%a %d %b %Y")
        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 106
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible to Calculate Dates"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def get_renewal_message(self) -> None:
        """
            Get te Renewal Dates.
        """        
        try:
            # Update Date
            date_then = datetime.strptime(self.DB_DICTIONARY['DRUG_EXPIRY_DATE'], "%a %d %b %Y")
            # Now
            date_now = datetime.now()
            # Calculate the difference
            delta = date_then - date_now
            # print(f"Delta {delta.days}")
            if delta.days <= 7:
                self.DB_DICTIONARY['DRUG_MESSAGE'] = "** Renew **"
            if delta.days <= 0:
                self.DB_DICTIONARY['DRUG_MESSAGE'] = "** Expired **"

        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 107
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible to Create Message"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

# Get the date for the Drug 
    def query_database(self, drug_name):
        try:
            self.DB_DICTIONARY['DRUG_NAME'] = drug_name
            self.DB_DICTIONARY['SQL_QUERY'] = f'SELECT "drug_name", "date_updated", "pack_quantity", SUM("dose_00" + "dose_01" + "dose_02" + "dose_03" + "dose_04" + "dose_05" + "dose_06" + "dose_07" + "dose_08" + "dose_09" + "dose_10" + "dose_11" + "dose_12" + "dose_13" + "dose_14" + "dose_15" + "dose_16" + "dose_17" + "dose_18" + "dose_19" + "dose_20" + "dose_21" + "dose_22" + "dose_23") FROM "{self.DB_DICTIONARY['TABLE_NAME']}" WHERE "drug_name" =  \'{drug_name}\';'

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.DB_DICTIONARY['SQL_QUERY'])

            # Commit Change
            conn.commit()
            # Fetch all results
            results = cursor.fetchone()
        
            # Close the connection
            conn.close()
            if len(results) > 0:
                self.DB_DICTIONARY['DRUG_UPDATE']       = results[1]
                self.DB_DICTIONARY['DRUG_QUANTITY']     = results[2]
                self.DB_DICTIONARY['DRUG_DOSE']         = results[3]
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 108
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    def post_mqtt_messages(self) -> None:
        """
            Update MQTT.
        """        
        try:
            # Create MQTT client
            client = mqtt.Client(client_id="HA_MED_JULIAN",
            transport='TCP',
            protocol=mqtt.MQTTv311,
            clean_session=True)
            
            # Connect to broker
            client.connect(self.MQTT_DICTIONARY['MQTT_BROKER_ADDDRESS'], self.MQTT_DICTIONARY['MQTT_BROKER_PORT'])
            client.loop_start()

            self.MQTT_DICTIONARY['MQTT_TOPIC'] = f"homeassistant/julian/medicine/{self.DB_DICTIONARY['DRUG_NAME']}/expiry_date"
            self.MQTT_DICTIONARY['MQTT_PAYLOAD'] = self.DB_DICTIONARY['DRUG_EXPIRY_DATE']   
            client.publish(self.MQTT_DICTIONARY['MQTT_TOPIC'], self.MQTT_DICTIONARY['MQTT_PAYLOAD'], qos=self.MQTT_DICTIONARY['MQTT_QOS'], retain=self.MQTT_DICTIONARY['MQTT_RETAIN'])
            time.sleep(0.25)

            self.MQTT_DICTIONARY['MQTT_TOPIC'] = f"homeassistant/julian/medicine/{self.DB_DICTIONARY['DRUG_NAME']}/renewal_date"
            self.MQTT_DICTIONARY['MQTT_PAYLOAD'] = self.DB_DICTIONARY['DRUG_RENEWAL_DATE']   
            client.publish(self.MQTT_DICTIONARY['MQTT_TOPIC'], self.MQTT_DICTIONARY['MQTT_PAYLOAD'], qos=self.MQTT_DICTIONARY['MQTT_QOS'], retain=self.MQTT_DICTIONARY['MQTT_RETAIN'])
            time.sleep(0.25)

            self.MQTT_DICTIONARY['MQTT_TOPIC'] = f"homeassistant/julian/medicine/{self.DB_DICTIONARY['DRUG_NAME']}/message"
            self.MQTT_DICTIONARY['MQTT_PAYLOAD'] = self.DB_DICTIONARY['DRUG_MESSAGE']   
            client.publish(self.MQTT_DICTIONARY['MQTT_TOPIC'], self.MQTT_DICTIONARY['MQTT_PAYLOAD'], qos=self.MQTT_DICTIONARY['MQTT_QOS'], retain=self.MQTT_DICTIONARY['MQTT_RETAIN'])
            time.sleep(0.25)

            # Clean up
            client.loop_stop()
            client.disconnect()

        except ValueError:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 109
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Impossible to Create MQTT Output"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])            

# Create Table medicine if not exist
    def createTable(self) -> None:
        """
            Create the Meds Table if it does not exist
        """ 
        try:
            self.DB_DICTIONARY['SQL_QUERY'] = self.DB_DICTIONARY['CREATE_TABLE']

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.DB_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Close the connection
            conn.close()            
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 110
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

# Insert or Update Medicine Row
    def createUpdateMedicine(self, IorUString) -> None:
        """
            Insert or Update Medicine Row
        """ 
        try:
            self.DB_DICTIONARY['SQL_QUERY'] = IorUString

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.DB_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Close the connection
            conn.close()            
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 111
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    # Check the Table Exists
    def checkTableExists(self) -> bool:
        """
            Check the Table Exists
        """
        try:
            self.DB_DICTIONARY['SQL_QUERY'] = IorUString

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.DB_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Close the connection
            conn.close()
            return True
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 112
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])


    def do_run(self) -> None:
        """
            Do Run.
        """        
        self.get_days_since()
        self.get_doses_used()
        self.get_doses_left()
        self.get_days_left()
        self.get_drug_days_left()
        self.get_renewal_dates()
        self.get_renewal_message()
        self.post_mqtt_messages()

if __name__ == "__main__":
    print("Class Testing by running directly\n")    
    had = HA_Drugs("julian")
    had.createTable()

    had.setMQTTBroker("10.10.20.10", 1883)

    had.query_database('Monoprost')
    had.do_run()

    had.query_database('Rivotril')
    had.do_run()    

    had.query_database('Tramadol')
    had.do_run()    

    had.query_database('Venlafaxina')
    had.do_run() 

    had.query_database('Levetiracetam')
    had.do_run() 

    # had.get_days_since()
    # had.get_doses_used()
    # had.get_doses_left()
    # had.get_days_left()
    # had.get_drug_days_left()
    # had.get_renewal_dates()
    # had.get_renewal_message()
    # had.post_mqtt_messages()

    print(had.getMQTTBroker())
    print("\n")
    print(had.getdBInfo())
    print("\n")
    print(had.getErrorInfo())
    print("\n")
