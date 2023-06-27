from flask import Flask, render_template, request, url_for, redirect, session

from flaskext.mysql import MySQL
import datetime
import json


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

def calculateGrade(level, total, sum):

    a = total - sum
    if level == 2:
        if a < (20/100)*total:
            return 10
        elif a <= (27/100)*total:
            return 9
        elif a <= (38/100)*total:
            return 8
        elif a <= (45/100)*total:
            return 7
        elif a <= (52/100) *total:
            return 6
        elif a <= (60/100)*total:
            return 5
        else:
            return 4
    elif level == 1:
        if a < (23/100)*total:
            return 10
        elif a <= (30/100)*total:
            return 9
        elif a <= (41/100)*total:
            return 8
        elif a <= (48/100)*total:
            return 7
        elif a <= (54/100) *total:
            return 6
        elif a <= (62/100)*total:
            return 5
        else:
            return 4
    else:
        if a < (27/100)*total:
            return 10
        elif a <= (35/100)*total:
            return 9
        elif a <= (45/100)*total:
            return 8
        elif a <= (52/100)*total:
            return 7
        elif a <= (60/100) *total:
            return 6
        elif a <= (65/100)*total:
            return 5
        else:
            return 4


@app.route('/api/calculate/cgpa', methods=['GET','POST'])
def calculatecGPA():
    username = session['username']

    sql = "SELECT * FROM courses where username = '{}'".format(username)


    conn = mysql.connect()

    cursor = conn.cursor()
    conn.ping(reconnect=True)
    cursor.execute(sql)
    data = cursor.fetchall()

    num = 0
    den = 0
    for i in data:
        s = dict(json.loads(i[4]))
        d = 0
        for j in s.items():
            d += float(j[1])
        grade = calculateGrade(i[13], i[14], d)
        num += grade*int(i[2])
        den += int(i[2])
        print(grade)


    cursor = conn.cursor()
    sql = "SELECT * FROM old_course where username = '{}'".format(username)

    conn.ping(reconnect=True)
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        num += i[1]*i[2]
        den += int(i[1])

    if num == 0 or den == 0:
        return 0

    s = num/den
    return str(round(s,2))

@app.route('/api/calculate/gpa', methods=['GET','POST'])
def calculateGPA():
    username = session['username']

    sql = "SELECT * FROM courses where username = '{}'".format(username)


    conn = mysql.connect()
    cursor = conn.cursor()
    conn.ping(reconnect=True)
    cursor.execute(sql)
    data = cursor.fetchall()

    num = 0
    den = 0
    for i in data:
        s = dict(json.loads(i[4]))
        d = 0
        for j in s.items():
            d += float(j[1])
        grade = calculateGrade(i[13], i[14], d)
        num += grade*int(i[2])
        den += int(i[2])
        print(grade)

    if num == 0 or den == 0:
        return 0
    s = num/den
    return str(round(s,2))


