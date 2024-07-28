import json
import os
from difflib import get_close_matches as yakinsonuc
from datetime import datetime
from customtkinter import *

def addIcon(window):
    window.iconbitmap('AEXP AI Logo.ico')

mainWindow = CTk()
mainWindow.title('AEXP AI')
mainWindow.geometry('1366x768')
mainWindow.iconbitmap('AEXP AI Logo.ico')

def downloadDB(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        print(f"Cant find database named {filepath}. A new database will be created.")
        return {"questions": []}

def saveToDB(filepath, database):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(database, file, indent=2)

def findCloseAnswer(question, questions):
    eslesen = yakinsonuc(question, questions, n=1, cutoff=0.6)
    return eslesen[0] if eslesen else None

def findUserAnswer(question, database):
    for answers in database["questions"]:
        if answers["question"] == question:
            return answers["answer"], answers.get("addedDate", "unknow")
    return None, None

def addNewQuestion(filepath, question, answer, database):
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    database["questions"].append({"question": question, "answer": answer, "addedDate": date})
    saveToDB(filepath, database)

def userRegistration(user, password):
    with open('database.json', 'r', encoding='utf-8') as file:
        user_database = json.load(file)

    if user in user_database:
        return False
    else:
        user_database[user] = password
        with open('database.json', 'w', encoding='utf-8') as file:
            json.dump(user_database, file, indent=2)
        return True

def userLogin(user, password):
    with open('database.json', 'r', encoding='utf-8') as file:
        user_database = json.load(file)

    if user in user_database and user_database[user] == password:
        return True
    else:
        return False

def userLoginWindow():
    loginWindow = CTkToplevel()
    loginWindow.title('User Login')
    loginWindow.geometry('600x400')
    addIcon(loginWindow)
    loginWindow.grab_set() 

    def login():
        userlogin = user.get()
        passwordlogin = password.get()
        if userLogin(userlogin, passwordlogin):
            global user
            global user_database
            user = userlogin
            user_database = downloadDB(f'{user}_database.json')
            loginWindow.destroy()
            showDialogWindow()
        else:
            errorText.configure(text="Wrong username or password")

    frame = CTkFrame(loginWindow, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    CTkLabel(frame, text="Username:", font=("Helvetica", 16)).pack(pady=10)
    user = CTkEntry(frame)
    user.pack(pady=10)
    
    CTkLabel(frame, text="Password:", font=("Helvetica", 16)).pack(pady=10)
    password = CTkEntry(frame, show="*")
    password.pack(pady=10)
    
    errorText = CTkLabel(frame, text="", text_color="red")
    errorText.pack(pady=10)
    
    CTkButton(frame, text="Login", command=login, fg_color="#1e90ff").pack(pady=10)

def userRegistrationWindow():
    registrationWindow = CTkToplevel()
    registrationWindow.geometry('600x400')
    registrationWindow.title("User Registration")
    addIcon(registrationWindow)
    registrationWindow.grab_set()  

    def registration():
        regName = user.get()
        regPassword = password.get()
        if userRegistration(regName, regPassword):
            global user
            global user_database
            user = regName
            user_database = downloadDB(f'{user}_database.json')
            registrationWindow.destroy()
            showDialogWindow()
        else:
            errorText.configure(text="This username already exists.")

    frame = CTkFrame(registrationWindow, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    CTkLabel(frame, text="Username:", font=("Helvetica", 16)).pack(pady=10)
    user = CTkEntry(frame)
    user.pack(pady=10)
    
    CTkLabel(frame, text="Password:", font=("Helvetica", 16)).pack(pady=10)
    password = CTkEntry(frame, show="*")
    password.pack(pady=10)
    
    errorText = CTkLabel(frame, text="", text_color="red")
    errorText.pack(pady=10)
    
    CTkButton(frame, text="Register", command=registration, fg_color="#1e90ff").pack(pady=10)

def showDialogWindow():
    dialogWindow = CTkToplevel()
    dialogWindow.title('Question Window')
    dialogWindow.geometry('600x400')
    addIcon(dialogWindow)
    dialogWindow.grab_set()

    def speak():
        user_prompt = userPrompt.get()
        if user_prompt == 'quit':
            dialogWindow.destroy()
            mainWindow.deiconify()
        else:
            userQuestion = findCloseAnswer(user_prompt, [answers["question"] for answers in user_database["questions"]])
            if userQuestion:
                bot_prompt, _ = findUserAnswer(userQuestion, user_database)
                botPrompt.configure(text=f"AEXP AI: {bot_prompt}")
            else:
                newQuestion = CTkInputDialog(text="I don't know how to answer this. Can you teach?", title="AEXP AI").get_input()
                if newQuestion != 'skip':
                    if user:
                        addNewQuestion(f'{user}_database.json', user_prompt, newQuestion, user_database)
                    else:
                        addNewQuestion('database.json', user_prompt, newQuestion, user_database)
                    botPrompt.configure(text="AEXP AI: Thank you, I learned something new thanks to you.")

    frame = CTkFrame(dialogWindow, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    userPrompt = CTkEntry(frame, height=50, width=300)
    userPrompt.pack(pady=10)
    
    CTkButton(frame, text="Send", command=speak, fg_color="#1e90ff").pack(pady=10)
    botPrompt = CTkLabel(frame, text="", wraplength=500, font=("Helvetica", 14))
    botPrompt.pack(pady=20)

def exit():
    mainWindow.destroy()

mainFrame = CTkFrame(mainWindow, corner_radius=10)
mainFrame.pack(pady=20, padx=20, fill="both", expand=True)

CTkLabel(mainFrame, text="AEXP AI", font=("Helvetica", 24, "bold")).pack(pady=20)
CTkButton(mainFrame, text="User Login", command=userLoginWindow, fg_color="#1e90ff", font=("Helvetica", 16)).pack(pady=10)
CTkButton(mainFrame, text="User Registration", command=userRegistrationWindow, fg_color="#1e90ff", font=("Helvetica", 16)).pack(pady=10)
CTkButton(mainFrame, text="Open Conversation", command=showDialogWindow, fg_color="#1e90ff", font=("Helvetica", 16)).pack(pady=10)
CTkButton(mainWindow, text="Exit", command=exit).pack(side="top", anchor="se", padx=10, pady=10)

botPrompt = CTkLabel(mainFrame, text="", wraplength=1000, font=("Helvetica", 14))
botPrompt.pack(pady=20)

user_database = downloadDB('database.json')

mainWindow.mainloop()