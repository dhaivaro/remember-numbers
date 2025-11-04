from tkinter import Toplevel, StringVar
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
        entry = ttk.Entry(field_frame, textvariable=var, width=8)
        entry.grid(column=1, row=0, sticky="W", padx=(2, 0))
        entries.append(entry)
    
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
        show_correct_numbers_window(root, numbers_count, memorized_numbers, number_type)
    
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
