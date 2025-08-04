import customtkinter as ctk

def show_home(parent, username, on_timer, on_logout):
    # Remove all previous widgets from this frame
    for widget in parent.winfo_children():
        widget.destroy()

    # App Title
    title = ctk.CTkLabel(parent, text="Task Planner", font=ctk.CTkFont(size=22, weight="bold"))
    title.pack(pady=10)

    # Welcome
    user_label = ctk.CTkLabel(parent, text=f"Welcome, {username}!", font=ctk.CTkFont(size=16, weight="bold"))
    user_label.pack(pady=(5,15))

    # Example: Task section
    tasks_frame = ctk.CTkFrame(parent)
    tasks_frame.pack(fill="both", expand=True, padx=10, pady=5)
    ctk.CTkLabel(tasks_frame, text="Your Tasks:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10, pady=(5, 2))

    # Example static tasks - replace with your real task loading logic
    sample_tasks = [
        {"name": "Buy groceries", "category": "🛒 Personal", "completed": False},
        {"name": "Finish report", "category": "💼 Work", "completed": True},
        {"name": "Call mom", "category": "👪 Family", "completed": False},
        {"name": "Gym workout", "category": "🏋️ Health", "completed": False},
        {"name": "Read book", "category": "📚 Learning", "completed": True},
        {"name": "Pay bills", "category": "💰 Finance", "completed": False},
    ]
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
