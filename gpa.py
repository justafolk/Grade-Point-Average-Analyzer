class Course:
    def __init__(self, name, credits, faculty, marks_distribution=0, seniors_advice = 0, friends_advice = 0, experience = 0, num_units = 0):
        self.name = name
        self.credits = credits
        self.faculty = faculty
        self.marks_distribution = marks_distribution
        self.seniors_advice = seniors_advice
        self.friends_advice = friends_advice
        self.experience = experience
        self.num_units = num_units


class Semester:
    def __init__(self, name, duration, total_credits):
        self.name = name
        self.duration = duration
        self.total_credits = total_credits
        self.courses = dict()

    def addcourse(self, course, credits):
        self.courses[course.name] = credits
    
    def removecourse(self, course):
        self.courses.pop(course.name)
    


class User:
    def __init__(self, name, current_year, department, MIS, birthday=None, login_method=None):
        self.name = name
        self.current_year = current_year
        self.department = department
        self.MIS = MIS
        self.birthday = birthday
        self.login_method = login_method
        self.semesters = set()
    
    def addsemester(self, semester):

        self.semesters.insert(semester)
    
    def rmsemester(self, semester):
        self.semesters.pop(semester)
    


class Analyzer:
    def __init__(self, generosity):
        self.generosity = generosity

    def average_grades(self):
        # calculates the average grades based on the advices and experience
        grades = self.generosity 
        return grades

    def assign_grades(self, totalmarks):
        # assigns grades based on the calculated average grades

        # generosity ranges from 1 to 10, 1 being not generous and 10 being generous
        # totalmarks ranges from 0 to 100
        # create a if / switch case logic to assign grades based on the generosity
        marks = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

        if self.generosity == 1:
            if totalmarks > 60:
                return 'AA'
            elif totalmarks > 50:
                return 'AB'
            elif totalmarks > 40:


            pass
        elif self.generosity == 2:


        pass

    def plot_grades(self):
        # plots the grades of each subject
        pass

    def plot_growth(self):
        # plots the growth throughout semesters
        pass

    def plot_credit_distribution(self):
        # plots a pie chart for credit distribution
        pass

    def plot_goal_met(self):
        # plots a graph showing if goals are met
        pass

    def assign_goals(self):
        # auto assigns goals for each subject with respect to given gpa goals
        pass
