import customtkinter as ctk
from PIL import Image

# Initialize app
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Task Planner")
app.geometry("500x700")
app.resizable(False, False)

def check(cb, tt, line,container):
    """Toggle strike-through visual effect"""
    container.update_idletasks() 
    if cb.get() == 1: 
        textWidth = tt.winfo_reqwidth()
        line.place(relx = 0.05, rely=0.5, width=textWidth)
        tt.configure(text_color="gray")
    else:
        line.place_forget()
        tt.configure(text_color=("black", "white"))


masterFrame = ctk.CTkFrame(app, fg_color="transparent")
masterFrame.pack(fill="both", expand=True, padx=10, pady=10)


topFrame = ctk.CTkFrame(masterFrame, fg_color="transparent", height=50)
topFrame.pack(fill="x", pady=(0, 10))

title = ctk.CTkLabel(topFrame, text="Tasks", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(side="left", padx=10)

plusBtn = ctk.CTkButton(
    topFrame,
    text="+",
    width=40,
    height=40,
    corner_radius=20,
    fg_color="#1a73e8",
    hover_color="#0d62c9",
    font=ctk.CTkFont(size=20),
    command=lambda:print("Add task button clicked")
)
plusBtn.pack(side="right", padx=10)


tasks = ctk.CTkScrollableFrame(masterFrame, fg_color="transparent")
tasks.pack(fill="both", expand=True)

# Sample
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

    checkbox = ctk.CTkCheckBox(
        taskFrame,
        text="",
        width=20,
        height=20,
        border_width=2
    )
    checkbox.pack(side="left", padx=(5, 10))
    
    textContainer = ctk.CTkFrame(taskFrame, fg_color="transparent")
    textContainer.pack(side="left", fill="x", expand=True)
    
    taskText = ctk.CTkLabel(
        textContainer,
        text=taskList[task]["name"],
        font=ctk.CTkFont(size=16),
        anchor="w"
    )
    taskText.pack(fill="x")
    
    strikeLine = ctk.CTkCanvas(
        textContainer,
        height=1,
        bg="gray",
        highlightthickness=0
    )
    
    checkbox.configure(
        command=lambda cb=checkbox, tt=taskText, sl=strikeLine,tc=textContainer: check(cb, tt, sl, tc)
    )
    
    if taskList[task]["completed"]:
        if taskList[task]["completed"]:
            checkbox.select()
            taskText.configure(text_color="gray")
            
            tasks.update_idletasks()
            
            textWidth = taskText.winfo_reqwidth()
            strikeLine.place(relx=0.05, rely=0.5,width=textWidth)

dock = ctk.CTkFrame(app, height=70, corner_radius=0)
dock.pack(side="bottom", fill="x")

for btn_text in ["Home", "Timer", "Settings"]:
    btn = ctk.CTkButton(
        dock,
        text=btn_text,
        width=80,
        height=60,
        corner_radius=10,
        fg_color="transparent",
        hover_color="#f1f3f4"
    )
    btn.pack(side="left", expand=True)

app.mainloop()