#!C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Python 3.10

#!/usr/bin/env python3
import cgi
import sqlite3

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('student_database.db')
cursor = conn.cursor()

# Create the student_grades table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_grades (
        id INTEGER PRIMARY KEY,
        name TEXT,
        midterm_exam1 REAL,
        midterm_exam2 REAL,
        final_exam REAL
    )
''')

# Function to calculate the average score
def calculate_average(midterm_exam1, midterm_exam2, final_exam):
    return (midterm_exam1 + midterm_exam2 + 2 * final_exam) / 4

# Function to display all records in the HTML format
def display_records():
    cursor.execute('SELECT * FROM student_grades')
    students = cursor.fetchall()

    print('<h2>Student Grades</h2>')
    print('<table>')
    print('<tr><th>Name</th><th>Average Score</th><th>Action</th></tr>')
    for student in students:
        name, midterm_exam1, midterm_exam2, final_exam = student[1:]
        average_score = calculate_average(midterm_exam1, midterm_exam2, final_exam)

        print('<tr>')
        print(f'<td>{name}</td><td>{average_score:.2f}</td>')
        print(f'<td><a href="?action=delete&id={student[0]}">Delete</a></td>')
        print('</tr>')
    print('</table>')

# Function to insert a new record into the database
def insert_record(form):
    name = form.getvalue('fullname')
    midterm_exam1 = float(form.getvalue('midterm1'))
    midterm_exam2 = float(form.getvalue('midterm2'))
    final_exam = float(form.getvalue('finalexam'))

    average_score = calculate_average(midterm_exam1, midterm_exam2, final_exam)

    cursor.execute('INSERT INTO student_grades (name, midterm_exam1, midterm_exam2, final_exam) VALUES (?, ?, ?, ?)',
                   (name, midterm_exam1, midterm_exam2, final_exam))
    conn.commit()

    print('<p>Student record inserted successfully!</p>')

# Function to delete a record from the database
def delete_record(form):
    name = form.getvalue('fullname')
    cursor.execute('DELETE FROM student_grades WHERE name = ?', (name,))
    conn.commit()

    print('<p>Student record deleted successfully!</p>')

# Main CGI script
form = cgi.FieldStorage()

print('Content-type: text/html\n')

print('<!DOCTYPE html>')
print('<html lang="en">')
print('<head>')
print('    <meta charset="UTF-8">')
print('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
print('    <title>Student Records</title>')
print('    <style>')
print('        * {')
print('            margin: 0;')
print('            font-family: \'Roboto\', sans-serif;')
print('        }')
print('        h1, form {')
print('            text-align: center;')
print('            padding: 5px;')
print('        }')
print('        input, button {')
print('            padding: 3px;')
print('            margin: 5px;')
print('        }')
print('        button:hover {')
print('            cursor: pointer;')
print('        }')
print('    </style>')
print('</head>')
print('<body>')
print('    <br>')
print('    <h1>Enter a new record</h1>')
print('    <form action="#" method="post">')
print('        <label for="fullname">Full Name :</label>')
print('        <input type="text" name="fullname"><br>')
print('        <label for="midterm1">Midterm #1:</label>')
print('        <input type="text" name="midterm1"><br>')
print('        <label for="midterm2">Midterm #2:</label>')
print('        <input type="text" name="midterm2"><br>')
print('        <label for="finalexam">Final Exam:</label>')
print('        <input type="text" name="finalexam"><br>')
print('        <button type="submit">Save</button>')
print('        <button onclick="displayRecords()">Display the records</button>')
print('    </form>')
print('    <h1>Delete a record</h1>')
print('    <form action="#" method="post">')
print('        <label for="fullname">Full Name :</label>')
print('        <input type="text" name="fullname"><br>')
print('        <button type="submit">Delete</button>')
print('    </form>')

if 'fullname' in form:
    action = form.getvalue('action')
    if action == 'insert':
        insert_record(form)
    elif action == 'delete':
        delete_record(form)

display_records()

print('</body>')
print('</html>')

cursor.close()
conn.close()
