# ===== Importing external modules ===========
import datetime
from datetime import date

# =========== I am defining classes & functions here =============


class User:
    '''
    The User class has a username and password
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_password(self):
        return self.password

    def get_username(self):
        return self.username


class Task:
    '''
    The Task class has a username, task title & description, assignment and due
    dates, as well as a yes/no status indication completion.
    '''
    def __init__(self, user, title, description, date_assigned, date_due
                ,status):
        self.user = user
        self.title = title
        self.description = description
        self.date_assigned = date_assigned
        self.date_due = date_due
        self.status = status

    def __str__(self):
        return("{}, {}, {}, {}, {}, {}".format(self.user, self.title,
                                            self.description,
                                            self.date_assigned,
                                            self.date_due, self.status))

    def summary(self):
        '''
        Returns a summary of the tasks information in a tabular form. The first
        column has the labels (user, task title, etc), and the second column
        corresponding information.
        '''
        width = 13 #using the length of the longest label, 'Date assigned', to
        #put a vertical bar between the 2 columns at a consistent position.

        print(f"Task: {" "*(width-len("Task"))} | "
            f"{self.title.replace("\n","")}\n"
            f"Assigned to: {" "*(width-len("Assigned to"))} | "
            f"{self.user.replace("\n","")}\n"
            f"Date assigned: {" "*(width-len("Date assigned"))} |"
            f" {self.date_assigned.replace("\n","")}\n"
            f"Due date: {" "*(width-len("Due date"))} | "
            f"{self.date_due.replace("\n","")}\n"
            f"Task complete? {" "*(width-len("Task complete"))} | "
            f"{self.status.replace("\n","")}\nTask description:\n"
            f"{self.description.replace("\n","")}\n")

    #for use when updating assigned users in the view_mine function
    def update_username(self, new_username):
        self.user = new_username


def dateinput():
    '''
    Helper function for ensuring validity of inputted dates, and logical
    consistency between starting and due dates within Task objects. Prompts
    for input from user to build starting and due dates, and if both are valid
    returns them in string form for use in building and amending task objects.
    '''
    date_assigned = ""
    date_due = ""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", \
            "Oct", "Nov", "Dec"]

    #if inputs are invalid for creating dates, or the start date is after the
    #due date, keep looping until valid.
    while True:
        '''
        start_year = input("start year: ")
        start_month = input("start month: ")
        start_day = input("start day: ")
        '''

        due_year = input("due year: ")
        due_month = input("due month: ")
        due_day = input("due day: ")
        try:
            #run exception and ask for input again if input invalid
            start_date = date.today()
            due_date = datetime.date(int(due_year), int(due_month), \
                                    int(due_day))

            #check for whether dates are logical or not
            if start_date > due_date:
                print("Error: due date cannot be before start date. ")

            #building date strings according to format in Task object
            else:
                for month in months:
                    if months.index(month)+1 == start_date.month:
                        date_assigned = "{} {} {}".format(start_date.day, \
                                                    month, start_date.year)

                    if months.index(month)+1 == int(due_month):
                        date_due = "{} {} {}".format(due_day, month, due_year)
                break
        except:
            print("Invalid input provided, please try again.")
    return [date_assigned, date_due]


def equals(task1, task2):
    '''
    Helper function to test if two tasks are completely identical
    '''
    if task1.user == task2.user and task1.title == task2.title and \
    task1.description == task2.description and task1.date_assigned == \
    task2.date_assigned and task1.date_due == task2.date_due and \
    task1.status == task2.status:
        return True
    else:
        return False


def read_data(users_list, tasks_list):
    '''
    given 2 empty user and task lists, open the user and tasks text files and
    read them to the lists for use in the functions that follow. Entries in the
    lists are stored as User and Task objects respectively.
    '''

    try:
        with open("./user.txt", "r") as file:
            for i in file:
                i = i.strip("\n")  #remove any lingering newlines
                i = i.split(", ")  #username and password in the file are
                #separated by a comma followed by a blank space
                users_list.append(User(i[0], i[1]))
    except:
        pass

    with open("./tasks.txt", "r") as file:
            entries_list = []  #each line in the file is fed into this first
            for line in file:
                line = line.strip("\n")
                entries_list.append(line.split(", "))

            for i in range(0, len(entries_list)):  #each task has 6 data points
                #to be added to each Task object
                tasks_list.append(Task(entries_list[i][0],
                entries_list[i][1],
                entries_list[i][2],
                entries_list[i][3],
                entries_list[i][4],
                entries_list[i][5]))


def reg_user(username, password, users_list):
    '''
    Given a new user's details, add them to the user text file and create a
    User object for them as well to be added to the users list. Includes a
    check for whether their username and password are already taken as well as
    password confirmation.
    '''
    try:
        with open("./user.txt", "a") as file:
            for user in users_list:
                while user.get_username() == username:
                    username = input("This username is already taken, "
                                    "try entering another one: ")

            for user in users_list:
                while user.get_password() == password:
                    password = input("This password is already taken, "
                                    "try entering another one: ")
                    confirm = input("Please confirm the password: ")
                    while confirm != password:
                        confirm = input("Passwords don't match, "
                                        "please confirm again: ")

            file.write("\n" + username + ", " + password) #add new user to file
            users_list.append(User(username, password)) #create User object and
            #add to users list for future use
    except:
        print("Error: User text file not found.\n")


def add_task(username, title, description, date_assigned, date_due, status,
            tasks_list):
    '''
    Given task info provided by the user, add the task to the file and create
    a corresponding Task object to be added to the tasks list
    '''
    task = [username, title, description, date_assigned, date_due, status]
    try:
        with open("./tasks.txt", "w") as file:
            tasks_list.append(Task(username, title, description, date_assigned,
                            date_due, status))
            for task in tasks_list:
                file.write("{}\n".format(task))
    except:
        return("Error: Tasks text file not found.\n")


'''
Breaking the editing component of the view_mine function into its own function.
This is to help with modularity.
'''
def new_due_date(my_task):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", \
            "Oct", "Nov", "Dec"]
    while True:
        due_year = input("due year: ")
        due_month = input("due month: ")
        due_day = input("due day: ")
        try:
            new_due_date = datetime.date(int(due_year), int(due_month), \
                                        int(due_day))
            if new_due_date >= date.today():
                for month in months:
                    if int(due_month) == months.index(month)+1:
                        return "{} {} {}".format(due_day, month, due_year)
            else:
                print("New due date must be at least today or later.")
                continue
        except:
            print("Invalid inputs.")


def edit_my_task(my_task, users_list, tasks_list):
    '''
    Helper function for view_mine. Gives user prompts to change the assigned
    user and due date, provided the task is marked as incomplete.
    '''
    if my_task.status.lower() == "no":
        selection = ""
        while selection != "-1":
            selection = input("Enter 1 to reassign the task to someone else."
                            " Enter 2 to change the due date. Enter -1 to go"
                            " back: ")
            if selection == "1":
                '''
                Reassigning to another user. Displays the users in the user
                list, asks for the username to assign to, and updates the list.
                '''
                for user in users_list:
                    print("{}: {}".format(users_list.index(user)+1, \
                                    user.get_username()))

                new_username = input("Enter the username of the person you"
                                    "want to reassign the task to: ")
                present = ""
                while present != "1":

                    for user in users_list: #check to see if input valid
                        if user.get_username() == new_username:
                            present = "1"
                            break

                    if present == "1": #updating the task
                        for task in tasks_list:
                            if equals(task, my_task):
                                task.update_username(new_username)
                                task.summary()

                    else:
                        new_username = input("Invalid input, please enter a"
                                            " username from the list: ")

            elif selection == "2":
                print("Task: {} is due on {}".format(my_task.title, \
                                                my_task.date_due))
                if my_task.status.lower() == "no":
                    my_task.date_due = new_due_date(my_task)
                    task.summary()

            elif selection == "-1":
                continue

            else:
                selection = input("Invalid selection, please try again: ")
    else:
        print("Task is already marked as complete.")


def update_my_tasks(my_tasks, tasks_list):
    '''
    Helper function for view_mine. After tasks have been edited,
    used to write changes made in the view_mine function to the tasks file.
    '''
    try:
        with open("./tasks.txt", "w") as file:
            #looking for the corresponding task in the main tasks list, and
            #replacing it with the updated Task object
            for task in tasks_list:
                for my_task in my_tasks:
                    if task.title == my_task.title and task.description \
                    == my_task.description and task.date_assigned == \
                    my_task.date_assigned:
                        tasks_list[tasks_list.index(task)] = my_task

            for task in tasks_list:  #rewriting file to include updates
                file.write("{}\n".format(task))
    except:
        print("An error occurred. Could not write changes to file")


def view_mine(users_list, tasks_list, user):
    '''
    For a given user, print out their tasks with the use of the Task.summary()
    method.
    '''
    i = 0  #logs the number of tasks for the user, if zero at the end of the
    #iteration it will allow us to return a message that they have no tasks
    my_tasks = []
    for task in tasks_list:
        if task.user == user.get_username():  #check if a task matches the user
            i += 1
    print("{} tasks found for {}.\n".format(i, user.get_username()))

    i = 0  #reusing this variable to log each individual task for the user
    for task in tasks_list:
        if task.user == user.get_username():
            i += 1
            print("Assigned to {}: task {}\n".format(user.get_username(), i))
            task.summary()
            my_tasks.append(task)
    if i == 0:
        print("No tasks found for {}.".format(user.get_username()))

    if i != 0:
        select = ""
        while select != "-1":
            select = input("Enter the number of the task you wish to update,"
                        " or enter -1 to return to the main menu.")
            try:
                int(select)
                if int(select) == -1:
                    break
                elif int(select) >= 1 and int(select) <= len(my_tasks):
                    print("Task {}: {}".format(select, \
                        my_tasks[int(select)-1].title))

                    if my_tasks[int(select)-1].status.lower() == "no":
                        print("Task is not complete.")
                    else:
                        print("Task is complete.")

                    print("The task is assigned to {}." \
                        .format(my_tasks[int(select)-1].user))
                    print("The task is due on {}." \
                        .format(my_tasks[int(select)-1].date_due))

                    option = ""
                    while option != "0":
                        option = input("Enter 1 if you want to update the "
                                "completion status of the task, 2 if you want"
                                " to change the assigned user or due date. "
                                "If you do not want to make further"
                                " changes, enter 0: ")
                        if option == "0":
                            break

                        elif option == "1":
                            if my_tasks[int(select)-1].status.lower() == "yes":
                                my_tasks[int(select)-1].status = "No"
                            else:
                                my_tasks[int(select)-1].status = "Yes"
                            my_tasks[int(select)-1].summary()

                        elif option == "2":
                            edit_my_task(my_tasks[int(select)-1], users_list, \
                                        tasks_list)
                            my_tasks[int(select)-1].summary()

                    for task in my_tasks:
                        task.summary()
                else:
                    print("Selection out of range.\n")
            except:
                print("Invalid input selected.\n")

    update_my_tasks(my_tasks, tasks_list)


def view_all():
    '''
    Summarize all tasks in the file using Task.summary(). It does this by
    creating task objects on the fly but I could implement this using the tasks
    list as well.
    '''
    try:
        with open("./tasks.txt", "r") as file:
            for line in file:
                line = line.split(", ")
                Task(line[0], line[1], line[2], line[3], line[4], line[5]) \
                .summary()
    except:
        print("Error: Tasks file not found.")


def view_completed(tasks_list, user):
    '''
    Admin-only function that summarizes all tasks using Task.summary(), but
    only those that are completed (i.e. status variable set to "Yes")
    '''
    if user.get_username() == "admin":
        for task in tasks_list:
            if task.status.lower() == "yes":
                task.summary()
    else:
        print("You do not have admin-level access.")


def delete(tasks_list, user):
    '''
    Admin-only function that displays the titles of all tasks on file with a
    number. The admin can then enter the desired number to delete the task. It
    is removed from the list of Task objects as well as the tasks text file
    '''
    if user.get_username() == "admin":
        try:
            with open("./tasks.txt", "w") as file:
                print("Current tasks on file:\n")
                #print the number of each task on file, plus their titles
                for task in tasks_list:
                    print("{}: {}".format(tasks_list.index(task)+1, task.title))

                delete = ""
                #take the number as an input. If it matches a task on file,
                #delete the task. Invalid input will prompt another input, 0 to
                #quit.
                while delete != "0" and len(tasks_list) != 0:
                    delete = input("Enter the number of the task which you"
                                " would like to delete. Enter 0 to exit: ")
                    try:
                        int(delete)
                        if delete == "0":
                            break

                        #removing the Task from the list, and printing the
                        #remaining tasks with updated numbers
                        elif delete != "0" and int(delete) <= len(tasks_list):
                            del tasks_list[int(delete)-1]
                            print("\nCurrent tasks on file:\n")
                            for task in tasks_list:
                                print("{}: {}".format(tasks_list.index(task)+1,\
                                                task.title))

                        elif delete != "0" and int(delete) > len(tasks_list):
                            print("Input out of range. Try again.")
                    except:
                        print("Invalid input.")

                if len(tasks_list) == 0:
                    print("No more tasks remaining on file.\n")

                #rewriting the tasks text file to exclude the deleted tasks
                for task in tasks_list:
                    file.write(f"{task}\n")
        except:
            print("Error: tasks file not found.")
    else:
        print("You do not have admin-level access.")


'''
Additional sub-functions to be used in the display statistics and generate
reports functions at the tasks level
'''
def check_if_overdue(task):
    '''
    Helper function to simplify the overdue functions. Returns 1
    if a given task is overdue on today's date, 0 otherwise.
    '''
    due_list = task.date_due.split(" ")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", \
            "Oct", "Nov", "Dec"]
    date_today = date.today()

    for month in months:
        if month == due_list[1]:
            due_date = datetime.date(int(due_list[2]), months.index(month)+1, \
                                    int(due_list[0]))

    if date_today > due_date and task.status.lower() == "no":
        return 1
    else:
        return 0


def total_tasks(tasks_list):
    total = len(tasks_list)
    return "{} tasks are currently being managed by the task manager." \
            .format(total)


def total_completed_tasks(tasks_list):
    total_completed = 0
    for task in tasks_list:
        if task.status.lower() == "yes":
            total_completed += 1

    return "{} tasks have been marked as complete".format(total_completed)


def total_incomplete_tasks(tasks_list):
    total_incomplete = 0
    for task in tasks_list:
        if task.status.lower() == "no":
            total_incomplete += 1

    return "{} tasks are currently incomplete".format(total_incomplete)


def total_overdue_tasks(tasks_list):
    total_overdue = 0
    for task in tasks_list:
        if check_if_overdue(task) == 1:
            total_overdue += 1

    return "{} tasks are currently overdue".format(total_overdue)


def percent_incomplete(tasks_list):
    total_incomplete = 0
    total = 0
    for task in tasks_list:
        if task.status.lower() == "no":
            total_incomplete += 1
            total += 1
        elif task.status.lower() == "yes":
            total += 1

    percentage = round((total_incomplete/total)*100, 2)
    return "{}{} of all tasks are incomplete".format(percentage, "%")


def percent_overdue(tasks_list):
    total_overdue = 0
    total = 0
    for task in tasks_list:
        if check_if_overdue(task) == 1:
            total_overdue += 1
            total += 1
        elif check_if_overdue(task) == 0:
            total += 1

    percentage = round((total_overdue/total)*100, 2)
    return "{}{} of all tasks are overdue".format(percentage, "%")


'''
Additional sub-functions to be used in the display statistics and generate
reports functions at the user level
'''
def user_total_tasks(user, tasks_list):
    i = 0
    for task in tasks_list:
        if task.user == user.get_username():
            i += 1
    return "User {} has {} tasks.".format(user.get_username(), i)


def user_percent_tasks(user, tasks_list):
    i = 0
    for task in tasks_list:
        if task.user == user.get_username():
            i += 1
    percentage = round((i/len(tasks_list))*100, 2)
    return "{}{} of the tasks belong to {}".format(percentage, "%", \
                                                user.get_username())


def user_percent_completed(user, tasks_list):
    i = 0
    tally = 0
    for task in tasks_list:
        if task.user == user.get_username() and task.status.lower() == "yes":
            i += 1
            tally += 1
        elif task.user == user.get_username() and task.status.lower() == "no":
            tally += 1

    try:  #to prevent a divide by zero error if the user has no tasks
        percentage = round((i/tally)*100, 2)
        return "{}{} of tasks assigned to {} are complete".format(percentage, \
                                                    "%", user.get_username())
    except:  #None will be removed when the info is written to file
        return None


def user_percent_incomplete(user, tasks_list):
    i = 0
    tally = 0
    for task in tasks_list:
        if task.user == user.get_username() and task.status.lower() == "no":
            i += 1
            tally += 1
        elif task.user == user.get_username() and task.status.lower() == "yes":
            tally += 1

    try: #to prevent a divide by zero error if the user has no tasks
        percentage = round((i/tally)*100, 2)
        return "{}{} of tasks assigned to {} are not complete" \
                .format(percentage, "%", user.get_username())

    except:
        return None


def check_if_overdue(task):
    '''
    Helper function to simplify the user_percent_overdue function. Returns 1
    if a given task is overdue on today's date, 0 otherwise.
    '''
    due_list = task.date_due.split(" ")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", \
            "Oct", "Nov", "Dec"]
    date_today = date.today()

    for month in months:
        if month == due_list[1]:
            due_date = datetime.date(int(due_list[2]), months.index(month)+1, \
                                    int(due_list[0]))

    if date_today > due_date and task.status.lower() == "no":
        return 1
    else:
        return 0


def user_percent_overdue(user, tasks_list):
    i = 0
    tally = 0
    for task in tasks_list:
        if task.user == user.get_username() and check_if_overdue(task) == 1:
            i += 1
            tally += 1
        elif task.user == user.get_username() and check_if_overdue(task) == 0:
            tally += 1

    try: #to prevent a divide by zero error if the user has no tasks
        percentage = round((i/tally)*100, 2)
        return "{}{} of tasks assigned to {} are overdue".format(percentage, \
                                                    "%", user.get_username())
    except:
        return None


def generate_reports(users_list, tasks_list):
    '''
    Creates the task_overview and user_overview files and provides top-level
    and user-level summaries.
    '''
    try:
        with open("./task_overview.txt", "w") as file:
            file.write("No. of users on file: {}\n".format(len(users_list)))
            file.write("\n")
            file.write("{}\n".format(total_tasks(tasks_list)))
            file.write("{}\n".format(total_completed_tasks(tasks_list)))
            file.write("{}\n".format(total_incomplete_tasks(tasks_list)))
            file.write("{}\n".format(total_overdue_tasks(tasks_list)))
            file.write("{}\n".format(percent_incomplete(tasks_list)))
            file.write("{}\n".format(percent_overdue(tasks_list)))
    except:
        print("Error occurred while trying to generate reports.")

    try:
        with open("./user_overview.txt", "w") as file:
            file.write("No. of users on file: {}\n".format(len(users_list)))
            file.write("{}\n".format(total_tasks(tasks_list)))
            file.write("\n")

            for user in users_list:  #writing summary for each user
                file.write("{}\n".format(user_total_tasks(user, tasks_list)))
                file.write("{}\n".format(user_percent_tasks(user, tasks_list)))

                if user_percent_completed(user, tasks_list) == None:
                    file.write("")  #if a user has no tasks, it makes no sense
                                    #to write anything for the next 3 entries
                else:
                    file.write("{}\n".format(user_percent_completed(user, \
                                            tasks_list)))

                if user_percent_incomplete(user, tasks_list) == None:
                    file.write("")
                else:
                    file.write("{}\n".format(user_percent_incomplete(user, \
                                            tasks_list)))

                if user_percent_overdue(user, tasks_list) == None:
                    file.write("")
                else:
                    file.write("{}\n".format(user_percent_overdue(user, \
                                            tasks_list)))
                file.write("\n")
    except:
        print("Error occurred while trying to generate reports.")


def display_statistics(users_list, tasks_list):
    '''
    Presents info in task_overview and user_overview files in a readable form
    on the console. Creates them if they don't already exist to prevent errors.
    '''
    try:
        generate_reports(users_list, tasks_list)
        with open("./task_overview.txt", "r") as file:
            print("Summary for all tasks:\n")
            for line in file:
                line = line.strip("\n")
                print(line)
        print("\n")

        with open("./user_overview.txt", "r") as file:
            print("Summary for tasks assigned to each user\n")
            for line in file:
                line = line.strip("\n")
                print(line)

    except:
        print("Error occurred while trying to display statistics.")


# ==== Login Section ====
#initialising and filling user and tasks lists with read_data function
users_list = []
tasks_list = []
read_data(users_list, tasks_list)

username = input("Enter your username: ")
password = input("Enter your password: ")

'''
The following block of code checks if the user's details are on file exactly as
they were inputted. It does this by looking at each User object in the list. If
a matching username and password are found, exit the block.
'''
x = True
position = 1 #need to keep track of position as we go through the users list.
#this allows us to get to the else condition once we reach the end of the list
#after failing to find the user.
while x == True and position != 0:
    for user in users_list:
        if user.get_username() == username and user.get_password() == password:
            print("Successfully logged in.")
            x = False
            position = 0
            break
        elif position < len(users_list):
            position = position + 1
        else: #only come here if we reach the end of the list with no match
            #allows us to take user input and start the search again.
            position = 1
            print("Incorrect login details. \n")
            username = input("Try entering your username again: ")
            password = input("Try entering your password again: ")

while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.

    if username == "admin":
        menu = input(
            '''Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    vc - view completed tasks
    del - delete tasks
    ds - display statistics
    gr - generate reports
    e - exit
    : '''
        ).lower()

    else:
        menu = input(
            '''Select one of the following options:
    a - add task
    va - view all tasks
    vm - view my tasks
    ds - display statistics
    gr - generate reports
    e - exit
    : '''
        ).lower()

    if menu == 'r' and username == "admin":
        '''
        requests a new user's username and password.
        it then doesn't progress until the password is confirmed exactly.
        reg_user takes the new user's details, and adds them to the user
        text file. If the details already exist it will repeat the process
        of getting the details again.
        '''
        new_username = input("Registration: enter the new user's username: ")
        new_pass = input("Registration: enter the new user's password: ")
        confirm = input("Confirm the new user's password: ")

        while confirm != new_pass:
            confirm = input("Passwords don't match, please confirm again: ")

        reg_user(new_username, new_pass, users_list)


    elif menu == 'a':
        '''This code block will allow a user to add a new task to task.txt file
        - You can use these steps:
            - Prompt a user for the following:
                - the username of the person whom the task is assigned to,
                - the title of the task,
                - the description of the task, and
                - the due date of the task.
            - Then, get the current date.
            - Add the data to the file task.txt
            - Remember to include 'No' to indicate that the task is not
            complete.
        '''
        task_user = input("Enter the user's name: ")
        #need to check if the user actually exists before adding a task
        pos = 1
        while pos != 0:
            for user in users_list:
                if user.get_username() == task_user:
                    pos = 0
                    break
                elif pos < len(users_list):
                    pos += 1
                else:
                    task_user = input("Error: username not found. Please enter"
                                    " it exactly as it appears on file: ")
                    pos = 1

        task_title = input("Enter the task's title: ")
        task_description = input("Provide a brief description of the task. "
                                "Do not include commas in your description: ")

        dates = dateinput()  #using the dateinput function to get valid start
        #and due dates
        task_start = dates[0]
        task_due = dates[1]

        task_status = "No"

        add_task(task_user, task_title, task_description, task_start,
                task_due, task_status, tasks_list)

    elif menu == 'va':
        '''
        invoke the view_all function to output all tasks
        '''
        view_all()

    elif menu == 'vm':
        '''
        invoke the view_mine function to output the user's tasks
        '''
        view_mine(users_list, tasks_list, User(username, password))

    elif menu == "vc" and username == "admin":
        '''
        invoke the view_completed function for admin to output the user's task

        '''
        view_completed(tasks_list, User(username, password))

    elif menu == "del" and username == "admin":
        '''
        invoke the delete function for the admin to delete selected tasks
        '''
        delete(tasks_list, User(username, password))

    elif menu == "ds":
        display_statistics(users_list, tasks_list)

    elif menu == "gr":
        generate_reports(users_list, tasks_list)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
