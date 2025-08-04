import customtkinter as ctk
from loginpage import show_login      # expects: show_login(parent, on_success, on_signup)
from signin import show_signup    # expects: show_signup(parent, on_success, on_login)
from home import show_home        # expects: show_home(parent, username, on_timer, on_logout)
from timer import show_timer      # expects: show_timer(parent, on_back)

# Initialize root window and main frame
app = ctk.CTk()
app.title("Efficio Patronum")
app.geometry("500x700")
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

current_user = {'username': None}

def show_login_screen():
    show_login(main_frame,
        on_success=lambda username: [current_user.__setitem__('username', username), show_home_screen()],
        on_signup=show_signup_screen
    )

def show_signup_screen():
    show_signup(main_frame,
        on_success=show_login_screen,
        on_login=show_login_screen
    )

def show_home_screen():
    show_home(main_frame,
        username=current_user['username'],
        on_timer=show_timer_screen,
        on_logout=show_login_screen
    )

def show_timer_screen():
    show_timer(main_frame, on_back=show_home_screen)

# Show initially
show_login_screen()
app.mainloop()
