#!/usr/bin/env python3
# coding: utf-8
# class_gps.py :- Used to Read the GPS System
"""
    EARS JSON Config.
    
    This class Reads aand Wites the JSON Config.
    Version: 1.0.0
    Dated: 20241119
    Author: jB
"""

import gc
import machine
import utime, time

# Define Class
class Ears_GPS:

# Start Class Intrinsic Functions    
    def __init__(self) -> None:
        """
            Class __init__ function.
        """
        self.fixtype = ["None","GPS","DGPS"]
        self.buff = ""        

        self.gpssdict = {}
        

        # Define the UART pins and create a UART object
        self.gps_serial = machine.UART(0, baudrate=9600, tx=0, rx=1)
        
        print(self.gps_serial)
        
    """ Get $GPGGA and $GPRMC Info """
    def getGPS(self):    
        timeout = time.time() + 1
        print(f"Time out {timeout}")
        self.gpssdict["fix_type"] = self.fixtype[0]
        self.gpssdict["num_sats"] = 0
        
        """ Loop to read GPS Sentences """
        while True:
            """ Try / Except to ensure we catch the errors """
            try:
                if self.gps_serial.any():
                    line = self.gps_serial.readline()  # Read a complete line from the UART
                    if line:
                        line = line.decode('utf-8')
                        parts = line.split(',')
                        parts = [x.replace("\r\n","") for x in parts]

                        """ Get $GPGGA Info """ 
                        if (parts[0] == "$GPGGA" and len(parts) == 15):
                            print(f"$GPGGA Part 0  = {parts[0]}")
                            
                            """ Get Fix 0-2"""
                            if (parts[6]):
                                print(f"  Part 6 Fix   = {parts[6]}")
                                if 0 <= int(parts[6]) <= 2:                            
                                    self.gpssdict["fix_type"] = self.fixtype[int(parts[6])]
                                else:
                                    self.gpssdict["fix_type"] = self.fixtype[0]
                                print(f"  Part 6 Fix   = {self.gpssdict["fix_type"]}")
                            
                            """ Get Number of Satelittes """
                            if (parts[7]):
                                print(f"  Part 7 Sats  = {parts[7]}")
                                self.gpssdict["num_sats"] = int(parts[7])
                                print(f"  Part 7 Sats  = {self.gpssdict["num_sats"]}")
                            
                            """ Get Altitude """    
                            if (parts[9]):
                                print(f"  Part 9 Alt   = {parts[9]}")
                                self.gpssdict["altitude"] = int(parts[9])
                                print(f"  Part 9 Alt   = {self.gpssdict["altitude"]}")
                            
                            """ Get Altitude UOM """
                            if (parts[10]):
                                print(f"  Part 10 UOM  = {parts[10]}")
                                self.gpssdict["alt_uom"] = parts[10]
                                print(f"  Part 10 UOM  = {self.gpssdict["alt_uom"]}")
                                
                        """ End $GPGGA Info """
                            
                        """ Get $GPRMC Info """    
#                         if (parts[0] == "$GPRMC"):
#                             print(f"$GPRMC Length  = {len(parts)}")
                        if (parts[0] == "$GPRMC" and len(parts) == 13):                            
                            print(f"$GPRMC Part 0  = {parts[0]}")

                            """ Get UTC Time """                            
                            if (parts[1]):
                                print(f" Part 1 Time   = {parts[1]}")
                                if (float(parts[1]) > 0):
                                    self.gpssdict["utctime"] = int(float(parts[1]))
                                else:
                                    self.gpssdict["utctime"] = 0
                                print(f" Part 1 Time   = {self.gpssdict["utctime"]}")    
                                    
                            """ Get UTC Date """   
                            if (parts[9]):
                                print(f" Part 9 Date   = {parts[9]}")
                                if 0 <= int(parts[9]) <= 2524604400: # 2050-01-01 00:00:00
                                    self.gpssdict["utcdate"] = int(parts[9])
                                else:
                                    self.gpssdict["utcdate"] = 0                                    
                                print(f" Part 9 Date   = {parts[9]}")
                                
                            """ Get Latitude """    
                            if (parts[3]):
                                print(f" Part 3 Lat    = {parts[3]}")
                                if (float(parts[3]) > 0):
                                    self.gpssdict["lattitude"] = float(parts[3])
                                else:
                                    self.gpssdict["lattitude"] = 0.0
                                self.gpssdict["latdegrees"] = self.__convertToDegree(self.gpssdict["lattitude"])    
                                print(f" Part 3 Lat    = {self.gpssdict["lattitude"]}")
                                print(f" Part 3 Lat    = {self.gpssdict["latdegrees"]}")
                                
                            """ Get Latitude Northing """    
                            if (parts[4]):
                                print(f" Part 4 NS     = {parts[4]}")
                                self.gpssdict["NS"]    = parts[4]
                                print(f" Part 4 NS     = {self.gpssdict["NS"]}")
                                
                            """ Get Longitude """    
                            if (parts[5]):
                                print(f" Part 5 Lon    = {parts[5]}")
                                if 0.0 <= float(parts[5]) <= 10000.0: 
                                    self.gpssdict["longitude"] = float(parts[5])
                                else:
                                    self.gpssdict["longitude"] = 0.0
                                self.gpssdict["longdegrees"] = self.__convertToDegree(self.gpssdict["longitude"])    
                                print(f" Part 5 Lon    = {self.gpssdict["longitude"]}")
                                print(f" Part 5 Lon    = {self.gpssdict["longdegrees"]}")
                                    
                            """ Get Longitude Easting """    
                            if (parts[6]):
                                print(f" Part 6 EW     = {parts[6]}")
                                self.gpssdict["EW"]    = parts[6]
                                print(f" Part 6 EW     = {self.gpssdict["EW"]}")
                                
                            """ Get Speed in Knots """    
                            if (parts[7]):
                                print(f" Part 8 Knots  = {parts[7]}")
                                if 0.0 <= float(parts[7]) <= 10000.0:
                                    self.gpssdict["knots"] = float(parts[8])
                                else:
                                    self.gpssdict["knots"] = 0.0                                    
                                print(f" Part 8 Knots  = {self.gpssdict["knots"]}")    
                                    
                                    
                            """ Get Heading """    
                            if (parts[10]):
                                print(f" Part 10 Head  = {parts[10]}")                            
                                if 0.0 <= float(parts[10]) <= 10000.0:
                                    self.gpssdict["heading"] = float(parts[10])
                                else:
                                    self.gpssdict["heading"] = 0.0
                                print(f" Part 10 Head  = {parts[10]}")                                    
                                    
                        """ End $GPRMC Info """                            
        
                """" End of Try """
            
                """ Ensure only Valid Data """
            except:
                  pass

            self.gpssdict["timestamp"] = time.time()
            self.gpssdict["timestampdif"] = time.time() - (timeout - 8)
            print(self.gpssdict)
            """ Sleep before the next attempt """
            time.sleep(0.5)        
                
            if (time.time() > timeout):
                self.TIMEOUT = True
                break
            utime.sleep_ms(500)

        """ End of While True"""
            
    """ Convert Raw Degrees """
    def __convertToDegree(RawDegrees):

        RawAsFloat = float(RawDegrees)
        firstdigits = int(RawAsFloat/100) 
        nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
        Converted = float(firstdigits + nexttwodigits/60.0)
        Converted = '{0:.6f}'.format(Converted) 
        return str(Converted)
        
if __name__ == "__main__":
    eg = Ears_GPS()
    print("Class Testing by running directly\n")
    eg.getGPS()
