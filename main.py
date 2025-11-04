from tkinter import Tk
from settings_page import create_initial_frame
from tkinter import font

def main():
    # Create the main application window
    root = Tk()
    root.title("Mnemonicon")
    root.geometry("600x400+300+300")  # Set size and position of the main window

    # Change the default font globally
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=14)  # Increase font size to 14
    root.option_add("*Font", default_font)  # Apply the font to all widgets

    # Create the initial main frame
    mainframe = create_initial_frame(root)

    # Start the application's event loop
    root.mainloop()

if __name__ == "__main__":
    main()