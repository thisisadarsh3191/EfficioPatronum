# signin.py
import customtkinter as ctk
import connector

def build_signup(app, on_signup_success=None, onSignup=None):
    for widget in app.winfo_children():
        widget.destroy()
    show_pw = ctk.BooleanVar(value=False)
    def showPW():
        show_pw.set(not show_pw.get())
        if show_pw.get():
            fields["password"]["entry"].configure(show='')
            showPwButton.configure(text='Hide Password')
        else:
            fields["password"]["entry"].configure(show='*')
            showPwButton.configure(text='Show Password')

    def signup():
        hasError = False
        for field in fields.values():
            field["entry"].configure(border_color="#565B5E")
            field["error_label"].configure(text="")
        for fieldName, fieldData in fields.items():
            value = fieldData["entry"].get().strip()
            if not value:
                hasError = True
                fieldData["entry"].configure(border_color='red', border_width=2)
                fieldData["error_label"].configure(text="{} is required".format(fieldName.capitalize()))
        if not hasError:
            name = fields["name"]["entry"].get().strip()
            username = fields["username"]["entry"].get().strip()
            password = fields["password"]["entry"].get().strip()
            res = connector.register(name, username, password)
            if res is True:
                field["error_label"].configure(text="Signup successful! Go back to login.", text_color="green")
            elif isinstance(res, str):
                field["error_label"].configure(text=res, text_color="red")
            elif res is False:
                field["error_label"].configure(text="Username already exists", text_color="red")
    title = ctk.CTkLabel(app, text="Sign Up", font=ctk.CTkFont(size=22, weight="bold"),text_color=("#222222", "#FFFFFF"), bg_color="transparent", fg_color="transparent")
    title.pack(pady=20)
    entry_frame = ctk.CTkFrame(app,fg_color="transparent", bg_color="transparent")
    entry_frame.pack(pady=10)
    fields = {}
    fields["name"] = {
        "entry": ctk.CTkEntry(entry_frame, placeholder_text="Name", width=300),
        "error_label": ctk.CTkLabel(entry_frame, text='', text_color="red")
    }
    fields["name"]["entry"].pack(pady=5)
    fields["name"]["error_label"].pack()
    fields["username"] = {
        "entry": ctk.CTkEntry(entry_frame, placeholder_text='Enter Username:', width=300),
        "error_label": ctk.CTkLabel(entry_frame, text='', text_color="red")
    }
    fields["username"]["entry"].pack(pady=5)
    fields["username"]["error_label"].pack()
    password_container = ctk.CTkFrame(entry_frame, fg_color="transparent", bg_color="transparent")
    password_container.pack(fill="x", pady=5)
    fields["password"] = {
        "entry": ctk.CTkEntry(password_container, placeholder_text='Enter Password', show='*', width=300),
        "error_label": ctk.CTkLabel(password_container, text='', text_color="red")
    }
    fields["password"]["entry"].pack(pady=0)
    fields["password"]["error_label"].pack()
    showPwButton = ctk.CTkButton(
        password_container,
        text='Show Password',
        width=80,
        height=20,
        fg_color=("#2B2B2B", "#F1F3F4"),
        hover=False,
        text_color=("#DFDFDF", "#2B2B2B"),
        font=ctk.CTkFont(size=12),
        command=showPW
    )
    showPwButton.pack(pady=(0, 5))
    signUpButton = ctk.CTkButton(app, text="Sign Up", width=200, command=signup,fg_color="#13b21e", hover_color="#0d5712", text_color="white", font=ctk.CTkFont(size=16, weight="bold"))
    signUpButton.pack(pady=20)
    if onSignup:
        back_btn = ctk.CTkButton(app, text="Back to Login", command=onSignup)
        back_btn.pack(pady=10)
