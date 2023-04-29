from flask import Flask, render_template, request, url_for, redirect
from flaskext.mysql import MySQL

app = Flask("GPA Calculator")
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'justafolk'
app.config['MYSQL_DATABASE_DB'] = 'gpa'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
class Course:
    def __init__(self, name, credits, faculty = "NONE", course_type="BSC"):
        self.name = name
        self.credits = credits
        self.faculty = faculty
        self.course_type = course_type


@app.route('/')
def mainapp():
    return render_template('index.html', title="Home")

@app.route('/semester/view', methods=['GET'])
def viewsemester():
    return render_template('semview.html', title="Home")
        
@app.route('/semester/view/courses', methods=['GET'])
def viewcourses():
    return render_template('courseview.html', title="Home")

@app.route('/semester/create')
def onboarding():
    return render_template('semesterform.html', title="Onboarding")

@app.route('/login')
def login():
    return render_template('login.html', title="Login")

@app.route('/signup')
def signup():
    return render_template('signup.html', title="Signup")

@app.route('/registeruser', methods=['POST'])
def registeruser():
    username =  request.form['username']  
    clgname  =  request.form['clgname']  
    misno    =  request.form['misno']  
    userbranch= request.form['userbranch']  
    useremail = request.form['useremail']  
    upass     =  request.form['pass']  
    sql = "INSERT INTO users (name, department, MIS, email, password, login_method) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(username, userbranch, misno, useremail, upass, "email")


    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

    return redirect('/')



@app.route('/course/create', methods=['GET', 'POST'])
def createcourse():
    return render_template('create_course.html', title="Create Course")

@app.route('/api/v1/createcourse', methods=['POST'])
def createcourseapi():
    name = request.form['name']
    credits = request.form['credits']
    faculty = request.form['faculty']
    course_type = request.form['course_type']
    new_course = course(name, credits, faculty, course_type)
    return redirect('/course/list')

@app.route('/course/list', methods=['GET'])
def course_list():
    if(request.method == 'GET'):
        print("GET")
        coursename = request.args.get('name')
        
    cursor =conn.cursor()
    cursor.execute("SELECT * from courses")
    data = cursor.fetchone()
    print((data.__dict__), "chaltay")
    course = [Course("BSCS", 3), Course("BSCss", 2), Course("sslSCS", 1)]

    return render_template('course_list.html', title="Course List", courses=course, coursename=coursename )


@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run( debug=True)    
