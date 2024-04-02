# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

from pathlib import Path
from ttkthemes import ThemedTk
from a5_gui import MainApp

def main():
    '''
    entry point of the program, run GUI
    '''
    main_gui = ThemedTk(theme='black')

    # 'title' assigns a text value to the Title Bar area of a window.
    main_gui.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main_gui.geometry("1000x900")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main_gui.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main_gui)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main_gui.update()
    main_gui.minsize(main_gui.winfo_width(), main_gui.winfo_height())
    id = main_gui.after(2000, app.check_new)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main_gui.mainloop()

if __name__ == "__main__":
    main()
