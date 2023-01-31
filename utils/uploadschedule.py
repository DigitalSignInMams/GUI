# for juniors
import mysql.connector
from time import sleep

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
        sleep(2)
        continue

command = "DELETE FROM schedule;"
sql.execute(command)
mydb.commit()
print("Reset Schedules Table")

START_TIME = '07:40'
END_TIME = '14:45'
TERMS = ['A', 'B', 'C', 'D']
WEEKDAYS = [1, 2, 3, 4, 5]
NUM_STUDENTS = 50

for id in range(1, NUM_STUDENTS+1):
    for term in TERMS:
        for weekday in WEEKDAYS:
            command = f"INSERT INTO schedule VALUES ({id}, \'{term}\', {weekday}, CONVERT(\"{START_TIME}\", TIME), CONVERT(\"{END_TIME}\", TIME))"
            sql.execute(command)

mydb.commit()

mydb.close()
print("Done inserting entries into schedule table!")