@app.route('/api/marks/add', methods=['GET', 'POST'])
def addmarks():
    course_id, mark_id, marks = request.args.get('marks').split("_")

    sql = "select * from courses where username='{}' and id='{}'".format(session['username'], course_id)

    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()

    c = dict(json.loads(data[4]))
    print(mark_id)
    c[mark_id] = marks
    marks = json.dumps(c)
    print(marks)
    usname = session['username']
    sql = "update courses set marks_distribution='{}' where username='{}' and id='{}'".format(marks, usname, course_id)

    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print("DONE", calculateGPA())
    return calculateGPA()
    



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
        session['name'] = user[1]
        session['currentsem'] = user[10]

        print(user[10])
        return redirect(url_for('mainapp'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/semester/old/add')
def oldsem():
    return render_template('oldsem.html')

@app.route('/createoldSemester', methods=['POST'])
def addoldsem():

    semname = request.form['semname'] 

    course_count = request.form['countcourse']


    cursor = conn.cursor()

    sql = "select * from semesters where username='{}' and name='{}'".format(session['username'], semname)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()

    print("PROBLEM>>>???")
    if data :
        print(data)
        print(sql)
        return render_template('semesterform.html', error="Semester already exists")

    total_credits = 0
    print("PROBLEM")

    for i in range(1, int(course_count)+1):
        course_name = request.form['course'+str(i)]
        credits = request.form['credits'+str(i)]
        grade = request.form['grades'+str(i)]
        total_credits += int(credits)

        sql = "INSERT INTO old_course (username, course_name, credits, grade, semname ) VALUES ('{}','{}', '{}', '{}', '{}')".format( session['username'], course_name, credits, grade,  semname)
        cursor.execute(sql)
        conn.commit()




    sql = "INSERT INTO semesters (username, name, total_credits_enrolled) VALUES ('{}','{}', '{}')".format( session['username'], semname, total_credits)

    cursor.execute(sql)
    conn.commit()
    cursor.close()

    return redirect('/semester/view/courses')

def abbreviate_sentence(sentence):
    words = sentence.split()
    abbreviation = ''.join(word[0].upper() for word in words)
    return abbreviation

def create_schedule(courses, limit):
    courses = dict(sorted(courses.items(), key=lambda item: item[1], reverse=True))
    schedule = [ [] for i in range(7) ]
    pointer = 0
    flag = 0

    for i, j in courses.items():
        k = pointer%7
        while j > 0 and len(schedule[k]) <= limit:
            flag = 1
            schedule[k].append(i)
            j-=1
            k = (k+2)%7
            pointer += 1
    return schedule

di = {"MVCDE":5, "TOC":4, "DC":3, "BFE":3, "DSA":2, "SA":2, "MPT":3}
sdc = create_schedule(di, 4)



@app.route('/viewall')
def view_all():

    cursor = conn.cursor()
    sql = "select * from courses where username='{}'".format(session['username'])
    cursor.execute(sql)
    courses = cursor.fetchall()


    sql = "select * from semesters where username='{}'".format(session['username'])
    cursor.execute(sql)
    semesters = cursor.fetchall()

    sql = "select * from old_course where username='{}'".format(session['username'])
    cursor.execute(sql)
    old_courses = cursor.fetchall()

    return render_template('view_all.html', courses=courses, semesters=semesters, old_courses=old_courses)



@app.route('/')
def mainapp():
    if not check_session():
        return redirect('/login')
    return redirect('/home')

@app.route('/semester/view', methods=['GET'])
def viewsemester():

    cursor = conn.cursor()

    sql = "select * from semesters where username = '{}' and name = '{}'".format(session['username'], session['currentsem'])
    cursor.execute(sql)
    
    s = cursor.fetchone()
    if not s:
        return redirect("/semester/create") 
    
    sql = "select * from courses where semester = '{}' and username = '{}'".format(session['currentsem'], session['username'])
    cursor.execute(sql)
    courses = cursor.fetchall()


    return render_template('semview.html', sgpa=calculateGPA(), cgpa=calculatecGPA(), sem = s, courses = courses, semname=request.args.get('semname'), title="Home", session=session)
        
def calculateLevel(snr, frnd, own):
    a = (snr*30+frnd*10+own*60)

    print(a)
    if a > 7500:
        return 2
    elif a > 6500:
        return 1 
    else:
        return 0

@app.route('/semester/view/courses', methods=['GET'])
def viewcourses():
    sql = "select * from courses where username='{}' and semester='{}'".format(session['username'], request.args.get('semester'))
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    marks = []
    datas = []
    for i in range(len(data)):
        datas.append([i for i in data[i] ])
        datas[i][4] = dict(json.loads(data[i][4]))

        level = data[i][13]

        for j,k in datas[i][4].items():
            print(datas[i][4])
            temp = j
            datas[i][4][j] = float(k)

        datas[i][4][temp] = level
        
    print(type(data))

    return render_template('courseview.html', title="Home", session=session, data=datas, semester=request.args.get('semester'), marks=marks)

@app.route('/semester/courses/create', methods=['GET'])
def createcourses():
    return render_template('createcourse.html', title="Home", session=session, semester=request.args.get('semester'))

@app.route('/onboarding/')
def onboardings():
    return render_template('onboarding.html', title="Onboarding")

@app.route('/semester/create')
def onboarding():
    sql = "select * from semesters where username='{}'".format(session['username'])
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('semesterform.html', data = data)

@app.route('/createSemester', methods=['POST'])
def createSemester():
    semname = request.form['semname'] 
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    creaditsallowed = request.form['creaditsallowed']


    sql = "select * from semesters where username='{}' and name='{}'".format(session['username'], semname)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        return render_template('semesterform.html', error="Semester already exists")

    sql = "INSERT INTO semesters (username, name, duration, total_credits_enrolled) VALUES ('{}','{}', '{}', '{}')".format( session['username'], semname, startdate+ "="+ enddate, creaditsallowed)

    cursor = conn.cursor()
    cursor.execute(sql)

    sql = "update users set currentsem = '{}' where username = '{}'".format(semname, session['username'])

    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

    return redirect('/semester/view/courses')


@app.route('/createCourse', methods=['POST'])
def createCourse():
    coursename = request.form['coursename']
    credits = request.form['credits']
    faculty = request.form['faculty']
    course_type = request.form['coursetype']

    sql = "select * from courses where username='{}' and name='{}'".format(session['username'], coursename)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        return render_template('createcourse.html', error="Course already exists")

    mark1 = request.form['mark1']
    mark2 = request.form['mark2']
    mark3 = request.form['mark3']
    mark4 = request.form['mark4']
    tpt = int(mark1) + int(mark2) + int(mark3) + int(mark4)

    # encode all mark variables in a json string
    marks = json.dumps({
        "mark1": mark1,
        "mark2": mark2,
        "mark3": mark3,
        "mark4": mark4
    })

    semester = request.form['semester']
    
    seniors_advice = request.form['seniorsop']
    friends_advice = request.form['friendsop']
    experience = request.form['youop']

    level = calculateLevel(int(seniors_advice), int(friends_advice), int(experience))

    coursecode = request.form['coursecode']


    sql = "INSERT INTO courses (username, name, credits, faculty, marks_distribution, course_type, seniors_advice, friends_advice, experience, semester, coursecode, level, total_marks) VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format( session['username'], coursename, credits, faculty, marks, course_type, seniors_advice, friends_advice, experience, semester, coursecode, level, tpt)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

    return redirect('/semester/view/courses')


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


def create_schedule(courses, limit):
    courses = dict(sorted(courses.items(), key=lambda item: item[1], reverse=True))
    print(courses)

    schedule = [ [] for i in range(7) ]
    pointer = 0
    for i, j in courses.items():
        k = pointer
        credit = j
        while j > 0:
            schedule[k].append([i,credit])
            j-=1
            k = (k+2)%7
        pointer += 1
    print(schedule)

    return schedule

def scheduler():
    cursor = conn.cursor()
    sql = "select * from courses where username='{}' and semester='{}'".format(session['username'], session['currentsem'])
    cursor.execute(sql)

    courses = cursor.fetchall()
    ss = dict()

    for i in courses:
        sd = i[1].lower().replace("and", "")
        ss[abbreviate_sentence(sd)] = i[2]

    s = create_schedule(ss, 4)
    return s

from itertools import zip_longest


from datetime import datetime
@app.route('/home')
def home():
    print("SD",session['currentsem'])

    if not check_session() or len(session["currentsem"]) == 0:
        return redirect('/login')

    cursor = conn.cursor()
    sql = "select * from courses where username = '{}' and semester = '{}'".format(session['username'], session['currentsem'])
    cursor.execute(sql)
    courses = cursor.fetchall()


    current_date = datetime.now()

    day_of_week = current_date.weekday()

    print(scheduler())

    cgpa = calculatecGPA()
    sgpa = calculateGPA()

    print("PRINTING")
    schedule = [list(filter(None, row)) for row in zip_longest(*scheduler())]

    return render_template('home.html', courses = courses[0:4], schedule = schedule, day=day_of_week, cgpa = cgpa, sgpa = sgpa)

def calculateGPAhelp(gradesNcredits):
    grades = 0 
    for j, i in gradesNcredits.items():
        grades += i[0]*i[1]
    return grades 

def calculateGPAextra(gradesNcredits):
    grades = 0 
    credits = 0
    for j, i in gradesNcredits.items():
        grades += i[0]*i[1]
        credits += i[0]
    return grades /credits

def calculateCreditsRequired(gradesNcredits, target_gpa):
    credits_required = gradesNcredits.copy()
    total_creds = 0
    credits_required = {k:v for k,v in sorted(credits_required.items(), key=lambda item: item[1][-1])}
    for course, data in gradesNcredits.items():
        credits_required[course] = [credits_required[course][0], 10]
        total_creds += credits_required[course][0]

    tg = calculateGPAhelp(credits_required)
    target_gpa = target_gpa*total_creds
    while (tg > target_gpa):
        
        for course, data in credits_required.items():
            credits_required[course] = [credits_required[course][0], credits_required[course][1]-1]
            tg = calculateGPAhelp(credits_required)
            print(course)
            if (tg == target_gpa):
                return credits_required
            if (tg < target_gpa):
                credits_required[course] = [credits_required[course][0], credits_required[course][1]+1]
    
    return credits_required

def assignGrades(t):
    cursor = conn.cursor()
    for i,j in t.items():
        sql = "update courses set grades='{}' where name='{}' and username='{}'  ".format(j[1], i, session["username"], )
        cursor.execute(sql)

    conn.commit()
    pass


@app.route('/semester/create/goals', methods=["GET"])
def goalsCreate():
    cgpa = calculatecGPA()
    sgpa = calculateGPA()
    if not request.args.get("targetgpa"):
        return render_template("creategoals.html", cgpa=cgpa, sgpa=sgpa, getflag = 0)

    cursor = conn.cursor()
    sql = "select * from courses where username = '{}' and semester = '{}'".format(session['username'], session['currentsem'])
    cursor.execute(sql)
    courses = cursor.fetchall()

    Gradendstuff = dict()
    for i in courses:
        Gradendstuff[i[1]] = [i[2], i[13]]
    
    t = calculateCreditsRequired(Gradendstuff, float(request.args.get("targetgpa")))

    assignGrades(t)

    return render_template("creategoals.html", cgpa=cgpa, sgpa=sgpa, targets=t, expects = round(calculateGPAextra(t), 2), getflag = 1)



app.jinja_env.globals.update(abbreviate_sentence = abbreviate_sentence)
if __name__ == '__main__':
    app.run( debug=True)    

