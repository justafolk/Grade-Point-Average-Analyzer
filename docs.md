
Certainly! Here's the documentation for each function in the provided code:

greet() function:

Description: Prints a greeting based on the current time of day (Good Morning, Good Afternoon, or Good Night).
Parameters: None.
Returns: None.
check_session() function:

Description: Checks if the 'username' key is present in the session dictionary to determine if the user is logged in.
Parameters: None.
Returns: Boolean value indicating whether the user is logged in (True) or not (False).
calculateGrade(level, total, sum) function:

Description: Calculates the grade based on the level of the course, total marks, and the sum of obtained marks.
Parameters:
level: Integer value representing the level of the course (1, 2, or 3).
total: Total marks for the course.
sum: Sum of obtained marks for the course.
Returns: Grade value as an integer.
calculatecGPA() function:

Description: Calculates the cumulative GPA (cGPA) for the user based on their courses and marks.
Parameters: None.
Returns: String representation of the calculated cGPA rounded to two decimal places.
calculateGPA() function:

Description: Calculates the GPA (Grade Point Average) for the user's current semester based on their courses and marks.
Parameters: None.
Returns: String representation of the calculated GPA rounded to two decimal places.
addmarks() function:

Description: Updates the marks distribution for a specific course based on the provided marks.
Parameters: None.
Returns: String representation of the calculated GPA rounded to two decimal places.
logout() function:

Description: Logs out the user by removing the 'username' key from the session dictionary.
Parameters: None.
Returns: Redirects the user to the '/login' page.
loginuser() function:

Description: Authenticates the user by checking their credentials against the database.
Parameters: None.
Returns: Redirects the user to the '/mainapp' page if the credentials are valid. Otherwise, renders the 'login.html' template with an error message.
oldsem() function:

Description: Renders the 'oldsem.html' template for adding old semester information.
Parameters: None.
Returns: Rendered template 'oldsem.html'.
addoldsem() function:

Description: Adds the information of an old semester to the database.
Parameters: None.
Returns: Redirects the user to '/semester/view/courses'.
abbreviate_sentence(sentence) function:

Description: Abbreviates a sentence by taking the first letter of each word and capitalizing it.
Parameters:
sentence: String representing the input sentence.
Returns: Abbreviated string.
create_schedule(courses, limit) function:

Description: Creates a schedule by distributing courses evenly across days of the week, considering a limit on the number of courses per day.
Parameters:
courses: Dictionary containing course names as keys and their priority as values.
limit: Maximum number of courses allowed per day.
Returns: List of lists representing the course schedule for each day of the week.