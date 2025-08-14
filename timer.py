import customtkinter as ctk
import time
from threading import Thread

parent=ctk.CTk()

for widget in parent.winfo_children():
    widget.destroy()

# State tracking
timer_vars = {'running': False, 'start_time': None, 'duration': 0, 'remaining_time': 0, 'thread': None}

input_frame = ctk.CTkFrame(parent)
input_frame.pack(pady=20)

# Input controls
hours_var = ctk.IntVar(value=0)
ctk.CTkLabel(input_frame, text="Hours:").grid(row=0, column=0, padx=5)
hours_slider = ctk.CTkSlider(input_frame, from_=0, to=23, variable=hours_var, number_of_steps=23)
hours_slider.grid(row=0, column=1, padx=5)
ctk.CTkLabel(input_frame, textvariable=hours_var).grid(row=0, column=2, padx=5)

minutes_var = ctk.IntVar(value=0)
ctk.CTkLabel(input_frame, text="Minutes:").grid(row=1, column=0, padx=5)
minutes_slider = ctk.CTkSlider(input_frame, from_=0, to=59, variable=minutes_var, number_of_steps=59)
minutes_slider.grid(row=1, column=1, padx=5)
ctk.CTkLabel(input_frame, textvariable=minutes_var).grid(row=1, column=2, padx=5)

seconds_var = ctk.IntVar(value=0)
ctk.CTkLabel(input_frame, text="Seconds:").grid(row=2, column=0, padx=5)
seconds_slider = ctk.CTkSlider(input_frame, from_=0, to=59, variable=seconds_var, number_of_steps=59)
seconds_slider.grid(row=2, column=1, padx=5)
ctk.CTkLabel(input_frame, textvariable=seconds_var).grid(row=2, column=2, padx=5)

timer_frame = ctk.CTkFrame(parent)
control_frame = ctk.CTkFrame(parent)
timer_canvas = ctk.CTkCanvas(timer_frame, width=300, height=300, bg="#ffffff", highlightthickness=0)
timer_canvas.pack(pady=20)

def start_timer():
    timer_vars['duration'] = hours_var.get()*3600 + minutes_var.get()*60 + seconds_var.get()
    if timer_vars['duration'] > 0:
        input_frame.pack_forget()
        timer_frame.pack(pady=20)
        control_frame.pack(pady=10)
        timer_vars['running'] = True
        timer_vars['start_time'] = time.time()
        timer_vars['remaining_time'] = timer_vars['duration']
        update_timer_display()
        start_timer_thread()

def draw_circular_timer(progress, time_str):
    timer_canvas.delete("all")
    center_x, center_y = 150, 150
    radius = 120
    line_width = 15
    timer_canvas.create_oval(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        outline="#333333", width=line_width
    )
    if progress > 0:
        start_angle = 90
        extent = -360 * progress
        timer_canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=extent,
            outline="#ff0000", width=line_width, style="arc"
        )
    timer_canvas.create_text(center_x, center_y, text=time_str, font=("Arial", 24, "bold"), fill="#222")

def update_timer_display():
    if not timer_vars['running']:
        return
    elapsed = time.time() - timer_vars['start_time']
    timer_vars['remaining_time'] = max(0, timer_vars['duration'] - elapsed)
    progress = min(1.0, elapsed / timer_vars['duration']) if timer_vars['duration'] > 0 else 0.0
    hours = int(timer_vars['remaining_time'] // 3600)
    minutes = int((timer_vars['remaining_time'] % 3600) // 60)
    seconds = int(timer_vars['remaining_time'] % 60)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    draw_circular_timer(progress, time_str)
    if timer_vars['remaining_time'] <= 0:
        timer_vars['running'] = False
        draw_circular_timer(1.0, "Time's up!")
    else:
        timer_canvas.after(100, update_timer_display)

def start_timer_thread():
    if timer_vars['thread'] and timer_vars['thread'].is_alive():
        return
    timer_vars['thread'] = Thread(target=update_timer_display)
    timer_vars['thread'].daemon = True
    timer_vars['thread'].start()

def toggle_timer():
    if timer_vars['running']:
        timer_vars['running'] = False
        pause_resume_btn.configure(text="Resume")
    else:
        timer_vars['running'] = True
        timer_vars['start_time'] = time.time() - (timer_vars['duration'] - timer_vars['remaining_time'])
        update_timer_display()
        pause_resume_btn.configure(text="Pause")

def reset_timer():
    timer_vars['running'] = False
    timer_frame.pack_forget()
    control_frame.pack_forget()
    input_frame.pack(pady=20)

start_btn = ctk.CTkButton(input_frame, text="Start Timer", command=start_timer)
start_btn.grid(row=3, columnspan=3, pady=10)

pause_resume_btn = ctk.CTkButton(control_frame, text="Pause", command=toggle_timer)
pause_resume_btn.pack(side="left", padx=10)

reset_btn = ctk.CTkButton(control_frame, text="Reset", command=reset_timer)
reset_btn.pack(side="left", padx=10)

parent.mainloop()

