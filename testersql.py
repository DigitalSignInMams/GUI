import mysql.connector

mydb = mysql.connector.connect(
    host="mysql.wpi.edu",
    user="ctang5",
    password="CT@ng5",
    database="mams_siso",
  )
sql = mydb.cursor()
