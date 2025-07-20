import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Efficio Patronum")
app.geometry("500x500")
app.resizable(True, True)

showPW = ctk.BooleanVar(value=False)

def show_pw():
    showPW.set(not showPW.get())
    if showPW.get():
        fields["password"]["entry"].configure(show='')
        passBtn.configure(text='Hide Password')
    else:
        fields["password"]["entry"].configure(show='*')
        passBtn.configure(text='Show Password')

title = ctk.CTkLabel(app, text="Login Page", font=ctk.CTkFont(size=22, weight="bold"))
title.pack(pady=20)

entryFrame = ctk.CTkFrame(app,bg_color="transparent",fg_color="transparent")
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
    fg_color="#C1BABA",
    hover=False,
    text_color=("#2B2B2B", "#DFDFDF"),
    font=ctk.CTkFont(size=12),
    command=show_pw
)

passBtn.pack(pady=(0, 5)) 

def login():
    username = fields["username"]["entry"].get().strip()
    password = fields["password"]["entry"].get().strip()

    for field in fields.values():
        field["entry"].configure(border_color='#565B5E')
        field["error_label"].configure(text='')

    has_error = False
    if not username.strip():
        has_error = True
        fields["username"]["entry"].configure(border_color='red', border_width=2)
        fields["username"]["error_label"].configure(text="Username is required")

    if not password.strip():
        has_error = True
        fields["password"]["entry"].configure(border_color='red', border_width=2)
        fields["password"]["error_label"].configure(text="Password is required")
    
    if has_error:
        return
    
    #checking condition
    
    print(f"Username: {username}, Password: {password}")

login_button = ctk.CTkButton(app, text="Login", command=login)
login_button.pack(pady=20)

app.mainloop()