import cv2
import tkinter as tk
import threading
import customtkinter as ctk
import PIL.Image, PIL.ImageTk
from typing import Optional
from lib.exceptions import ButtonAlreadyExists

class Window:
    def __init__(self,
                 WIN : ctk.CTk,
                 WIDTH : int,
                 HEIGHT : int,
                 APPEARANCE : str,
                 THEME : str) -> None:
        """
        Parameters
        ----------
        self._window : ctk.CTk
            The window object.
        self.width : int
            The width of the window created.
        self.height : int
            The height of the window created.
        self.mode : str
            The appearance color of the application.
        self.theme : str
            The theme color of the application.

        Variables
        ---------
        self.data : dict
            A dictonary containing all information about buttons creates and titles displayed on screen.
        """
        self.window = WIN
        self.width = WIDTH
        self.height = HEIGHT
        ctk.set_appearance_mode(APPEARANCE)
        ctk.set_appearance_mode(THEME)
        self.data: dict = {
            "Title": None,
            "btns": {}
        }

        # Open the video camera
        self.capture = cv2.VideoCapture(1)
        self.cam_frame = ctk.CTkFrame(self.window)
        self.cam_frame.pack(side=ctk.LEFT, anchor = ctk.CENTER)
        self.cam_frame.lift()
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.cam_frame, width = 640, height = 480)
        self.canvas.pack()  

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.zoom = 1
        #self.update()
        t = threading.Thread(target=self.update(), daemon=True)
        t.start()
        t.join()

    def get_zoom(self) -> int:
        return self.zoom
    
    def set_zoom(self, level):
        self.zoom = level

    def constract(self, title : str) -> None:
        """
        Creates the main window adds a title.

        Parameters
        ----------
        title : str
            A string which will serve as the window's title.
        """
        self.window.title(title)
        self.window.geometry(f'{self.width}x{self.height}')

    def header(self,
               text : str,
               font : Optional[list[str, int, str]] = ['Arial', 28, 'bold']) -> None:
        """
        Displays a title on the screen.

        Parameters
        ----------
        text : str
            The text that will be displayed.
        font : Optional[list[str, int, str]] = ['Arial', 28, 'bold']
            The style of the text. 
        """
        frame = ctk.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0, anchor=tk.N)
        T = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(family=f'<{font[0]}>', size=font[1], weight=font[2]))
        T.pack()
        self.data["Title"] = text

    def logger(self,
               state : str = 'disabled',
               side : str = 'BOTTOM',
               anchor : str ='se',
               area: tuple[int] = ()):
        """
        Creates a logger box.

        Parameters
        ----------
        state : str, optional
            The state (open or closed) the logger will be.
        side : str, optional
            The side where the textbox will be - [TOP BOTTOM LEFT RIGHT].
        anchor : str, optional 
            The anchor the textbox will be - [S N E W SE SW NE NW].
        area : tuple[int], optional
            A tupe with width and legth of the textbox - tuple values need to be integers.
        """
        # Create a Frame to hold the Text widget and the Scrollbar
        frame = ctk.CTkFrame(self.window)

        match side:
            case 'TOP':
                frame.pack(side=ctk.TOP, anchor=anchor)
            case 'BOTTOM':
                frame.pack(side=ctk.BOTTOM, anchor=anchor)
            case 'LEFT':
                frame.pack(side=ctk.LEFT, anchor=anchor)
            case 'RIGHT':
                frame.pack(side=ctk.RIGHT, anchor=anchor)
            case _:
                raise (
                    ValueError("Value should be a string and one of those: \"LEFT\", \"RIGHT\" \"TOP\", \"BOTTOM\".")
                    )

        if not area:
            t = ctk.CTkTextbox(frame, width=self.width // 6, height=self.height // 2.5, state=state, activate_scrollbars=True)
        else:
            t = ctk.CTkTextbox(frame, width=area[0], height=area[1], state=state, activate_scrollbars=True)
        
        t.pack()

        return t
    
    def add_btn(self, 
                text : str,
                width: int,
                height : int,
                event : Optional[object] = None,
                border_width : Optional[int] = 0,
                border_radius : Optional[int] = 8,
                possition : Optional[tuple[float, float, ctk.ANCHOR]] = (0.5, 0.5, ctk.CENTER),
                image : ctk.CTkImage = None) -> None:
        """
        Handles the creation of a button.

        Parameters
        ----------
        text : str
            The text that will be displayed on the button.
        width : int 
            The width of the button.
        height : int 
            THe height of the button.
        event : Optional[object] = None
            A funcntion that will be activated when the button will be clicked.
        border_width : Optional[int] = 0
            Border width.
        border_radius : Optional[int] = 8
            Border radius.
        possition : Optional[tuple[float, float, ctk.ANCHOR]] = (0.5, 0.5, ctk.CENTER),
            A tuple with the possiton of the button on the screen.
        image : ctk.CTkImage = None
            An image that will be added to the button
        
        Raises
        ------
        ButtonAlreadyExists
            If a given button's name is identical to an existing button's name.  
        """
        if text in self.data['btns'].keys():
            raise ButtonAlreadyExists("Button with the name {} already exists, please rename your button".format(text))
    
        button = ctk.CTkButton(master=self.window,
                                 width=width,
                                 height=height,
                                 border_width=border_width,
                                 corner_radius = border_radius,
                                 text=text,
                                 command=event,
                                 image=image)
        button.place(relx=possition[0], rely=possition[1], anchor=possition[2])

        self.data['btns'][str(text)] = {'possition' : possition, 'size' : (width, height), 'image' : image}
    
    def handle_logger_status(self, logger : ctk.CTkTextbox, status : str) -> None:
        """
        Handles the opening and closing of the logger.

        Parameters
        ----------
        logger : ctk.CTkTextbox
            A textbox object.
        status : str
            the status we wnat the logger ot be <opened/closed>
        """
        match status:
            case 'disabled':
                logger.configure(state='disabled')
            case 'normal':
                logger.configure(state='normal')
            case _:
                raise(ValueError(f"Value {status} is not defined.\nValues are: 'normal', 'disabled'. Values must be str type."))
    
    def config_settings_window(self):
        #raise NotImplementedError("function is not ready to use yet")
        settings_window = ctk.CTkToplevel(self.window)
        settings_window.title("Settings")
        settings_window.geometry(f"{self.width}x{self.height}")

    def return_to_main(self):
        raise NotImplementedError("function is not ready to use yet")
    
    def update(self):
        # Get a frame from the video source
        ret, frame = self.capture.read()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, None, fx=self.zoom, fy=self.zoom, interpolation=cv2.INTER_LINEAR)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
 
        self.window.after(self.delay, self.update)
