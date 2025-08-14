import customtkinter as ctk
from PIL import Image
import connector as conn

dark =  Image.open("assets/dark.png")
light = Image.open("assets/light.png")
dark = dark.resize(light.size)
# print(dark.size, light.size)

homeIcon = Image.open("assets/homeIcon.png")
homeDark = Image.open("assets/homeIcon_inverted.png").resize(homeIcon.size)
timerIcon = Image.open("assets/timerIcon.png").resize(homeIcon.size)
timerDark = Image.open("assets/timerIcon_inverted.png").resize(homeIcon.size)
settingsIcon = Image.open("assets/settingsIcon.png").resize(homeIcon.size)
settingsDark = Image.open("assets/settingsIcon_inverted.png").resize(homeIcon.size)
dockClick = None  

dock_buttons = {
        "home": { "text": "🏠"},
        "timer": { "text": "⏱"},
        "settings": { "text": "⚙️"}
    }

# def invert(icon):
#     current = ctk.get_appearance_mode()
#     if current == "Dark":
#         return ctk.CTkImage(Image.open(f"assets/{icon}.png"), size=(24, 24))
#     else:
#         return ctk.CTkImage(Image.open(f"assets/{icon}.png"), size=(24, 24))

dock = None
modeBtn = None

app = None  # Will be set in build_home


def build_home(window, username="User",onDockButtonClick=None):
    global dock, modeBtn, dock_buttons, app, dockClick
    dockClick = onDockButtonClick
    app = window

    masterFrame = ctk.CTkFrame(app, fg_color="transparent")
    masterFrame.pack(fill="both", expand=True, padx=10, pady=10)

    header = ctk.CTkFrame(masterFrame, fg_color="transparent", height=50)
    header.pack(fill="x", pady=(0, 10))

    title = ctk.CTkLabel(header, text=f"Welcome {username}", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(side="left", padx=10)

    modeBtn = ctk.CTkButton(
        header,
        text="Dark Mode",
        text_color=("black", "white"),
        width=40,
        height=40,
        corner_radius=20,
        fg_color="transparent",
        hover_color="#60acd2",
        command=toggle_appearance_mode
    )
    modeBtn.pack(side="right", padx=10)

    def taskAdder(name, category):
        # Create a new row in tasksFrame, just like for other tasks
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
            text=name,
            font=ctk.CTkFont(size=16),
            anchor="w"
        )
        taskText.pack(fill="x")

        categoryLabel = ctk.CTkLabel(
            textFrame,
            text=category,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        categoryLabel.pack(fill="x")

        checkbox.configure(
            command=lambda cb=checkbox, tt=taskText: toggle_task_completion(cb, tt)
        )

    addBtn = ctk.CTkButton(
        header,
        text="+ Add Task",
        width=40,
        height=40,
        corner_radius=20,
        fg_color="#1a73e8",
        hover_color="#0d62c9",
        font=ctk.CTkFont(size=20),
        command=lambda:addTask(app, taskAdder)
    )
    addBtn.pack(side="right", padx=10)


    


    tasksFrame = ctk.CTkScrollableFrame(masterFrame, fg_color="transparent")
    tasksFrame.pack(fill="both", expand=True)

    global task_data
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
            command=lambda b=btnID: onDockButtonClick(b) if onDockButtonClick else print(f"{b} button clicked")
        )
        btn.pack(side="left", expand=True)


def rebuild_dock():
    global dock
    dock.destroy()

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
            command=lambda b=btnID: dockClick(b) if dockClick else print(f"{b} button clicked")
        )
        btn.pack(side="left", expand=True)

def toggle_appearance_mode():
    current = ctk.get_appearance_mode()
    new_mode = "Dark" if current == "Light" else "Light"
    ctk.set_appearance_mode(new_mode)
    rebuild_dock()
    modeBtn.configure(text=f"{current.capitalize()} Mode")


    rebuild_dock()

def toggle_task_completion(checkbox, taskText):
    if checkbox.get():
        taskText.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")
    else:
        taskText.configure(font=ctk.CTkFont(size=16), text_color=("black", "white"))

def addTask(app,addCallback):
    ctk.set_appearance_mode("./assets/violet_theme.json")
    dialogBox = ctk.CTkToplevel(app)
    dialogBox.title("Add New Task")
    dialogBox.geometry("320x210")
    dialogBox.resizable(False, False)



    ctk.CTkLabel(dialogBox, text="Task Name:").pack(anchor="w", padx=20, pady=(20, 0))
    name = ctk.CTkEntry(dialogBox, width=260)
    name.pack(padx=20, pady=6)

    category_choices = list({task['category'] for task in task_data})
    category = ctk.StringVar(value=category_choices[0] if category_choices else "🗂 General")
    ctk.CTkLabel(dialogBox, text="Category:").pack(anchor="w", padx=20, pady=(8, 0))
    category_menu = ctk.CTkOptionMenu(dialogBox, variable=category, values=category_choices,fg_color="#a007ff",button_color="#a007ff",button_hover_color="#66009a",dropdown_fg_color="#ebebeb")
    category_menu.pack(padx=20, pady=6)

    # ctk.CTkLabel(dialogBox, text="Category:").pack(anchor="w", padx=20, pady=(8, 0))
    # category = ctk.CTkEntry(dialogBox, width=160)
    # category.pack(padx=20, pady=6)

    def add():
        nameEntry = name.get().strip()
        categoryEntry = category.get().strip() or "🗂 General"
        if nameEntry:
            task_data.append({"name": nameEntry, "category": categoryEntry, "completed": False})
            addCallback(nameEntry, categoryEntry)
            dialogBox.destroy()
        else:
            name.configure(placeholder_text="Task name required!")

    addBtn = ctk.CTkButton(dialogBox, text="Add", command=add)
    addBtn.pack(pady=10)
    name.focus()

