from tkinter import Toplevel, StringVar, Frame, Label
from tkinter import ttk

def open_check_results_numbers_window(root, numbers_count=None, memorized_numbers=None, number_type='XX'):
    """
    Create a new window for checking number memorization results.
    """
    # Default numbers count if not provided
    if numbers_count is None:
        numbers_count = 10
    
    if memorized_numbers is None:
        memorized_numbers = []  # Fallback if no numbers provided
    
    # Calculate columns and rows
    fields_per_column = 10
    columns = (numbers_count + fields_per_column - 1) // fields_per_column  # Ceiling division
    
    # Calculate window size based on columns and field widths
    base_width = 600
    max_number_width = len(str(numbers_count)) + 1  # +1 for the dot
    field_width = max_number_width * 8 + 30 + 20  # Label width + entry width + padding
    total_fields_width = columns * field_width + (columns - 1) * 5 + 40  # Fields + spacing + padding
    
    window_width = max(base_width, total_fields_width)
    window_height = 600  # Extra height for button and results
    
    # Create a new Toplevel window
    results_window = Toplevel(root)
    results_window.title("Check Results")
    results_window.geometry(f"{window_width}x{window_height}+450+450")

    # Add a new frame to the window
    results_frame = ttk.Frame(results_window, padding=(10, 10, 10, 10))
    results_frame.grid(column=0, row=0, sticky=("W"))

    # Configure grid resizing
    results_window.columnconfigure(0, weight=1)
    results_window.rowconfigure(0, weight=1)
    results_frame.columnconfigure(0, weight=1)

    # Title
    ttk.Label(results_frame, text="Number Memorization Check", font=("Arial", 16)).grid(
        column=0, row=0, columnspan=columns, sticky="", pady=20)
    
    # Create numbered input fields
    entries = []
    user_inputs = []
    
    # Calculate the width needed for the largest number label (moved here for consistency)
    max_number_width = len(str(numbers_count)) + 1  # +1 for the dot
    
    # Auto-focus function
    def auto_focus_next(current_index, entry_widget):
        """Move focus to next field when correct number of digits is entered"""
        def on_key_release(event):
            current_text = entry_widget.get().strip()
            # Determine required length based on number type
            required_length = 3 if number_type == 'XXX' else 2 if number_type == 'XX' else 1
            
            # Skip auto-focus for navigation keys
            if event.keysym in ['Tab', 'Shift_L', 'Shift_R', 'Left', 'Right', 'Up', 'Down', 'BackSpace', 'Delete']:
                return
            
            # Enforce length limit by truncating if too long
            if len(current_text) > required_length:
                truncated_text = current_text[:required_length]
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, truncated_text)
                current_text = truncated_text
            
            # If current text has reached required length and contains only digits
            if len(current_text) == required_length and current_text.isdigit():
                # Move to next field if available
                next_index = current_index + 1
                if next_index < len(entries):
                    entries[next_index].focus()
                    entries[next_index].select_range(0, 'end')  # Select all text in next field for easy overwrite
        
        return on_key_release
    
    # Input validation function
    def validate_numeric_input(char):
        """Allow only numeric input"""
        return char.isdigit()
    
    for i in range(numbers_count):
        col = i // fields_per_column
        row = (i % fields_per_column) + 1  # +1 to account for title row
        
        # Field label and entry
        field_frame = ttk.Frame(results_frame)
        field_frame.grid(column=col, row=row, sticky="W", padx=(0, 5), pady=2)
        
        # Create label with fixed width for alignment
        label_text = f"{i+1}.".ljust(max_number_width)
        ttk.Label(field_frame, text=label_text, font=("Arial", 10), width=max_number_width).grid(column=0, row=0, sticky="W")
        
        var = StringVar()
        user_inputs.append(var)
        
        # Register validation function
        vcmd = (results_window.register(validate_numeric_input), '%S')
        
        entry = ttk.Entry(field_frame, textvariable=var, width=8, validate='key', validatecommand=vcmd)
        entry.grid(column=1, row=0, sticky="W", padx=(2, 0))
        entries.append(entry)
        
        # Bind auto-focus functionality
        entry.bind('<KeyRelease>', auto_focus_next(i, entry))
    
    # Check Results button
    def check_user_results():
        correct = 0
        wrong = 0
        
        for i in range(len(memorized_numbers)):
            user_answer = user_inputs[i].get().strip()
            
            # Format expected answer based on number type
            if number_type == 'XXX':
                expected = f"{memorized_numbers[i]:03d}"
            elif number_type == 'XX':
                expected = f"{memorized_numbers[i]:02d}"
            else:
                expected = str(memorized_numbers[i])
            
            if user_answer == expected:
                correct += 1
            else:
                wrong += 1
        
        # Handle empty fields as wrong
        for i in range(len(memorized_numbers), numbers_count):
            if user_inputs[i].get().strip():
                wrong += 1
            else:
                wrong += 1
        
        total = len(memorized_numbers)
        percentage = (correct / total * 100) if total > 0 else 0
        
        results_text = f"{correct} correct | {wrong} wrong or missed | {percentage:.1f}% correct"
        results_label.config(text=results_text)
    
    check_button = ttk.Button(results_frame, text="Check Results", command=check_user_results)
    check_button.grid(column=0, row=fields_per_column + 2, columnspan=1, sticky=("W"), pady=20, padx=(0, 10))

    # Show correct results button
    def show_correct_results():
        # Get user answers
        user_answers = []
        for i in range(numbers_count):
            user_answers.append(user_inputs[i].get().strip())
        
        show_correct_numbers_window_with_comparison(root, numbers_count, memorized_numbers, user_answers, number_type)
    
    show_results_button = ttk.Button(results_frame, text="Show correct results", command=show_correct_results)
    show_results_button.grid(column=1, row=fields_per_column + 2, columnspan=2, sticky=("W"), pady=20, padx=(10, 0))

    root.bind('<Return>', lambda event: check_user_results())
    
    # Results display label (initially empty)
    results_label = ttk.Label(results_frame, text="", font=("Arial", 12))
    results_label.grid(column=0, row=fields_per_column + 3, columnspan=columns, sticky="", pady=10)
    
    # Set focus on first field
    if entries:
        entries[0].focus()

