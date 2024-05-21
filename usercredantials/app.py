from flask import Flask, request, render_template, redirect, url_for
from flask_restx import Api, Resource, fields
import mysql.connector
import webbrowser
from threading import Timer

app = Flask(__name__)
api= Api(app,doc='/swagger/')

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Svraki@321",  # Your MySQL password
        database="task"  # Your database name
    )
    return conn

def create_table():
    conn = get_db_connection()
    cObj = conn.cursor()
    create_script = '''CREATE TABLE IF NOT EXISTS employee (id int PRIMARY KEY,name varchar(40) NOT NULL,address varchar(100))'''
    cObj.execute(create_script)
    conn.commit()
    cObj.close()
    conn.close()

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('data.html', records=records)

@app.route('/submit', methods=['POST'])
def submit():
    id = request.form['id']
    name = request.form['name']
    address = request.form['address']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employee (id, name, address) VALUES (%s, %s, %s)", (id, name, address))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('data'))

@app.route('/data')
def data():
    conn = get_db_connection()
    cObj = conn.cursor()
    cObj.execute("SELECT * FROM employee")
    records = cObj.fetchall()
    cObj.close()
    conn.close()
    return render_template('data.html', records=records)

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    address = request.form['address']
    conn = get_db_connection()
    cObj = conn.cursor()
    cObj.execute("UPDATE employee SET name = %s, address = %s WHERE id = %s", (name, address, id))
    conn.commit()
    cObj.close()
    conn.close()
    return redirect(url_for('data'))

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    conn = get_db_connection()
    cObj = conn.cursor()
    cObj.execute("DELETE FROM employee WHERE id = %s", (id,))
    conn.commit()
    cObj.close()
    conn.close()
    return redirect(url_for('data'))

ns = api.namespace('employee', description='Employee operations')

#Define the API namespace
ns = api.namespace('employees', description='Operations related to employees')

# Model
employee_model = ns.model('Employee', {
    'id': fields.Integer(required=True, description='The employee ID'),
    'name': fields.String(required=True, description='The employee name'),
    'address': fields.String(required=True, description='The employee address')
})

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Svraki@321",
        database="task"
    )

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INT PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            address VARCHAR(100)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@ns.route('/')
class EmployeeList(Resource):
    @ns.doc('list_employees')
    @ns.marshal_list_with(employee_model)
    def get(self):
        """List all employees"""
        conn = get_db_connection()
        cObj = conn.cursor()
        cObj.execute("SELECT id, name, address FROM employee")
        employees = cObj.fetchall()
        cObj.close()
        conn.close()
        return [{'id': emp[0], 'name': emp[1], 'address': emp[2]} for emp in employees]


    @ns.expect(employee_model)
    @ns.marshal_with(employee_model, code=201)
    @ns.doc('create_employee')
    def post(self):
        print("Creating an employee")
        conn = get_db_connection()
        cursor = conn.cursor()
        data = api.payload
        cursor.execute("INSERT INTO employee (id, name, address) VALUES (%s, %s, %s)",
                       (data['id'], data['name'], data['address']))
        conn.commit()
        cursor.close()
        conn.close()
        return data, 201

@ns.route('/<int:id>')
@ns.response(404, 'Employee not found')
@ns.param('id', 'The employee identifier')
class Employee(Resource):
    @ns.doc('get_employee')
    @ns.marshal_with(employee_model)
    def get(self, id):
        """Fetch an employee given its identifier"""
        conn = get_db_connection()
        cObj = conn.cursor()
        cObj.execute("SELECT id, name, address FROM employee WHERE id = %s", (id,))
        emp = cObj.fetchone()
        cObj.close()
        conn.close()
        if emp is not None:
            return {'id': emp[0], 'name': emp[1], 'address': emp[2]}
        api.abort(404)
            
    @ns.expect(employee_model)
    @ns.doc('update_employee')
    def put(self, id):
        print(f"Updating employee with ID: {id}") 
        conn = get_db_connection()
        cursor = conn.cursor()
        data = api.payload
        cursor.execute("UPDATE employee SET name = %s, address = %s WHERE id = %s",
                       (data['name'], data['address'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return data

    @ns.doc('delete_employee')
    def delete(self, id):
        print(f"Deleting employee with ID: {id}") 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'Employee deleted successfully'}, 204


create_table()
def open_browser():
    webbrowser.open_new('http://127.0.01:5000/data')
if __name__ == '__main__':
    Timer(1,open_browser).start()
    app.run(debug=True)

