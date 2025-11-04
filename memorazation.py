from tkinter import Toplevel
from tkinter import ttk
import random
import time
import threading
from check_results_window import open_check_results_window
from check_results_numbers import open_check_results_numbers_window

def open_new_window(root, min_range=10, max_range=99, time_duration=3, numbers_count=None, number_type='XX', math_tasks_count=5):
    """
    Create a new window (Toplevel) and add a new frame to it.
    Display random numbers from range for set duration.
    """
    # Create a new Toplevel window
    new_window = Toplevel(root)
    new_window.title("Memorization Window")
    new_window.geometry("600x400+400+400")  # Set size and position of the new window

    # Add a new frame to the new window
    new_mainframe = ttk.Frame(new_window, padding=(10, 10, 10, 10))
    new_mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

    # Configure grid resizing for the new window
    new_window.columnconfigure(0, weight=1)
    new_window.rowconfigure(0, weight=1)
    new_mainframe.rowconfigure(9, weight=1)
    new_mainframe.columnconfigure(1, weight=1)

    # Create number display label
    number_display = ttk.Label(new_mainframe, text="", font=("Arial", 64))
    number_display.grid(column=1, row=4, sticky="", pady=50)

    # Generate random numbers without repetition
    numbers_list = list(range(min_range, max_range + 1))
    random.shuffle(numbers_list)
    
    # Limit to numbers_count if specified
    if numbers_count and numbers_count < len(numbers_list):
        numbers_list = numbers_list[:numbers_count]

    # Store the numbers for results checking
    displayed_numbers = numbers_list.copy()

    def display_numbers():
        """Display numbers sequentially with time delay"""
        for number in numbers_list:
            if new_window.winfo_exists():
                if number_type == 'XXX':
                    formatted_number = f"{number:03d}"  # Format as 3 digits with leading zeros
                elif number_type == 'XX':
                    formatted_number = f"{number:02d}"  # Format as 2 digits with leading zeros
                else:
                    formatted_number = str(number)
                number_display.config(text=formatted_number)
                new_window.update()
                time.sleep(time_duration)
            else:
                break
        
        if new_window.winfo_exists():
            number_display.config(text="Session Complete!", font=("Arial", 24))
            # Automatically redirect to check results after 2 seconds
            new_window.after(1000, lambda: check_results(new_window, numbers_count, displayed_numbers, math_tasks_count, number_type))

    # Start displaying numbers in a separate thread
    thread = threading.Thread(target=display_numbers)
    thread.daemon = True
    thread.start()

    # Display settings information at the bottom
    settings_text = f"Range: {min_range}-{max_range} | Count: {numbers_count if numbers_count else 'All'} | Duration: {time_duration}s"
    settings_label = ttk.Label(new_mainframe, text=settings_text, font=("Arial", 10))
    settings_label.grid(column=1, row=9, sticky="S", pady=(0, 10), padx=(0, 20))

def restart_session(mainframe, number_display, min_range, max_range, time_duration, numbers_count=None, number_type='XX'):
    """Restart the number display session"""
    # Reset font to original size
    number_display.config(font=("Arial", 64))
    
    numbers_list = list(range(min_range, max_range + 1))
    random.shuffle(numbers_list)
    
    # Limit to numbers_count if specified
    if numbers_count and numbers_count < len(numbers_list):
        numbers_list = numbers_list[:numbers_count]
    
    def display_numbers():
        for number in numbers_list:
            if mainframe.winfo_exists():
                if number_type == 'XXX':
                    formatted_number = f"{number:03d}"  # Format as 3 digits with leading zeros
                elif number_type == 'XX':
                    formatted_number = f"{number:02d}"  # Format as 2 digits with leading zeros
                else:
                    formatted_number = str(number)
                number_display.config(text=formatted_number, font=("Arial", 64))
                mainframe.update()
                time.sleep(time_duration)
            else:
                break
        
        if mainframe.winfo_exists():
            number_display.config(text="Session Complete!", font=("Arial", 24))
    
    thread = threading.Thread(target=display_numbers)
    thread.daemon = True
    thread.start()

def check_results(memorization_window, numbers_count, displayed_numbers, math_tasks_count, number_type):
    """Handle check results button click"""
    # Get the root window from the current mainframe
    import tkinter as tk
    root = tk._default_root
    memorization_window.destroy()  # Close the memorization window
    
    # Skip math tasks if count is 0
    if math_tasks_count == 0:
        open_check_results_numbers_window(root, numbers_count, displayed_numbers, number_type)
    else:
        open_check_results_window(root, numbers_count, displayed_numbers, math_tasks_count, number_type)



