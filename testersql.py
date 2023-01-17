import mysql.connector

mydb = mysql.connector.connect(
    host="mysql.wpi.edu",
    user="ctang5",
    password="CT@ng5",
    database="mams_siso",
  )
sql = mydb.cursor(buffered=True)

command = f"SELECT first_name, last_name FROM person WHERE student_id = get_id(43704390)"
sql.execute(command)
result = sql.fetchall()
print(result)