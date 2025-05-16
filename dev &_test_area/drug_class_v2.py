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
import os
import subprocess
import sys
from datetime import timedelta, date, datetime
import time
import logging as logger

# Setup Logging
def ensure_logging() -> None:
    logger.basicConfig(filename='home-assistant.log', level=logger.INFO)  
    logger.info("drug_class.py invoked at {}".format(time.time())) 

# This function allows us to ensure we have the 3rd Party Libraries
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

        # Create Dictionaries

        # App Dictionary
        self.APP_DICTIONARY = {}
        self.APP_DICTIONARY['AUTHOR']  = "Julian"
        self.APP_DICTIONARY['VERSION'] = "Dev 2.0.0"

        # Errors Dictionary
        self.ERRORS_DICTIONARY = {}
        self.ERRORS_DICTIONARY['ERROR_CODE']            = 0 
        self.ERRORS_DICTIONARY['ERROR_MESSAGE']         = "No Errors."

        # Database Dictionary
        self.DB_DICTIONARY = {}
        self.DB_DICTIONARY['DATABASE_PATH']             = f"/config/users/{self.user}/{self.user}_v1.db"
        self.DB_DICTIONARY['TABLE_NAME']                = "Medicine"
        self.DB_DICTIONARY['DRUG_NAME']                 = None

        # SQL Dictionary
        self.SQL_DICTIONARY = {}
        self.SQL_DICTIONARY['SQL_QUERY']                = None
        self.SQL_DICTIONARY['TABLE_EXISTS']             = f'''SELECT name FROM sqlite_master
                                                        WHERE type='table' 
                                                        AND name='{self.DB_DICTIONARY['TABLE_NAME']}';
                                                        '''
        self.SQL_DICTIONARY['TABLE_CREATE']             = f'''CREATE TABLE IF NOT EXISTS {self.DB_DICTIONARY['TABLE_NAME']} (
                                                        'drug_name' TEXT  PRIMARY KEY,
                                                        'date_updated' TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
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
        self.SQL_DICTIONARY['TABLE_DROP']               = f'''DROP TABLE 
                                                        {self.DB_DICTIONARY['TABLE_NAME']};
                                                        '''
        self.SQL_DICTIONARY['TABLE_ROWS_TOTAL']         = f'''SELECT COUNT(*)
                                                        FROM 
                                                        {self.DB_DICTIONARY['TABLE_NAME']};
                                                        '''
        self.SQL_DICTIONARY['TABLE_ROWS_DISTINCT']      = f'''SELECT COUNT(DISTINCT drug_name)
                                                        FROM 
                                                        {self.DB_DICTIONARY['TABLE_NAME']};
                                                        '''
        self.SQL_DICTIONARY['DRUGS_QUANTITY_LEFT']      = f'''SELECT 
                                                        'drug_name',
                                                        'date_updated", 
                                                        'pack_quantity", 
                                                        SUM(
                                                        'dose_00' + 
                                                        'dose_01' + 
                                                        'dose_02' + 
                                                        'dose_03' + 
                                                        'dose_04' + 
                                                        'dose_05' + 
                                                        'dose_06' + 
                                                        'dose_07' + 
                                                        'dose_08' + 
                                                        'dose_09' + 
                                                        'dose_10' + 
                                                        'dose_11' + 
                                                        'dose_12' + 
                                                        'dose_13' + 
                                                        'dose_14' + 
                                                        'dose_15' + 
                                                        'dose_16' + 
                                                        'dose_17' + 
                                                        'dose_18' + 
                                                        'dose_19' + 
                                                        'dose_20' + 
                                                        'dose_21' + 
                                                        'dose_22' + 
                                                        'dose_23'
                                                        ) 
                                                        FROM 
                                                        {self.DB_DICTIONARY['TABLE_NAME']} 
                                                        WHERE 'drug_name' = {self.DB_DICTIONARY['DRUG_NAME']};
                                                        '''



    # Create Setters

    # Create Database
    def createDatabase(self) -> None:
        """
            Create our Database.
        """
        pass
        # Created automatically

    # Drop Database
    def dropDatabase(self) -> bool:
        """
            Drop our Database.
        """
        try:
            if os.path.exists(self.DB_DICTIONARY['DATABASE_PATH']):
                os.remove(self.DB_DICTIONARY['DATABASE_PATH'])
                return True
            else:
                return False
        except (ValueError, RuntimeError, TypeError, NameError):
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 100 
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = "Cannot Drop Database."
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])

    # Does Table Exist
    def existTable(self) -> bool:
        """
            Does our Table Exist Already.
        """
        try:
            self.SQL_DICTIONARY['SQL_QUERY'] = self.SQL_DICTIONARY['TABLE_EXISTS']

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.SQL_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Fetch all results
            results = cursor.fetchone()
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 101
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])
        finally:
            # Close the connection
            conn.close()
            if results:
                return True
            else:
                return False

    # Create the Table
    def createTable(self) -> bool:
        """
            Does our Table Exist Already.
        """
        try:
            self.SQL_DICTIONARY['SQL_QUERY'] = self.SQL_DICTIONARY['TABLE_CREATE']

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.SQL_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Fetch all results
            results = cursor.fetchone()
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 102
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])
        finally:
            # Close the connection
            conn.close()
            if results:
                return True
            else:
                return False

    # Drop the Table
    def dropTable(self) -> bool:
        """
            Drop our Table.
        """
        try:
            self.SQL_DICTIONARY['SQL_QUERY'] = self.SQL_DICTIONARY['TABLE_DROP']

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.SQL_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Fetch all results
            results = cursor.fetchone()
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 103
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])
        finally:
            # Close the connection
            conn.close()
            if results:
                return True
            else:
                return False

    # Count the Table Rows
    def countTableRows(self) -> int:
        """
            Drop our Table.
        """
        try:
            self.SQL_DICTIONARY['SQL_QUERY'] = self.SQL_DICTIONARY['TABLE_ROWS_TOTAL']

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.SQL_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Fetch all results
            results = cursor.fetchone()[0]
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 104
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])
        finally:
            # Close the connection
            conn.close()
            if results:
                return results
            else:
                return None

    # Count the Table Rows
    def countTableRowsDistinct(self) -> int:
        """
            Drop our Table.
        """
        try:
            self.SQL_DICTIONARY['SQL_QUERY'] = self.SQL_DICTIONARY['TABLE_ROWS_DISTINCT']

            # Connect to the database
            conn = sqlite3.connect(self.DB_DICTIONARY['DATABASE_PATH'])
            cursor = conn.cursor()
        
            # Execute the query
            cursor.execute(self.SQL_DICTIONARY['SQL_QUERY'])

            # Commit the query
            conn.commit()

            # Fetch all results
            results = cursor.fetchone()[0]
        except sqlite3.Error as e:
            self.ERRORS_DICTIONARY['ERROR_CODE']     = 104
            self.ERRORS_DICTIONARY['ERROR_MESSAGE']  = f"SQL Error: {e}"
            logger.error("Code {}: {}".format(self.ERRORS_DICTIONARY['ERROR_CODE'], self.ERRORS_DICTIONARY['ERROR_MESSAGE']))
            exit(self.ERRORS_DICTIONARY['ERROR_CODE'])
        finally:
            # Close the connection
            conn.close()
            if results:
                return results
            else:
                return None




if __name__ == "__main__":
    print("Class Testing by running directly\n") 
    had = HA_Drugs("julian")
    print(f"Initialised HA_DRUGS = {had}")

    print("Phase 1")
    # Empty Function as not applicable
    print(f"   Creating Database is unnecessary (None) = {had.createDatabase()}")

    # Print True if dropped or false if not there or not dropped
    print(f"   Dropping Database                (True) = {had.dropDatabase()}")

    # Print True if exists or false if not there
    print(f"   Checking if Table Exists        (False) = {had.existTable()}")

    print("Phase 2")
    # Print True if created or false if not
    print(f"   Create Table Exists              (True) = {had.createTable()}")

    # Print True if exists or false if not there
    print(f"   Checking if Table Exists         (True) = {had.existTable()}")

    # Print True if exists or false if not there
    print(f"   Checking if Table Dropped        (True) = {had.dropTable()}")

    # Print True if exists or false if not there
    print(f"   Checking if Table Exists        (False) = {had.existTable()}")

    print("Phase 3")
    # Print True if created or false if not
    print(f"   Create Table Exists              (True) = {had.createTable()}")

    # Print True if exists or false if not there
    print(f"   Checking if Table Exists         (True) = {had.existTable()}")

    print("Phase 4")
    # Get the number of Rows in the Table
    print(f"   Checking Number of Rows          (None) = {had.countTableRows()}")

    # Get the number of Rows in the Table
    print(f"   Checking Number of Distinct Rows (0)    = {had.countTableRowsDistinct()}")