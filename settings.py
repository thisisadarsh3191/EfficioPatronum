import customtkinter as ctk
import connector as conn
from home import dock_buttons

def showSettings(app, username, onLogout,onDockButtonClick=None):

    settingsFrame = ctk.CTkFrame(app)
    settingsFrame.pack(fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(settingsFrame, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

    ctk.CTkLabel(settingsFrame, text="Change Password", font=ctk.CTkFont(size=16)).pack(pady=(30, 6))
    currentPw = ctk.CTkEntry(settingsFrame, placeholder_text="Current Password", show="*")
    currentPw.pack(pady=4)
    newPw = ctk.CTkEntry(settingsFrame, placeholder_text="New Password", show="*")
    newPw.pack(pady=4)

    def change_password():
        oldPassword = currentPw.get()
        newPassword = newPw.get()
        if conn.login(username, oldPassword):
            if conn.passwordStrength(newPassword) is True:
                conn.changePw(username, newPassword)
                ctk.CTkLabel(settingsFrame, text="Password changed successfully!", text_color="green").pack()
            else:
                ctk.CTkLabel(settingsFrame, text=conn.passwordStrength(newPassword).capitalize, text_color="red").pack()
        else:
            ctk.CTkLabel(settingsFrame, text="Current password incorrect!", text_color="red").pack()

    

    ctk.CTkButton(settingsFrame, text="Change Password", command=change_password).pack(pady=10)

    # Logout Button
    ctk.CTkButton(settingsFrame, text="Logout", fg_color="#d7263d", text_color="white", command=onLogout).pack(pady=40)

    dock = ctk.CTkFrame(app, height=70, corner_radius=0)
    dock.pack(side="bottom", fill="x")




    for btnID, btnData in dock_buttons.items():
        btn = ctk.CTkButton(
            dock,
            text=btnData['text'],
            text_color=("black", "white"),
            width=80,
            height=60,
            corner_radius=10,
            fg_color="transparent",
            hover_color=("#60acd2", "#60acd2"),
            compound="top",
            font=ctk.CTkFont(size=18),
            command=(lambda b=btnID: onDockButtonClick(b)) if onDockButtonClick else (lambda b=btnID: print(f"{b} button clicked"))        )
        btn.pack(side="left", expand=True)

