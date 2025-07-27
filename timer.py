import customtkinter as ctk
import math
import time
from threading import Thread

# Global variables
timer_running = False
start_time = 0
duration = 0
remaining_time = 0
timer_thread = None

def create_input_frame(root):
    input_frame = ctk.CTkFrame(root)
    input_frame.pack(pady=20)
    
    # Hours selector
    hours_label = ctk.CTkLabel(input_frame, text="Hours:")
    hours_label.grid(row=0, column=0, padx=5)
    hours_var = ctk.IntVar(value=0)
    hours_slider = ctk.CTkSlider(input_frame, from_=0, to=23, variable=hours_var, number_of_steps=23)
    hours_slider.grid(row=0, column=1, padx=5)
    hours_display = ctk.CTkLabel(input_frame, textvariable=hours_var)
    hours_display.grid(row=0, column=2, padx=5)
    
    # Minutes selector
    minutes_label = ctk.CTkLabel(input_frame, text="Minutes:")
    minutes_label.grid(row=1, column=0, padx=5)
    minutes_var = ctk.IntVar(value=0)
    minutes_slider = ctk.CTkSlider(input_frame, from_=0, to=59, variable=minutes_var, number_of_steps=59)
    minutes_slider.grid(row=1, column=1, padx=5)
    minutes_display = ctk.CTkLabel(input_frame, textvariable=minutes_var)
    minutes_display.grid(row=1, column=2, padx=5)
    
    # Seconds selector
    seconds_label = ctk.CTkLabel(input_frame, text="Seconds:")
    seconds_label.grid(row=2, column=0, padx=5)
    seconds_var = ctk.IntVar(value=0)
    seconds_slider = ctk.CTkSlider(input_frame, from_=0, to=59, variable=seconds_var, number_of_steps=59)
    seconds_slider.grid(row=2, column=1, padx=5)
    seconds_display = ctk.CTkLabel(input_frame, textvariable=seconds_var)
    seconds_display.grid(row=2, column=2, padx=5)
    
    # Start button
    def start_timer():
        global duration, timer_running, start_time, remaining_time
        
        # Calculate total duration in seconds
        hours = hours_var.get()
        minutes = minutes_var.get()
        seconds = seconds_var.get()
        duration = hours * 3600 + minutes * 60 + seconds
        
        if duration > 0:
            # Hide input frame
            input_frame.pack_forget()
            
            # Show timer frame
            timer_frame.pack(pady=20)
            control_frame.pack(pady=10)
            
            # Start the timer
            timer_running = True
            start_time = time.time()
            remaining_time = duration
            update_timer_display()
            start_timer_thread()
    
    start_button = ctk.CTkButton(input_frame, text="Start Timer", command=start_timer)
    start_button.grid(row=3, columnspan=3, pady=10)
    
    return input_frame

def draw_circular_timer(canvas, progress, time_str):
    canvas.delete("all")  # Clear previous drawings
    
    # Circle dimensions
    center_x, center_y = 150, 150
    radius = 120
    line_width = 15
    
    # Draw background circle (gray)
    canvas.create_oval(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        outline="#333333", width=line_width
    )
    
    # Draw progress arc (red)
    if progress > 0:
        start_angle = 90  # Start at the top (12 o'clock position)
        extent = -360 * progress  # Negative for clockwise direction
        
        canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=extent,
            outline="#ff0000", width=line_width,
            style="arc"
        )
    
    # Draw time text in center
    canvas.create_text(
        center_x, center_y,
        text=time_str,
        font=("Arial", 24, "bold"),
        fill="#ffffff"
    )

def update_timer_display():
    global remaining_time, timer_running
    
    if not timer_running:
        return
    
    # Calculate remaining time
    elapsed = time.time() - start_time
    remaining_time = max(0, duration - elapsed)
    
    # Update circular progress
    progress = min(1.0, elapsed / duration) if duration > 0 else 0.0
    
    # Format time string
    hours = int(remaining_time // 3600)
    minutes = int((remaining_time % 3600) // 60)
    seconds = int(remaining_time % 60)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Draw timer with centered text
    draw_circular_timer(timer_canvas, progress, time_str)
    
    # Check if timer finished
    if remaining_time <= 0:
        timer_running = False
        draw_circular_timer(timer_canvas, 1.0, "Time's up!")
    else:
        # Schedule next update
        timer_canvas.after(100, update_timer_display)

def start_timer_thread():
    global timer_thread
    timer_thread = Thread(target=update_timer_display)
    timer_thread.daemon = True
    timer_thread.start()

def reset_timer():
    global timer_running
    timer_running = False
    
    # Hide timer and control frames
    timer_frame.pack_forget()
    control_frame.pack_forget()
    
    # Show input frame again
    input_frame.pack(pady=20)

def create_control_buttons(root):
    frame = ctk.CTkFrame(root)
    
    # Pause/Resume button
    def toggle_timer():
        global timer_running, start_time
        if timer_running:
            timer_running = False
            pause_resume_button.configure(text="Resume")
        else:
            timer_running = True
            start_time = time.time() - (duration - remaining_time)
            update_timer_display()
            pause_resume_button.configure(text="Pause")
    
    pause_resume_button = ctk.CTkButton(frame, text="Pause", command=toggle_timer)
    pause_resume_button.pack(side="left", padx=10)
    
    # Reset button
    reset_button = ctk.CTkButton(frame, text="Reset", command=reset_timer)
    reset_button.pack(side="left", padx=10)
    
    return frame

# Main application
root = ctk.CTk()
root.title("Circular Timer")
root.geometry("500x600")
ctk.set_default_color_theme("./assets/timerStyles.json")
# Create all frames
input_frame = create_input_frame(root)
timer_frame = ctk.CTkFrame(root)
control_frame = create_control_buttons(root)

# Timer display canvas
timer_canvas = ctk.CTkCanvas(timer_frame, width=300, height=300, bg="#ffffff", highlightthickness=0)
timer_canvas.pack(pady=20)

# Initially only show input frame
input_frame.pack(pady=20)

root.mainloop()