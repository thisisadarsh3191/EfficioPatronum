import customtkinter as ctk
from customtkinter import ThemeManager as tm
import time
from threading import Thread
from home import dock_buttons


# Global variables
timer_running = False
start_time = 0
duration = 0
remaining_time = 0
timer_thread = None


def build_timer(app,onDockButtonClick=None):

    def create_input_frame(root):
        input_frame = ctk.CTkFrame(root, bg_color=("#ebebeb", "#242424"), fg_color=("#F0F0F0", "#242424"))
        input_frame.pack(pady=20)
        
        # Input controls
        hours_var = ctk.IntVar(value=0)
        minutes_var = ctk.IntVar(value=0)
        seconds_var = ctk.IntVar(value=0)

        ctk.CTkLabel(input_frame, text="Hours:").grid(row=0, column=0, padx=5)
    
        hours_value_label = ctk.CTkLabel(input_frame, text=str(hours_var.get()))
        hours_value_label.grid(row=0, column=2, padx=5)
        def update_hours(val):
            hours_var.set(str(int(float(val))))
            hours_value_label.configure(text=str(hours_var.get()))
        hours_slider = ctk.CTkSlider(input_frame, from_=0, to=23, number_of_steps=23, command=update_hours)
        hours_slider.grid(row=0, column=1, padx=5)
        hours_slider.set(0)

        ctk.CTkLabel(input_frame, text="Minutes:").grid(row=1, column=0, padx=5)
        minutes_value_label = ctk.CTkLabel(input_frame, text=str(minutes_var.get()))
        minutes_value_label.grid(row=1, column=2, padx=5)
        def update_minutes(val):
            minutes_var.set(str(int(float(val))))
            minutes_value_label.configure(text=str(minutes_var.get()))
        minutes_slider = ctk.CTkSlider(input_frame, from_=0, to=59, number_of_steps=59, command=update_minutes)
        minutes_slider.grid(row=1, column=1, padx=5)
        minutes_slider.set(0)

        ctk.CTkLabel(input_frame, text="Seconds:").grid(row=2, column=0, padx=5)
        seconds_value_label = ctk.CTkLabel(input_frame, text=str(seconds_var.get()))
        seconds_value_label.grid(row=2, column=2, padx=5)
        def update_seconds(val):
            seconds_var.set(str(int(float(val))))
            seconds_value_label.configure(text=str(seconds_var.get()))
        seconds_slider = ctk.CTkSlider(input_frame, from_=0, to=59, number_of_steps=59, command=update_seconds)
        seconds_slider.grid(row=2, column=1, padx=5)
        seconds_slider.set(0)

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
        canvas.delete("all")

        bgColor = "#242424" if ctk.get_appearance_mode() == "Dark" else "#ebebeb"
        textColor = "#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#000000"

        canvas.configure(bg=bgColor)
        
        center_x, center_y = 150, 150
        radius = 120
        line_width = 15
        
        canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline="#CCCCCC", 
            width=line_width
        )
        
        
        if progress > 0:
            start_angle = 90  
            extent = -360 * progress
            
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=extent,
                outline="#ff4444",
                width=line_width,
                style="arc"
            )
        
        canvas.create_text(
            center_x, center_y,
            text=time_str,
            font=("Arial", 24, "bold"),
            fill = textColor
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
        frame = ctk.CTkFrame(root,bg_color=("#ebebeb","#242424"), fg_color=("#F0F0F0", "#242424"))
        
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

    ctk.set_default_color_theme("./assets/red_theme.json")

    for widget in app.winfo_children():
        widget.destroy()

    # Create all frames
    input_frame = create_input_frame(app)
    timer_frame = ctk.CTkFrame(app)
    control_frame = create_control_buttons(app)


    # Timer display canvas
    timer_canvas = ctk.CTkCanvas(
        timer_frame,
        width=300,
        height=300,
        highlightthickness=0,
        bg = "#242424" if ctk.get_appearance_mode() == "Dark" else "#ebebeb"
    )
    timer_canvas.pack(pady=20)

    # Initially only show input frame
    input_frame.pack(pady=20)


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

    # onDockButtonClick = None  # Placeholder for dock button click handler
