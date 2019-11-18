from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/instructor_courses')
def instructor_courses():
    db_path = '810.sqlite'
    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        return f'Error: cannot connect to database at {db_path}'
    else:
        sql = "select CWID,name,dept,Course, count(1) as Student from HW11_instructors join HW11_grades on Instructor_CWID=CWID group by name,Course"
        data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'students': students}
                for cwid, name, dept, course, students in db.execute(sql)]
        db.close()
        return render_template('repository.html', header='Stevens Repository',
                               table_title='Number of students by course and instructor', lists=data)


if __name__ == '__main__':
    app.run(debug=True)
