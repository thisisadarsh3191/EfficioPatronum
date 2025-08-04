import customtkinter as ctk
import connector

def show_login(parent, on_success, on_signup):
    # DESTROY previous widgets in parent frame
    for widget in parent.winfo_children():
        widget.destroy()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    showPW = ctk.BooleanVar(value=False)
    status_label = ctk.CTkLabel(parent, text="", text_color="red")
    status_label.pack(pady=5)
    fields = {}

    def show_pw():
        showPW.set(not showPW.get())
        if showPW.get():
            fields["password"].configure(show='')
            passBtn.configure(text='Hide Password')
        else:
            fields["password"].configure(show='*')
            passBtn.configure(text='Show Password')

    entryFrame = ctk.CTkFrame(parent)
    entryFrame.pack(pady=10)

    fields["username"] = ctk.CTkEntry(entryFrame, placeholder_text='Enter Username:', width=300)
    fields["username"].pack(pady=5)
    fields["password"] = ctk.CTkEntry(entryFrame, placeholder_text='Enter Password', show='*', width=300)
    fields["password"].pack(pady=5)

    passBtn = ctk.CTkButton(
        entryFrame, text='Show Password', width=80, height=20,
        fg_color="#C1BABA",
        text_color=("#2B2B2B", "#DFDFDF"),
        font=ctk.CTkFont(size=12),
        command=show_pw
    )
    passBtn.pack(pady=(0, 5))

    def do_login():
        username = fields["username"].get().strip()
        password = fields["password"].get().strip()
        status_label.configure(text="")
        if not username or not password:
            status_label.configure(text="Both fields required.")
            return
        if connector.login(username, password):
            on_success(username)
        else:
            status_label.configure(text="Invalid login.")

    login_button = ctk.CTkButton(parent, text="Login", command=do_login)
    login_button.pack(pady=10)
    signup_btn = ctk.CTkButton(parent, text="Sign Up", fg_color="#1a73e8", command=on_signup)
    signup_btn.pack(pady=5)
