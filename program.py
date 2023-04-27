from PIL import Image
from datetime import datetime
from lib.setup import Window
import os
import tkinter as tk
import customtkinter as ctk

def scroll_to_bottom(text_widget : ctk.CTkTextbox) -> None:
    """
    Scrolls to the buttom of the textbox.

    Parameters
    ----------
    text_widget : ctk.CTkTextbox
        A textbox object.
    """
    text_widget.see(tk.END)

def set_type(window : object, text_widget : ctk.CTkTextbox, new_status : str = None) -> None:
    global STATUS
    """
    Sets the type of the type of the application - manual, semi-ato automatic.

    Parameters
    ----------
    window : tkinter.Tk
        The window we are working on.
    text_widget : tkinter.Text
        The entire logger object.
    new_status : str
        The new status for the application.
    """
    window.handle_logger_status(text_widget, 'normal')
    if not STATUS == new_status:
        STATUS = new_status
        text_widget.insert(ctk.END, f"Program is now in {STATUS} mode\n")
    else:
        text_widget.insert(ctk.END, f"Program is already in {STATUS} mode\n")

    window.handle_logger_status(text_widget, 'disabled')
    scroll_to_bottom(l)

def shoot(window : ctk.CTk, text_widget : ctk.CTkTextbox) -> None:
    """
    Turns on & off the laster

    Parameters
    ----------
    window : tkinter.Tk
        The window we are working on.
    text_widget : ctk.CTkTextbox
        The entire logger object.
    """
    global LASER_CONDITION
    window.handle_logger_status(text_widget, 'normal')
    if not LASER_CONDITION:
        LASER_CONDITION = True
        text_widget.insert(ctk.END, "Laser Activated\n")
    else:    
        LASER_CONDITION = False
        text_widget.insert(ctk.END, "Laser Deactivaed\n")

    window.handle_logger_status(text_widget, 'disabled')
    scroll_to_bottom(l)
    #CMD.toggle_laser()

def zoom_in(window : ctk.CTk, text_widget : ctk.CTkTextbox) -> None:
    """
    Handle the zoom in commnad.

    Parameters
    ----------
    window : tkinter.Tk
        The window we are working on.
    text_widget : ctk.CTkTextbox
        The entire logger object.
    """
    #Add command for zoom in
    window.handle_logger_status(text_widget, 'normal')
    zoom_level = main_window.get_zoom()

    if zoom_level > 2:
        text_widget.insert(ctk.END, f"Cannot zoom over level {zoom_level}\n")
        return
    main_window.set_zoom(zoom_level + 1)
    main_window.window.after(0, main_window.update, zoom_level + 1)

    text_widget.insert(ctk.END, f"Zoomed In, level {zoom_level + 1}\n")
    window.handle_logger_status(text_widget, 'disabled')

def zoom_out(window : ctk.CTk, text_widget : ctk.CTkTextbox) -> None: 
    """
    Handle the zoom out command. 

    Parameters
    ----------
    window : tkinter.Tk
        The window we are working on.
    text_widget : ctk.CTkTextbox
        The entire logger object.
    """
    #Add command for zoom out

    zoom_level = main_window.get_zoom()
    if zoom_level <= 1:
        text_widget.insert(ctk.END, f"Cannot zoom out less than level {zoom_level}\n")
        return 
    main_window.set_zoom(zoom_level - 1)
    
    window.handle_logger_status(text_widget, 'normal')
    text_widget.insert(ctk.END, f"Zoomed Out, level {zoom_level - 1}\n")
    window.handle_logger_status(text_widget, 'disabled')
    main_window.window.after(0, main_window.update, zoom_level - 1)

def handle_bind(window : ctk.CTk, key : tk.Event, text_widget: ctk.CTkTextbox):
    global IS_PRESSED, FLAG, ID, STATUS
    window.handle_logger_status(text_widget, 'normal')
    if STATUS == 'manual':
        if key.keysym == 'space':
            shoot(window, text_widget)
        elif key.keysym in ('q', 'Q'):
            zoom_out(window, text_widget)
        elif key.keysym in ('e', 'E'):
            zoom_in(window, text_widget)
        elif key.keysym in ('a', 'A'):
            if FLAG != 'left':
                if ID is not None:
                    text_widget.after_cancel(ID)
                FLAG = 'left'
                text_widget.insert(ctk.END, "Moving Left - Counter-Clockwise\n")
                def move_left():
                    print(1)
                    if FLAG == 'left':
                        # Schedule the next movement
                        global ID
                        ID = text_widget.after(100, move_left)
                # Schedule the first movement
                ID = text_widget.after(150, move_left)
        elif key.keysym in ['d', 'D']:
            if FLAG != 'right':
                # Stop any previous movement
                if ID is not None:
                    text_widget.after_cancel(ID)
                FLAG = 'right'
                text_widget.insert(ctk.END, "Moving Right - Clockwise\n")
                # Start moving right
                def move_right():
                    print(2)
                    if FLAG == 'right':
                        # Schedule the next movement
                        global ID
                        ID = text_widget.after(150, move_right)
                # Schedule the first movement
                ID = text_widget.after(150, move_right)
        else:
            text_widget.insert(ctk.END, f"Invalid key pressed: {key.keysym}\n")
    elif STATUS == 'semi-auto':
        if key.keysym == 'space':
            shoot(window, text_widget)

    scroll_to_bottom(l)
    window.handle_logger_status(text_widget, 'disabled')


def handle_release() -> None:
    """Handles the release of a key."""
    global IS_PRESSED, FLAG
    IS_PRESSED = False
    FLAG = None  # add this line to reset the FLAG variable

if __name__ == '__main__':
    STATUS = None
    LASER_CONDITION = False
    IS_PRESSED = False
    FLAG = None
    ID = None
    #ZOOM_LEVEL = 0

    settings_icon = ctk.CTkImage(dark_image=Image.open(os.path.join('assets', 'settings.png')),
                                light_image=Image.open(os.path.join('assets', 'settings.png')),
                                size=(30,30))

    root = ctk.CTk()

    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

    main_window = Window(root, WIDTH, HEIGHT, 'dark', 'dark-blue')
    
    main_window.constract("AntiBalloons system controls")
    main_window.header("AntiAir system controls")

    main_window.add_btn('Manual', 100, 50, possition=(0.42, 0.95, ctk.CENTER), event=lambda: set_type(main_window, l, 'manual'))
    main_window.add_btn('Semi-Auto', 100, 50, possition=(0.5, 0.95, ctk.CENTER), event=lambda: set_type(main_window, l, 'semi-auto'))
    main_window.add_btn('Automatic', 100, 50, possition = (0.58, 0.95, ctk.CENTER), event=lambda: set_type(main_window, l, 'automatic'))
    main_window.add_btn(None, 50, 50, possition=(0.01, 0.95, ctk.W), image=settings_icon, event= lambda: main_window.config_settings_window)

    l = main_window.logger(state="normal") # normal
    l.insert(ctk.END, 'Program initiated at : {}\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    main_window.handle_logger_status(l, 'disabled')
    set_type(main_window, l, 'manual')

    main_window.window.bind("<KeyPress>", lambda event: handle_bind(main_window, event, l))
    main_window.window.bind("<KeyRelease>", lambda event: handle_release())

    #main_window.video_capture()
    main_window.window.mainloop()

