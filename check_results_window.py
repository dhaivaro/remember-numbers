from tkinter import Toplevel, StringVar
from tkinter import ttk
import random
from check_results_numbers import open_check_results_numbers_window

def open_check_results_window(root, numbers_count=None, displayed_numbers=None, math_tasks_count=5, number_type='XX'):
    """
    Create a new window for checking results with math tasks.
    """
    # Skip if no math tasks
    if math_tasks_count == 0:
        open_check_results_numbers_window(root, numbers_count, displayed_numbers, number_type)
        return
    
    # Create a new Toplevel window
    results_window = Toplevel(root)
    results_window.title("Check Results")
    results_window.geometry("600x500+450+450")  # Set size and position

    # Add a new frame to the window
    results_frame = ttk.Frame(results_window, padding=(10, 10, 10, 10))
    results_frame.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

    # Configure grid resizing
    results_window.columnconfigure(0, weight=1)
    results_window.rowconfigure(0, weight=1)
    results_frame.columnconfigure(1, weight=1)
    results_frame.rowconfigure(7, weight=1)

    # Generate math tasks
    tasks = []
    correct_answers = []
    for i in range(math_tasks_count):
        num1 = random.randint(1, 99)
        num2 = random.randint(1, 99)
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            answer = num1 + num2
            task_text = f"{num1} + {num2} = "
        else:
            # Ensure positive result for subtraction
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            task_text = f"{num1} - {num2} = "
        
        tasks.append(task_text)
        correct_answers.append(answer)

    # Variables and entries for user input
    user_inputs = []
    entries = []
    
    # Title
    ttk.Label(results_frame, text="Solve the Math Tasks", font=("Arial", 16)).grid(column=0, row=0, columnspan=3, pady=20)

    def validate_answer(index, max_index):
        """Validate the answer and enable next field if correct"""
        try:
            user_answer = int(user_inputs[index].get())
            if user_answer == correct_answers[index]:
                # Correct answer - enable next field
                if index < max_index - 1:
                    entries[index + 1].config(state='normal')
                    entries[index + 1].focus()
                else:
                    # All answers correct - automatically move to next page
                    results_window.destroy()
                    open_check_results_numbers_window(root, numbers_count, displayed_numbers, number_type)
                return True
            else:
                # Incorrect answer - keep next fields disabled
                return False
        except ValueError:
            return False

    # Create 5 math task fields
    for i in range(math_tasks_count):
        # Task label
        ttk.Label(results_frame, text=f"Task {i+1}: {tasks[i]}", font=("Arial", 12)).grid(
            column=0, row=i+1, sticky="W", padx=10, pady=10)
        
        # User input variable and entry
        var = StringVar()
        user_inputs.append(var)
        
        entry = ttk.Entry(results_frame, textvariable=var, width=10, state='disabled' if i > 0 else 'normal')
        entry.grid(column=1, row=i+1, sticky="W", padx=10, pady=10)
        entries.append(entry)
        
        # Bind validation to entry
        var.trace('w', lambda *args, idx=i: validate_answer(idx, math_tasks_count))

    # Enable first field
    if entries:
        entries[0].config(state='normal')
        entries[0].focus()
