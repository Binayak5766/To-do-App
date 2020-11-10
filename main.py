'''This is a simple to-do app designed by Binayak Ghosal. I have did some pretty simple things. I have decided to store the tasks and the subtasks in form of a dictionary in a json file. And the daily tasks that are updated everyday are stored in a .txt file. They are stored in just normal format. This is my very first project which I took up from the question answer section of a python course in which I was enrolled in. The guy who posed this question asked to use Tkinter but I used Kivy. This app stores the daily list and the todo list of the customers that use it.'''


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from plyer import notification
import json
import datetime

Builder.load_file("design.kv")
#The tasks are stored in a json file in a dictionary format.
#The limitation is that only 5 subtasks can be added to a task.


class LoginScreen(Screen):
    def tasks_today(self):
        file = open("To-do.txt", 'r')
        var = file.readlines()                             #Stores the content of the file in a list.
        file.close()
        tasks = ""
        flag = 0
        date_today = str(datetime.date.today())
        date_today = datetime.datetime.strptime(date_today,'%Y-%m-%d')
        for i in range(0,len(var)):
            try:
                check = var[i]
                check = check[:-2]
                check = datetime.datetime.strptime(check, '%Y-%m-%d')                #Checks the dates in the file with todays date.
                if check == date_today:
                    flag = 1
                    for j in range(i,len(var)):                           #Prints out the tasks for today.
                        tasks = tasks + var[j]
                break
            except:
                pass
                
        if flag == 0:
            self.ids.todo.text = "There is no tasks scheduled for today."
        else:
            self.ids.todo.text = tasks

    def go_progress(self):
        self.manager.current = "Progress_screen"

    def go_dailynote(self):
        self.manager.current = "Dailynote_screen"

    def exit(self):                  #This function closes the window
        Window.close()

class ProgressScreen(Screen):
    def view_all(self):
        with open ("Tasks.json") as file:
            task = json.load(file)

        lst = []
        variable = ""
        for i in task.keys():
            lst.append(i)
        for i in range(0,len(lst)):
            variable = variable + lst[i] + "\n" 
        lst = []
        for i in task.values():
            for j in i.values():
                lst.append(j)
        variables = ""
        for k in range(0,len(lst)):
            variables = variables + lst[k] + "\n"  
        self.ids.tasks_add.text = variable
        self.ids.subtasks_add.text = variables
             
    def add_task(self, task):
        with open ("Tasks.json") as file:
            tasks = json.load(file)

        tasks[task] = {'subtask1': '', 'subtask2': '', 'subtask3': '', 'subtask4': '', 'subtask5': '',}
        with open ("Tasks.json",'w') as file:
            json.dump(tasks,file)

    def add_subtask(self, task, subtask):
        with open ("Tasks.json") as file:
            tasks = json.load(file)

        subtask_to_add = list(subtask.split("\n"))

        if task in tasks.keys():
            try:
                tasks[task]['subtask1'] = subtask_to_add[0]
            except:
                tasks[task]['subtask1'] = ''
            try:
                tasks[task]['subtask2'] = subtask_to_add[1]
            except:
                tasks[task]['subtask2'] = ''
            try:
                tasks[task]['subtask3'] = subtask_to_add[2]
            except:
                tasks[task]['subtask3'] = ''
            try:
                tasks[task]['subtask4'] = subtask_to_add[3]
            except:
                tasks[task]['subtask4'] = ''
            try:
                tasks[task]['subtask5'] = subtask_to_add[4]
            except:
                tasks[task]['subtask5'] = ''
            
        with open ("Tasks.json",'w') as file:
            json.dump(tasks,file)

    def update(self, task, subtask):            #You will have to give the value of the subtasks starting from 1 to 5.
        with open ("Tasks.json") as file:
            tasks = json.load(file)

        updated_subtask = subtask.split("\n")

        if task in tasks.keys():
            try:
                tasks[task]['subtask1'] = updated_subtask[0]
            except:
                pass
            try:
                tasks[task]['subtask2'] = updated_subtask[1]
            except:
                pass
            try:
                tasks[task]['subtask3'] = updated_subtask[2]
            except:
                pass
            try:
                tasks[task]['subtask4'] = updated_subtask[3]
            except:
                pass
            try:
                tasks[task]['subtask5'] = updated_subtask[4]
            except:
                pass
            
        with open ("Tasks.json",'w') as file:
            json.dump(tasks,file)


    def clear(self):
        self.ids.tasks_add.text = ""
        self.ids.subtasks_add.text = ""


    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_screen"

    def exit(self):                  #This function closes the window
        Window.close()

class MainApp(App):
    def build(self):
        self.notify_me()
        return RootWidget()

    @staticmethod
    def notify_me():
        file = open("To-do.txt", 'r')
        var = file.readlines()                             #Stores the content of the file in a list.
        file.close()
        tasks = ""
        flag = 0
        date_today = str(datetime.date.today())
        date_today = datetime.datetime.strptime(date_today,'%Y-%m-%d')
        for i in range(0,len(var)):
            try:
                check = var[i]
                check = check[:-2]
                check = datetime.datetime.strptime(check, '%Y-%m-%d')                #Checks the dates in the file with todays date.
                if check == date_today:
                    flag = 1
                    for j in range(i,len(var)):                           #Prints out the tasks for today.
                        tasks = tasks + var[j]
            except:
                pass

        if(len(var) == 0):
            notification.notify(title='Tasks', message='No tasks scheduled for today.', ticker='r')
        else:
            notification.notify(title='Tasks', message=tasks, ticker='r')


class DailyNoteScreen(Screen):
    def view(self):
        file = open("To-do.txt", 'r')
        var = file.read()
        file.close()
        self.ids.print.text = var

    def save(self, daily_task):
        t = MainApp()               #New object created to access the notify_me function to get a notification upon adding new task.
        file = open("To-do.txt", 'a')
        file.write(str(datetime.date.today()) + ":" + "\n" + daily_task + "\n")
        file.close()
        t.notify_me()

    def clear(self):
        self.ids.print.text = ""

    def back(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "Login_screen"

    def exit(self):                  #This function closes the window
        Window.close()

class RootWidget(ScreenManager):
    pass

if __name__ == "__main__":
    MainApp().run()