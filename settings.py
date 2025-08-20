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

    status = ctk.CTkLabel(settingsFrame, text="", text_color="red")
    status.pack(pady=(4, 10))

    def change_password():
        oldPassword = currentPw.get()
        newPassword = newPw.get()
        status.configure(text="")

        if conn.login(username, oldPassword):
            if conn.passwordStrength(newPassword) is True:
                conn.changePw(username, newPassword)
                ctk.CTkLabel(settingsFrame, text="Password changed successfully!", text_color="green").pack()
            else:
                ctk.CTkLabel(settingsFrame, text=conn.passwordStrength(newPassword).capitalize, text_color="red").pack()
        else:
            ctk.CTkLabel(settingsFrame, text="Current password incorrect!", text_color="red").pack()
    
    ctk.CTkButton(settingsFrame, text="Change Password", command=change_password).pack(pady=10)

    def deleteAcc():
        dialog = ctk.CTkToplevel(settingsFrame)
        dialog.title("Delete Account")
        dialog.geometry("500x250")
        dialog.grab_set()
        dialog.resizable(False, False)

        ctk.CTkLabel(dialog,text="Enter Password to Confirm Deletion:",font=ctk.CTkFont(size=16)).pack(pady=(20,10))

        pwInput = ctk.CTkEntry(dialog, placeholder_text="Password", show="*",width=300)
        pwInput.pack(pady=10)
        pwInput.focus()

        warning = "Warning: This action cannot be undone! Deleting your account will remove all your data."
        ctk.CTkLabel(dialog, text=warning, text_color="red").pack(pady=(10, 0))

        status = ctk.CTkLabel(dialog, text="", text_color="red")
        status.pack(pady=(10, 0))

        btnFrame = ctk.CTkFrame(dialog,fg_color="transparent")
        btnFrame.pack(pady=10)

        def confirmDeletion():
            password = pwInput.get()
            success, msg = conn.deleteAccount(username, password)
            if success:
                status.configure(text="Account deleted successfully!", text_color="green")
                dialog.after(1500, lambda: (dialog.destroy(), onLogout()))
            else:
                status.configure(text=msg)
        def cancelDeletion():
            dialog.destroy()

        deleteBtn = ctk.CTkButton(
            btnFrame, 
            text="Delete Account",
            command=confirmDeletion,
            fg_color="#ff4d4d",
            hover_color="#cc0000",
            width=100
        )
        deleteBtn.pack(side="left", padx=20)
        cancelBtn = ctk.CTkButton(
            btnFrame, 
            text="Cancel",
            command=cancelDeletion,
            fg_color="#a0a0a0",
            hover_color="#888888",
            width=100
        )
        cancelBtn.pack(side="right", padx=20)
    
    ctk.CTkButton(
        settingsFrame,
        text="Delete Account",
        command=deleteAcc,
        fg_color="#ff4d4d",
        hover_color="#cc0000",
        text_color="white",
    ).pack(pady=20)



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
            command=(lambda b=btnID: onDockButtonClick(b)) if onDockButtonClick else (lambda b=btnID: print(f"{b} button clicked")))
        btn.pack(side="left", expand=True)


