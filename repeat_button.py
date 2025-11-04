from tkinter import ttk

def add_repeat_button(mainframe, start_callback=None, check_callback=None):
    """
    Add the 'Check results' button to the main frame.
    """
    check_button = ttk.Button(mainframe, text="Check Results", command=check_callback)
    check_button.grid(column=1, row=9, sticky="S", pady=(0, 10), padx=(5, 10))