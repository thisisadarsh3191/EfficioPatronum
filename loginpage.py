import customtkinter as ctk
import connector as conn 

conn.init()

def login(app, onLoginSuccess,onSignup):
    showPW = ctk.BooleanVar(value=False)


    def show_pw():
        showPW.set(not showPW.get())
        if showPW.get():
            fields["password"]["entry"].configure(show='')
            passBtn.configure(text='Hide Password')
        else:
            fields["password"]["entry"].configure(show='*')
            passBtn.configure(text='Show Password')


    def do_login():
        username = fields["username"]["entry"].get().strip()
        password = fields["password"]["entry"].get().strip()

        status_label.configure(text="")
        for field in fields.values():
            field["entry"].configure(border_color='#565B5E')
            field["error_label"].configure(text='')

        has_error = False
        if not username:
            has_error = True
            fields["username"]["entry"].configure(border_color='red', border_width=2)
            fields["username"]["error_label"].configure(text="Username is required")

        if not password:
            has_error = True
            fields["password"]["entry"].configure(border_color='red', border_width=2)
            fields["password"]["error_label"].configure(text="Password is required")

        if has_error:
            status_label.configure(text="Please fill all fields", text_color="red")
            return None, False

        if conn.login(username, password):
            status_label.configure(text="Login successful!", text_color="green")
            for widget in app.winfo_children():
                widget.destroy()
            onLoginSuccess(username)
        else:
            status_label.configure(text="Invalid username or password", text_color="red")

    title = ctk.CTkLabel(
        app,
        text="Login Page",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color=("#222222", "#FFFFFF"),
        bg_color="transparent",
        fg_color="transparent"
    )
    title.pack(pady=20)

    entryFrame = ctk.CTkFrame(app, bg_color="transparent", fg_color="transparent")
    entryFrame.pack(pady=10)

    fields = {}

    fields["username"] = {
        "entry": ctk.CTkEntry(entryFrame, placeholder_text='Enter Username:', width=300),
        "error_label": ctk.CTkLabel(entryFrame, text='', text_color="red")
    }
    fields["username"]["entry"].pack(pady=5)
    fields["username"]["error_label"].pack()

    password_container = ctk.CTkFrame(entryFrame, fg_color="transparent", bg_color="transparent")
    password_container.pack(fill="x", pady=5)
    fields["password"] = {
        "entry": ctk.CTkEntry(password_container, placeholder_text='Enter Password', show='*', width=300),
        "error_label": ctk.CTkLabel(password_container, text='', text_color="red")
    }
    fields["password"]["entry"].pack(pady=0)
    fields["password"]["error_label"].pack()

    passBtn = ctk.CTkButton(
        entryFrame,
        text='Show Password',
        width=80,
        height=20,
        fg_color=("#2B2B2B", "#F1F3F4"),
        hover=False,
        text_color=("#DFDFDF", "#2B2B2B"),
        font=ctk.CTkFont(size=12),
        command=show_pw
    )
    passBtn.pack(pady=(0, 5))

    status_label = ctk.CTkLabel(app, text="", text_color="red")
    status_label.pack(pady=5)


    login_button = ctk.CTkButton(app, text="Login",fg_color="#1a73e8", command=do_login)
    login_button.pack(pady=20)

    signup_button = ctk.CTkButton(app,text="Sign Up", fg_color="#1a73e8", command=onSignup)
    signup_button.pack(pady=5)


