import customtkinter as ctk
import connector

def show_signup(parent, on_success, on_login):
    for widget in parent.winfo_children():
        widget.destroy()
    connector.init()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    result_label = ctk.CTkLabel(parent, text="", text_color="red")
    result_label.pack(pady=5)
    fields = {}
    entry_frame = ctk.CTkFrame(parent)
    entry_frame.pack(pady=10)

    fields["name"] = ctk.CTkEntry(entry_frame, placeholder_text="Name", width=300)
    fields["name"].pack(pady=5)
    fields["username"] = ctk.CTkEntry(entry_frame, placeholder_text="Username", width=300)
    fields["username"].pack(pady=5)
    fields["password"] = ctk.CTkEntry(entry_frame, placeholder_text="Password", show="*", width=300)
    fields["password"].pack(pady=5)

    show_pw_btn = ctk.CTkButton(
        entry_frame, text='Show Password', width=80, height=20,
        fg_color="#C1BABA", font=ctk.CTkFont(size=12),
        command=lambda: toggle_pw()
    )
    show_pw_btn.pack(pady=(0, 5))

    show_pw_state = [False]
    def toggle_pw():
        show_pw_state[0] = not show_pw_state[0]
        fields["password"].configure(show='' if show_pw_state[0] else '*')
        show_pw_btn.configure(text='Hide Password' if show_pw_state[0] else 'Show Password')

    def signup():
        name = fields["name"].get().strip()
        username = fields["username"].get().strip()
        password = fields["password"].get().strip()
        result_label.configure(text="")
        if not name or not username or not password:
            result_label.configure(text="All fields required.", text_color="red")
            return
        check = connector.passwordStrength(password)
        if check is not True:
            result_label.configure(text=connector.strength[check], text_color="red")
            return
        resp = connector.register(name, username, password)
        if resp is True:
            result_label.configure(text="Registration successful!", text_color="green")
            on_success()
        elif resp is False:
            result_label.configure(text="Username already exists", text_color="red")
        else:
            result_label.configure(text=resp, text_color="red")

    signup_button = ctk.CTkButton(parent, text="Sign Up", width=200, command=signup)
    signup_button.pack(pady=10)
    login_btn = ctk.CTkButton(parent, text="Back to Login", command=on_login)
    login_btn.pack(pady=5)
