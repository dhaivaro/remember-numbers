from tkinter import StringVar, Radiobutton, W, E  # Import required classes and constants
from tkinter import ttk
from memorazation import open_new_window

def create_initial_frame(root):
    """
    Create the initial main frame inside the root window.
    """
    mainframe = ttk.Frame(root, padding=(10, 10, 10, 10))
    mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))

    # Configure grid resizing
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(1, minsize=350)
    mainframe.columnconfigure(3, minsize=50)
    mainframe.rowconfigure(6, weight=1)

    # Variables for input fields
    min_range_val = StringVar()
    max_range_val = StringVar()
    numbers_count = StringVar()
    time_to_memorize = StringVar()
    var = StringVar()  # For Radiobuttons
    number_of_maths_tasks = StringVar(value="5")  # Set default value to 5

    # Set the default value for the radiobuttons
    var.set('XX')  # Pre-select the 'XX' radiobutton

    # Radiobuttons
    r1 = Radiobutton(mainframe, text='XX', variable=var, value='XX')  # Radiobutton 1
    r2 = Radiobutton(mainframe, text='XXX', variable=var, value='XXX')  # Radiobutton 2
    r1.grid(column=2, row=1, sticky=W)  # Place Radiobutton 1
    r2.grid(column=3, row=1, sticky=W, padx=(0, 5))  # Place Radiobutton 2

    # Entry fields
    min_range_val_entry = ttk.Entry(mainframe, width=5, textvariable=min_range_val)
    min_range_val_entry.grid(column=2, row=2, sticky=(W))

    max_range_val_entry = ttk.Entry(mainframe, width=5, textvariable=max_range_val)
    max_range_val_entry.grid(column=3, row=2, sticky=(W), padx=(0, 5))

    numbers_count_entry = ttk.Entry(mainframe, width=5, textvariable=numbers_count)
    numbers_count_entry.grid(column=2, row=4, columnspan=2, sticky=(W))

    time_to_memorize_entry = ttk.Entry(mainframe, width=5, textvariable=time_to_memorize)
    time_to_memorize_entry.grid(column=2, row=5, columnspan=2, sticky=(W))

    number_of_maths_tasks_entry = ttk.Entry(mainframe, width=5, textvariable=number_of_maths_tasks)
    number_of_maths_tasks_entry.grid(column=2, row=6, columnspan=2, sticky=(W))

    # Start button
    def start_memorization():
        try:
            min_val = int(min_range_val.get()) if min_range_val.get() else 1
            max_val = int(max_range_val.get()) if max_range_val.get() else 99
            count = int(numbers_count.get()) if numbers_count.get() else None
            duration = int(time_to_memorize.get()) if time_to_memorize.get() else 3
            number_type = var.get()  # Get selected radiobutton value
            math_tasks_count = int(number_of_maths_tasks.get()) if number_of_maths_tasks.get() else 5
            open_new_window(root, min_val, max_val, duration, count, number_type, math_tasks_count)
        except ValueError:
            pass  # Handle invalid input gracefully
    
    start_button = ttk.Button(mainframe, text="Start", command=start_memorization)
    start_button.grid(column=2, row=7, columnspan=2, sticky="S", pady=(20, 10))

    # Bind Enter key to start memorization
    root.bind('<Return>', lambda event: start_memorization())

        # Add padding to all child widgets of the mainframe
    for child in mainframe.winfo_children():
        if child.grid_info().get('column') != 3:
            child.grid_configure(padx=5, pady=5)
        else:
            child.grid_configure(pady=5)

    # Labels
    ttk.Label(mainframe, text="Numbers type (XX or XXX)").grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, text="Range of numbers").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Min").grid(column=2, row=3, sticky=W, pady=(0, 20))
    ttk.Label(mainframe, text="Max").grid(column=3, row=3, sticky=W, padx=(0, 5), pady=(0, 20))
    ttk.Label(mainframe, text="Count of numbers to memorize").grid(column=1, row=4, sticky=W)
    ttk.Label(mainframe, text="Count of seconds for one number").grid(column=1, row=5, sticky=W)
    ttk.Label(mainframe, text="Number of math tasks").grid(column=1, row=6, sticky=W)

    # Configure the grid to adjust dynamically
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(3, minsize=50)



    # Set focus on the first input field
    min_range_val_entry.focus()

    return mainframe