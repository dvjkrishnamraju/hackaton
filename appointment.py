from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="DVv12345@",
            database="APPOINTMENTS"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route("/")
def homepage():
    return render_template("appointment.html")

@app.route("/submit", methods=["POST"])
def submit_appointment():
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    appointment_purpose = request.form["appointment_purpose"]

    connection = create_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS APPOINTMENTS (
        id INT AUTO_INCREMENT PRIMARY KEY,
        appointment_date DATE NOT NULL,
        appointment_time TIME NOT NULL,
        appointment_purpose TEXT NOT NULL
    )"""
    
    cursor.execute(create_table_query)

    insert_query = """
    INSERT INTO APPOINTMENTS (appointment_date, appointment_time, appointment_purpose) 
    VALUES (%s, %s, %s)
    """
    
    cursor.execute(insert_query, (appointment_date, appointment_time, appointment_purpose))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for("view_appointments"))  # Redirect to view_appointments route

@app.route("/appointments")
def view_appointments():
    connection = create_connection()
    cursor = connection.cursor()
    
    select_query = "SELECT appointment_date, appointment_time, appointment_purpose FROM APPOINTMENTS"
    cursor.execute(select_query)
    appointments = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template("view_appointments.html", APPOINTMENTS=appointments)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
