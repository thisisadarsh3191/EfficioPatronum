import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Efficio Patronum")
app.geometry("500x500")
app.resizable(True, True)

show_pw = ctk.BooleanVar(value=False)

def showPW():
    show_pw.set(not show_pw.get())
    if show_pw.get():
        fields["password"]["entry"].configure(show='')
        showPwButton.configure(text='Hide Password')
    else:
        fields["password"]["entry"].configure(show='*')
        showPwButton.configure(text='Show Password')

title = ctk.CTkLabel(app, text="Sign Up", font=ctk.CTkFont(size=22, weight="bold"))
title.pack(pady=20)

entry_frame = ctk.CTkFrame(app)
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

password_container = ctk.CTkFrame(entry_frame, fg_color="transparent")
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
    fg_color="#C1BABA",
    hover=False,
    text_color=("#2B2B2B", "#DFDFDF"),
    font=ctk.CTkFont(size=12),
    command=showPW
) 
showPwButton.pack(pady=(0, 5))  
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

        print("Signup successful")
        print("Name: {}".format(name))
        print("Username: {}".format(username))
        print("Password: {}".format(password))

signUpButton = ctk.CTkButton(app, text="Sign Up", width=200, command=signup)
signUpButton.pack(pady=20)

app.mainloop()