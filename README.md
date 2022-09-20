# TutoringTracker
(EOP)
This webapp is used to manage the amount of hours students aquire during tutoring.
###### Technologies used include:
- **Postgresql** hosted using **AWS** relational database. 
- **Django** for back-end development
- **HTMX** for AJAX requests
- **HTML, CSS, BootStrap** for front-end development
- **Heroku, git** for deployment

## Login Page
Logging in grants access to other pages
![image](https://user-images.githubusercontent.com/96543196/191287879-15cd3cf5-a1d4-4fe2-a999-03004957af34.png)

## Sessions
- The session page consists of a single input field. The Input field filters inputs and returns an error message if needed.
- Error messages are returned if the input is empty, student does not exist or if the student is already in the session.
- A student can be deleted if added on accident or can be signed out when they are ready to leave
- When the tutoring session ends, the end session button can be clicked to save the hours of all students in the current session.
![sessionpage](https://user-images.githubusercontent.com/96543196/191295903-b1049c23-f1f9-447e-9fae-9fe3332d8ad5.gif)

## Students
- The students page contains a list of all the students
- At the top of the page are two buttons info and Export
- The info button gives more information on how to use this page
- The Export button Exports the students hours to a csv or Text file
- When a students name is clicked you can add extra hours to their total
![studentspage](https://user-images.githubusercontent.com/96543196/191295069-4feb4af3-76ab-499a-a022-4767da5e6baf.gif)





