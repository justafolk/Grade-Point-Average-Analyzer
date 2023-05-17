from flask import Flask, render_template, request, url_for, redirect, session
from flaskext.mysql import MySQL
import datetime

app = Flask("GPA Calculator")
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'justafolk'
app.config['MYSQL_DATABASE_DB'] = 'gpa'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()

def greet():
    current_time = datetime.datetime.now().time()
    if current_time.hour < 12:
        print("Good Morning!")
    elif current_time.hour < 18:
        print("Good Afternoon!")
    else:
        print("Good Night!")

class Course:
    def __init__(self, name, credits, faculty = "NONE", course_type="BSC"):
        self.name = name
        self.credits = credits
        self.faculty = faculty
        self.course_type = course_type

def check_session():
    if 'username' not in session:
        return False

    return True

def create_schedule(courses, limit):
    courses = dict(sorted(courses.items(), key=lambda item: item[1], reverse=True))
    print(courses)

    schedule = [ [] for i in range(7) ]
    pointer = 0
    for i, j in courses.items():
        k = pointer
        while j > 0:
            schedule[k].append(i)
            j-=1
            k = (k+2)%7
        pointer += 1
    print(schedule)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/loginuser', methods=['POST'])
def loginuser():
    username = request.form['email']
    password = request.form['pass']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        session['username'] = username
        return redirect(url_for('mainapp'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/')
def mainapp():
    if not check_session():
        return redirect('/login')
    return redirect('/home')

@app.route('/semester/view', methods=['GET'])
def viewsemester():
    return render_template('semview.html', title="Home")
        
@app.route('/semester/view/courses', methods=['GET'])
def viewcourses():
    return render_template('courseview.html', title="Home")

@app.route('/semester/courses/create', methods=['GET'])
def createcourses():
    return render_template('createcourse.html', title="Home")

@app.route('/onboarding/')
def onboardings():
    return render_template('onboarding.html', title="Onboarding")

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
    sql = "INSERT INTO users (name, department, MIS, email, password, login_method, clgname) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(username, userbranch, misno, useremail, upass, "email", clgname)

    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

    return redirect('/')

@app.route('/api/v1/createcourse', methods=['POST'])
def createcourseapi():
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
    if not check_session():
        return redirect('/login')
    return render_template('home.html')

if __name__ == '__main__':
    app.run( debug=True)    