def show_correct_numbers_window(root, numbers_count, memorized_numbers, number_type='XX'):
    """
    Create a new window showing the correct number sequence.
    """
    # Calculate columns and rows
    fields_per_column = 10
    columns = (numbers_count + fields_per_column - 1) // fields_per_column
    
    # Calculate window size
    base_width = 600
    max_number_width = len(str(numbers_count)) + 1
    field_width = max_number_width * 8 + 30 + 20
    total_fields_width = columns * field_width + (columns - 1) * 5 + 40
    
    window_width = max(base_width, total_fields_width)
    window_height = 500
    
    # Create a new Toplevel window
    correct_window = Toplevel(root)
    correct_window.title("Correct Results")
    correct_window.geometry(f"{window_width}x{window_height}+500+500")

    # Add a new frame to the window
    correct_frame = ttk.Frame(correct_window, padding=(10, 10, 10, 10))
    correct_frame.grid(column=0, row=0, sticky=("W"))

    # Configure grid resizing
    correct_window.columnconfigure(0, weight=1)
    correct_window.rowconfigure(0, weight=1)
    correct_frame.columnconfigure(0, weight=1)

    # Title
    ttk.Label(correct_frame, text="Correct Number Sequence", font=("Arial", 16)).grid(
        column=0, row=0, columnspan=columns, sticky="", pady=20)
    
    # Display correct numbers
    for i in range(len(memorized_numbers)):
        col = i // fields_per_column
        row = (i % fields_per_column) + 1
        
        # Field label and display
        field_frame = ttk.Frame(correct_frame)
        field_frame.grid(column=col, row=row, sticky="W", padx=(0, 5), pady=2)
        
        # Create label with fixed width for alignment
        label_text = f"{i+1}.".ljust(max_number_width)
        ttk.Label(field_frame, text=label_text, font=("Arial", 16), width=max_number_width).grid(column=0, row=0, sticky="W")
        
        # Format and display correct number based on type
        if number_type == 'XXX':
            formatted_number = f"{memorized_numbers[i]:03d}"
        elif number_type == 'XX':
            formatted_number = f"{memorized_numbers[i]:02d}"
        else:
            formatted_number = str(memorized_numbers[i])
        
        ttk.Label(field_frame, text=formatted_number, font=("Arial", 16), width=8, relief="sunken", anchor="w").grid(column=1, row=0, sticky="W", padx=(2, 0))

