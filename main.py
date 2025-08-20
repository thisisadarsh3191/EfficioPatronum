import customtkinter as ctk
import home
import loginpage
import signin
import clock
import settings






currentUser = None
def showHome(username):
    global currentUser
    currentUser = username
    home.build_home(app, username, onDockButtonClick=onDockButtonClick,)

def onDockButtonClick(ButtonID):
    if ButtonID == "timer":
        for widget in app.winfo_children():
            widget.destroy()
        clock.build_timer(app,onDockButtonClick=onDockButtonClick)
    elif ButtonID == "home":
        for widget in app.winfo_children():
            widget.destroy()
        showHome(currentUser)  
    elif ButtonID == "settings":
        for widget in app.winfo_children():
            widget.destroy()
        settings.showSettings(app, currentUser, onLogout=showLogin,onDockButtonClick=onDockButtonClick)

def showLogin():
    for widget in app.winfo_children():
        widget.destroy()
    loginpage.login(app, onLoginSuccess=showHome, onSignup=showSignup)

def showSignup():
    signin.build_signup(app, onSignup=showLogin)


ctk.set_appearance_mode("Light")
app = ctk.CTk()
app.geometry("550x600")
app.minsize(400,400)
app.title("Efficio Patronum")
app.resizable(True,True)

showLogin()

app.mainloop()
