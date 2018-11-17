import os
import sys
import sqlite3
import numpy as np
import rpy2 

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None



def select_prova(conn,channel):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT IOV_SINCE,IOV_UNTIL,HVOUT1,HVOUT2  from CONDBR2_F0003_IOVS where CHANNEL_ID=?",channel)
 
    rows = cur.fetchall()
#    runstatus = np.genfromtxt('collisiontime.txt', names=True, dtype=None)
#    for line in runstatus:
    for row in rows:
#    	    if row[0]>=line[0] and row[1]<=line[1] and line[2]=="ON":
                print(row)




	#DeltaT=(row[1]-row[0])/1000000000
        #print row[0],DeltaT



def main():
    database = "TILE_DCS_HV-May2017.sqlite"
    # create a database connection
    conn = create_connection(database)
#    runstatus = np.genfromtxt('collisiontime.txt',  dtype=None)
    	





    with conn:
        select_prova(conn,"1")
 
 
 
if __name__ == '__main__':
    main()


 




# struttura della TABLE:
# CREATE TABLE "CONDBR2_F0003_IOVS" ( "OBJECT_ID" UNSIGNEDINT ,"CHANNEL_ID" UNSIGNEDINT ,"IOV_SINCE" ULONGLONG ,"IOV_UNTIL" ULONGLONG ,"USER_TAG_ID" UNSIGNEDINT ,"SYS_INSTIME" TEXT ,"LASTMOD_DATE" TEXT ,"ORIGINAL_ID" UNSIGNEDINT ,"NEW_HEAD_ID" UNSIGNEDINT ,"HVOUT1" FLOAT ,"HVOUT2" FLOAT ,"HVOUT3" FLOAT ,"HVOUT4" FLOAT ,"HVOUT5" FLOAT ,"HVOUT6" FLOAT ,"HVOUT7" FLOAT ,"HVOUT8" FLOAT ,"HVOUT9" FLOAT ,"HVOUT10" FLOAT ,"HVOUT11" FLOAT ,"HVOUT12" FLOAT ,"HVOUT13" FLOAT ,"HVOUT14" FLOAT ,"HVOUT15" FLOAT ,"HVOUT16" FLOAT ,"HVOUT17" FLOAT ,"HVOUT18" FLOAT ,"HVOUT19" FLOAT ,"HVOUT20" FLOAT ,"HVOUT21" FLOAT ,"HVOUT22" FLOAT ,"HVOUT23" FLOAT ,"HVOUT24" FLOAT ,"HVOUT25" FLOAT ,"HVOUT26" FLOAT ,"HVOUT27" FLOAT ,"HVOUT28" FLOAT ,"HVOUT29" FLOAT ,"HVOUT30" FLOAT ,"HVOUT31" FLOAT ,"HVOUT32" FLOAT ,"HVOUT33" FLOAT ,"HVOUT34" FLOAT ,"HVOUT35" FLOAT ,"HVOUT36" FLOAT ,"HVOUT37" FLOAT ,"HVOUT38" FLOAT ,"HVOUT39" FLOAT ,"HVOUT40" FLOAT ,"HVOUT41" FLOAT ,"HVOUT42" FLOAT ,"HVOUT43" FLOAT ,"HVOUT44" FLOAT ,"HVOUT45" FLOAT ,"HVOUT46" FLOAT ,"HVOUT47" FLOAT ,"HVOUT48" FLOAT ,"TEMP1" FLOAT ,"TEMP2" FLOAT ,"TEMP3" FLOAT ,"TEMP4" FLOAT ,"TEMP5" FLOAT ,"TEMP6" FLOAT ,"TEMP7" FLOAT , PRIMARY KEY("OBJECT_ID"), FOREIGN KEY("CHANNEL_ID") REFERENCES CONDBR2_F0003_CHANNELS("CHANNEL_ID") );