def show_correct_numbers_window_with_comparison(root, numbers_count, memorized_numbers, user_answers, number_type='XX'):
    """
    Create a new window showing both correct numbers and user answers,
    with red outlines for incorrect or missed answers.
    """
    # Calculate columns and rows
    fields_per_column = 10
    columns = (numbers_count + fields_per_column - 1) // fields_per_column
    
    # Calculate window size (wider to accommodate both correct and user columns)
    base_width = 800
    max_number_width = len(str(numbers_count)) + 1
    field_width = max_number_width * 8 + 60 + 60 + 40  # Label + correct + user + padding
    total_fields_width = columns * field_width + (columns - 1) * 5 + 40
    
    window_width = max(base_width, total_fields_width)
    window_height = 600
    
    # Create a new Toplevel window
    comparison_window = Toplevel(root)
    comparison_window.title("Results Comparison")
    comparison_window.geometry(f"{window_width}x{window_height}+500+500")

    # Add a new frame to the window
    comparison_frame = ttk.Frame(comparison_window, padding=(10, 10, 10, 10))
    comparison_frame.grid(column=0, row=0, sticky=("NSEW"))

    # Configure grid resizing
    comparison_window.columnconfigure(0, weight=1)
    comparison_window.rowconfigure(0, weight=1)
    comparison_frame.columnconfigure(0, weight=1)

    # Title
    ttk.Label(comparison_frame, text="Results Comparison", font=("Arial", 16)).grid(
        column=0, row=0, columnspan=columns, sticky="", pady=20)
    
    # Create header row for each column
    for col in range(columns):
        header_frame = ttk.Frame(comparison_frame)
        header_frame.grid(column=col, row=1, sticky="W", padx=(0, 20), pady=(0, 10))
        
        # Headers
        ttk.Label(header_frame, text="", font=("Arial", 10, "bold"), width=max_number_width).grid(column=0, row=0, sticky="W")
        ttk.Label(header_frame, text="Correct", font=("Arial", 10, "bold"), width=10).grid(column=1, row=0, sticky="W", padx=(2, 10))
        ttk.Label(header_frame, text="Your Answer", font=("Arial", 10, "bold"), width=12).grid(column=2, row=0, sticky="W", padx=(2, 0))
    
    # Display comparison for each number
    for i in range(numbers_count):
        col = i // fields_per_column
        row = (i % fields_per_column) + 2  # +2 to account for title and header rows
        
        # Create main field frame
        field_frame = ttk.Frame(comparison_frame)
        field_frame.grid(column=col, row=row, sticky="W", padx=(0, 20), pady=2)
        
        # Number label
        label_text = f"{i+1}.".ljust(max_number_width)
        ttk.Label(field_frame, text=label_text, font=("Arial", 12), width=max_number_width).grid(column=0, row=0, sticky="W")
        
        # Determine correct answer
        if i < len(memorized_numbers):
            if number_type == 'XXX':
                correct_answer = f"{memorized_numbers[i]:03d}"
            elif number_type == 'XX':
                correct_answer = f"{memorized_numbers[i]:02d}"
            else:
                correct_answer = str(memorized_numbers[i])
        else:
            correct_answer = ""
        
        # User answer (ensure we don't go out of bounds)
        user_answer = user_answers[i] if i < len(user_answers) else ""
        
        # Check if answer is correct
        is_correct = (user_answer == correct_answer and correct_answer != "")
        is_missed = (user_answer == "" and correct_answer != "")
        
        # Display correct answer
        correct_label = ttk.Label(field_frame, text=correct_answer, font=("Arial", 12), 
                                width=10, relief="sunken", anchor="w")
        correct_label.grid(column=1, row=0, sticky="W", padx=(2, 10))
        
        # Display user answer with conditional styling
        if is_correct:
            # Correct answer - normal styling
            user_label = ttk.Label(field_frame, text=user_answer, font=("Arial", 12), 
                                 width=12, relief="sunken", anchor="w")
            user_label.grid(column=2, row=0, sticky="W", padx=(2, 0))
        else:
            # Incorrect or missed - create with red border using regular tkinter Frame
            user_frame = Frame(field_frame, bg="red", relief="solid", bd=2)
            user_frame.grid(column=2, row=0, sticky="W", padx=(2, 0))
            
            if is_missed:
                display_text = "(missed)"
            else:
                display_text = user_answer
            
            # Use regular tkinter Label for better color control
            user_label = Label(user_frame, text=display_text, font=("Arial", 12), 
                             width=12, anchor="w", bg="white", relief="flat")
            user_label.pack(padx=1, pady=1)
    
    # Summary statistics
    correct_count = sum(1 for i in range(min(len(memorized_numbers), len(user_answers))) 
                       if user_answers[i] == (f"{memorized_numbers[i]:03d}" if number_type == 'XXX' 
                                             else f"{memorized_numbers[i]:02d}" if number_type == 'XX' 
                                             else str(memorized_numbers[i])))
    total_count = len(memorized_numbers)
    missed_count = sum(1 for i in range(len(memorized_numbers)) 
                      if i >= len(user_answers) or user_answers[i] == "")
    wrong_count = total_count - correct_count
    percentage = (correct_count / total_count * 100) if total_count > 0 else 0
    
    summary_text = f"Results: {correct_count} correct | {wrong_count} wrong/missed | {percentage:.1f}% accuracy"
    ttk.Label(comparison_frame, text=summary_text, font=("Arial", 12, "bold")).grid(
        column=0, row=fields_per_column + 3, columnspan=columns, sticky="", pady=20)
