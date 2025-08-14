import customtkinter as ctk

def add_task(parent,taskName,category):
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Add Task")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.grab_set()

    ctk.CTkLabel(dialog, text="Task Name:").pack(pady=(10, 0))
    nameEntry = ctk.CTkEntry(dialog,width=250)
    nameEntry.pack(pady=5)

    ctk.CTkLabel(dialog, text="Category:").pack(pady=(10, 0))
    categories = ["🛒 Personal", "💼 Work", "👪 Family", "🏋️ Health", "📚 Learning", "💰 Finance"]

    dropdown = ctk.CTkComboBox(dialog, values=categories)
    dropdown.set("Select Category")
    dropdown.pack(pady=5)

    def submit():
        name = nameEntry.get().strip()
        category = dropdown.get()
        if name:
            dialog.destroy()
            on_submit(name, category)
            

sample_tasks = [
        {"name": "Buy groceries", "category": "🛒 Personal", "completed": False},
        {"name": "Finish report", "category": "💼 Work", "completed": True},
        {"name": "Call mom", "category": "👪 Family", "completed": False},
        {"name": "Gym workout", "category": "🏋️ Health", "completed": False},
        {"name": "Read book", "category": "📚 Learning", "completed": True},
        {"name": "Pay bills", "category": "💰 Finance", "completed": False},
    ]

def show_home(parent, username, on_timer, on_logout):
    for widget in parent.winfo_children():
        widget.destroy()

    addTask = ctk.CTkButton(
    parent, 
    text="Add Task", 
    width=100, 
    command=  # Replace with your actual add task function
)
    
    addTask.place(relx=1.0, y=10, anchor="ne")  # Position at top right with some padding


    title = ctk.CTkLabel(parent, text="Efficio Patronum", font=ctk.CTkFont(size=22, weight="bold"))
    title.pack(pady=10)

    userLabel = ctk.CTkLabel(parent, text=f"Welcome, {username}!", font=ctk.CTkFont(size=16, weight="bold"))
    userLabel.pack(pady=(5,15))

    tasks_frame = ctk.CTkFrame(parent)
    tasks_frame.pack(fill="both", expand=True, padx=10, pady=5)
    ctk.CTkLabel(tasks_frame, text="Your Tasks:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10, pady=(5, 2))

    
    for task in sample_tasks:
        frame = ctk.CTkFrame(tasks_frame, fg_color="transparent")
        frame.pack(fill="x", pady=2, padx=10)
        cb = ctk.CTkCheckBox(frame, text="", width=20, height=20)
        cb.pack(side="left", padx=(5, 10))
        txt = ctk.CTkLabel(frame, text=task["name"], font=ctk.CTkFont(size=16), anchor="w")
        txt.pack(side="left", fill="x", expand=True)
        cat = ctk.CTkLabel(frame, text=task["category"], font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        cat.pack(side="left", padx=7)

        if task["completed"]:
            cb.select()
            txt.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")
        def toggle_cb(checkbox=cb, taskText=txt):
            if checkbox.get():
                taskText.configure(font=ctk.CTkFont(size=16, overstrike=True), text_color="gray")
            else:
                taskText.configure(font=ctk.CTkFont(size=16), text_color=("black", "white"))
        cb.configure(command=toggle_cb)

    # Buttons for navigation
    bottom_frame = ctk.CTkFrame(parent, fg_color="transparent")
    bottom_frame.pack(fill="x", pady=5)

    ctk.CTkButton(bottom_frame, text="Timer", command=on_timer).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(bottom_frame, text="Logout", fg_color="red", command=on_logout).pack(side="right", padx=10, pady=10)
