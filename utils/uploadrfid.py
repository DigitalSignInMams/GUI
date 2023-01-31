import csv
import mysql.connector
from time import sleep

with open("utils/rfid.csv", newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    counter = 0

    #Connect to WPI MySQL
    connected = False 
    while not connected:
        try:
            mydb = mysql.connector.connect(
                host="mysql.wpi.edu",
                user="ctang5",
                password="CT@ng5",
                database="mams_siso",
            )
            sql = mydb.cursor(buffered=True)
            print("Connected to MySQL Database.")
            connected = True
        except:
            print("Not connected to WPI MySQL database. Trying again.")
            sleep(10)
            continue
    
    #Reset RFID Table in MySQL
    command = "DELETE FROM rfid;"
    sql.execute(command)
    mydb.commit()
    print("Reset RFID Table")

    #Read through rfid.csv
    for line in csvreader:
        if counter == 0:
            counter+=1
            continue
        id = int(line[0])
        rfid_uid = line[1]
        if id == "" or rfid_uid == "":
            continue
        fname = line[3]
        lname = line[2]
        command = f"INSERT INTO rfid VALUES({id}, \"{rfid_uid}\");"
        sql.execute(command)
        mydb.commit()
    
    print("All RFID entries updated")

        
    
        