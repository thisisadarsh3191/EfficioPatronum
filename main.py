import customtkinter as ctk
import home
import loginpage
import timer


app = ctk.CTk()
app.title("Efficio Patronum")
app.geometry("500x500")
app.resizable(True, True)

import customtkinter as ctk
import loginpage
import signin
import home


currentUser = None
def showHome(username):
    global currentUser
    currentUser = username
    home.build_home(app, username, onDockButtonClick=onDockButtonClick)

def onDockButtonClick(ButtonID):
    if ButtonID == "timer":
        for widget in app.winfo_children():
            widget.destroy()
        timer.build_timer(app,onDockButtonClick=onDockButtonClick)
    elif ButtonID == "home":
        for widget in app.winfo_children():
            widget.destroy()
        showHome(currentUser)  # Replace with actual username if available
    else:
        print(f"Button {ButtonID} clicked")

def showLogin():
    for widget in app.winfo_children():
        widget.destroy()
    loginpage.login(app, onLoginSuccess=showHome, onSignup=showSignup)

def showSignup():
    signin.build_signup(app, onSignup=showLogin)


ctk.set_appearance_mode("Light")
app = ctk.CTk()

app.title("Efficio Patronum")
app.geometry("500x500")
app.resizable(True, True)

showLogin()

app.mainloop()
