import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Task Planner")
app.geometry("500x700")  
app.resizable(False, False)


def invert(icon):
    current = ctk.get_appearance_mode()
    if current == "Dark":
        return ctk.CTkImage(Image.open(f"assets/{icon}_inverted.png"), size=(24, 24))
    else:
        return ctk.CTkImage(Image.open(f"assets/{icon}.png"), size=(24, 24))
    
def rebuild_dock():
    global dock
    
    dock.destroy()
    
    dock = ctk.CTkFrame(app, height=70, corner_radius=0)
    dock.pack(side="bottom", fill="x")
    
    for btnID, btnData in dock_buttons.items():
        btn = ctk.CTkButton(
            dock,
            image=invert(btnData['icon']),
            text=btnData['text'],
            width=80,
            height=60,
            corner_radius=10,
            fg_color="transparent",
            hover_color=("#f1f3f4", "#2b2b2b"),
            compound="top",
            font=ctk.CTkFont(size=12),
            command=lambda b=btnID: print(f"{b} button clicked")
        )
        btn.pack(side="left", expand=True)

def toggle_appearance_mode():
    current = ctk.get_appearance_mode()
    new_mode = "Dark" if current == "Light" else "Light"
    ctk.set_appearance_mode(new_mode)
    # ctk.set_default_color_theme("dark-blue" if new_mode == "dark" else "light-blue")
    modeBtn.configure(text=f"{current.capitalize()} Mode")
    modeBtn.configure(image=invert("dark") if current == "Dark" else invert("light"))

    rebuild_dock()

def toggle_task_completion(checkbox, taskText):
    if checkbox.get():
        taskText.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")
    else:
        taskText.configure(font=ctk.CTkFont(size=16), text_color=("black", "white"))

masterFrame = ctk.CTkFrame(app, fg_color="transparent")
masterFrame.pack(fill="both", expand=True, padx=10, pady=10)

header = ctk.CTkFrame(masterFrame, fg_color="transparent", height=50)
header.pack(fill="x", pady=(0, 10))

title = ctk.CTkLabel(header, text="Tasks", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(side="left", padx=10)


modeBtn = ctk.CTkButton(
    header,
    text="Dark Mode",
    text_color=("black", "white"),
    image=invert("dark"),
    width=40,
    height=40,
    corner_radius=20,
    fg_color="transparent",
    hover_color="#515151",
    command=toggle_appearance_mode
)
modeBtn.pack(side="right", padx=10)

addBtn = ctk.CTkButton(
    header,
    text="+",
    width=40,
    height=40,
    corner_radius=20,
    fg_color="#1a73e8",
    hover_color="#0d62c9",
    font=ctk.CTkFont(size=20),
    command=lambda: print("Add task button clicked")
)
addBtn.pack(side="right", padx=10)

tasksFrame = ctk.CTkScrollableFrame(masterFrame, fg_color="transparent")
tasksFrame.pack(fill="both", expand=True)

task_data = [
    {"name": "Buy groceries", "category": "🛒 Personal", "completed": False},
    {"name": "Finish report", "category": "💼 Work", "completed": True},
    {"name": "Call mom", "category": "👪 Family", "completed": False},
    {"name": "Gym workout", "category": "🏋️ Health", "completed": False},
    {"name": "Read book", "category": "📚 Learning", "completed": True},
    {"name": "Pay bills", "category": "💰 Finance", "completed": False},
]

for task in task_data:
    taskFrame = ctk.CTkFrame(tasksFrame, height=45, fg_color="transparent")
    taskFrame.pack(fill="x", pady=2)  
    
    checkbox = ctk.CTkCheckBox(
        taskFrame,
        text="",
        width=20,
        height=20,
        border_width=2
    )
    checkbox.pack(side="left", padx=(5, 10))
    
    textFrame = ctk.CTkFrame(taskFrame, fg_color="transparent")
    textFrame.pack(side="left", fill="x", expand=True)
    
    taskText = ctk.CTkLabel(
        textFrame,
        text=task["name"],
        font=ctk.CTkFont(size=16),
        anchor="w"
    )
    taskText.pack(fill="x")
    
    categoryLabel = ctk.CTkLabel(
        textFrame,
        text=task["category"],
        font=ctk.CTkFont(size=12),
        text_color="gray",
        anchor="w"
    )
    categoryLabel.pack(fill="x")
    
    checkbox.configure(
        command=lambda cb=checkbox, tt=taskText: toggle_task_completion(cb, tt)
    )
    
    if task["completed"]:
        checkbox.select()
        taskText.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")

dock = ctk.CTkFrame(app, height=70, corner_radius=0)
dock.pack(side="bottom", fill="x")

dock_buttons = {
    "home": {"icon": ("homeIcon"), "text": "Home"},
    "timer": {"icon": ("timerIcon"), "text": "Timer"}, 
    "settings": {"icon": ("settingsIcon"), "text": "Settings"}
}

for btnID, btnData in dock_buttons.items():
    btn = ctk.CTkButton(
        dock,
        image=invert(btnData['icon']),
        text=btnData['text'],
        width=80,
        height=60,
        corner_radius=10,
        fg_color="transparent",
        hover_color=("#f1f3f4", "#2b2b2b"),
        compound="top",
        font=ctk.CTkFont(size=12),
        command=lambda b=btnID: print(f"{b} button clicked")
    )
    btn.pack(side="left", expand=True)

app.mainloop()