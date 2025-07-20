import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Task Planner")
app.geometry("500x500")
app.resizable(True, True)

def darkLight():
    current = ctk.get_appearance_mode()
    if current == "dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

def darkIcon():
    current = ctk.get_appearance_mode()
    if current == "dark":
        return ctk.CTkImage(Image.open("dark.png"))
    else:
        return ctk.CTkImage(Image.open("light.png"))

def check(cb, tt):
    """Toggle strike-through effect"""
    if cb.get():
        tt.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")
    else:
        tt.configure(font=ctk.CTkFont(size=16), text_color=("black", "white"))

masterFrame = ctk.CTkFrame(app, fg_color="transparent")
masterFrame.pack(fill="both", expand=True, padx=10, pady=10)

topFrame = ctk.CTkFrame(masterFrame, fg_color="transparent", height=50)
topFrame.pack(fill="x", pady=(0, 10))

title = ctk.CTkLabel(topFrame, text="Tasks", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(side="left", padx=10)

darkLightBtn = ctk.CTkButton(
    topFrame,
    width=40,
    height=40,
    corner_radius=20,
    fg_color="transparent",
    hover_color=("#f1f3f4","#2b2b2b"),
    command=darkLight,
    image=darkIcon()
)

plusBtn = ctk.CTkButton(
    topFrame,
    text="+",
    width=40,
    height=40,
    corner_radius=20,
    fg_color="#1a73e8",
    hover_color="#0d62c9",
    font=ctk.CTkFont(size=20),
    command=lambda: print("Add task button clicked")
)
plusBtn.pack(side="right", padx=10)

tasks = ctk.CTkScrollableFrame(masterFrame, fg_color="transparent")
tasks.pack(fill="both", expand=True)

taskList = {
    "task1": {"name": "Buy groceries", "type": "Personal", "completed": False},
    "task2": {"name": "Finish report", "type": "Work", "completed": True},
    "task3": {"name": "Call mom", "type": "Personal", "completed": False},
    "task4": {"name": "Gym workout", "type": "Health", "completed": False},
    "task5": {"name": "Read book", "type": "Learning", "completed": True},
    "task6": {"name": "Pay bills", "type": "Finance", "completed": False},
}

for task in taskList:
    taskFrame = ctk.CTkFrame(tasks, height=40, fg_color="transparent")
    taskFrame.pack(fill="x", pady=1)  

    taskText = ctk.CTkLabel(
        taskFrame,
        text=taskList[task]["name"],
        font=ctk.CTkFont(size=16),
        anchor="w"
    )
    
    checkbox = ctk.CTkCheckBox(
        taskFrame,
        text="",
        width=20,
        height=20,
        border_width=2,
        command=lambda cb=None, tt=taskText: check(cb, tt) if cb else None
    )
    
    checkbox.configure(command=lambda cb=checkbox, tt=taskText: check(cb, tt))
    
    checkbox.pack(side="left", padx=(5, 10))
    taskText.pack(side="left", fill="x", expand=True)
    
    if taskList[task]["completed"]:
        checkbox.select()
        taskText.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")

dock = ctk.CTkFrame(app, height=70, corner_radius=0)
dock.pack(side="bottom", fill="x")

dockBtn = {
    "Home": ctk.CTkImage(Image.open("homeIcon.png")),
    "Timer": ctk.CTkImage(Image.open("timerIcon.png")),
    "Settings": ctk.CTkImage(Image.open("settingsicon.png"))
}

for btn_text in ["Home", "Timer", "Settings"]:
    btn = ctk.CTkButton(
        dock,
        text=btn_text,
        image=dockBtn[btn_text],
        width=100,
        height=75,
        corner_radius=10,
        fg_color="transparent",
        hover_color=("#000000","#ffffff"),
        compound="top",
        command=lambda text=btn_text: print(f"{text} button clicked")
    )
    btn.pack(side="left", expand=True)

app.mainloop()