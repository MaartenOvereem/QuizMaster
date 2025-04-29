import tkinter as tk
from tkinter import filedialog
from PIL import Image
from .message import Message

class Popup(tk.Toplevel):
    """Acquires user-input in case of the addition of a new data point

    :param tk: inherits from the tkinter Toplevel class
    :type tk: tkinter Toplevel
    """    
    def __init__(self, navigator : object, clicked : str, scan : bool):
        """_summary_

        :param navigator: required main window for the tkinter Toplevel class
        :type navigator: navigator
        :param clicked: iid of the clicked item in the Treeview
        :type clicked: string
        :param scan: True if the popup is used acquire information on a document that has been monitored by the Vigilant
        :type scan: boolean
        """        
        super().__init__(navigator)
        self.title("User input")
        self.geometry("400x150")
        self.result = None
        self.navigator = navigator
        self.scan = scan
        self.directory = (clicked == "Directory")
        self.map = (clicked[0] == 'm')
        self.set = (clicked[0] == 's')
        self.question = (clicked[0] == 'q')
        self.manner = (clicked == "Manner")
        self.new_filename = ""
        self.file_path = ""
        
        if self.map or self.set or self.directory :                                                           #   
            self.new_filename_label = tk.Label(self, text="Enter new filename:")
            self.new_filename_label.pack(pady=(10, 5))
            
            self.filename_entry = tk.Entry(self)
            self.filename_entry.pack(pady=(0, 15), padx=20, expand=True) 

        button_frame = tk.Frame(self)
        button_frame.pack(pady=(10, 10), side="bottom") 
        
        # Constructor initiates different popup menus with different functionalities for each type of item
        if self.question:                                                                                     
            self.new_filename_label = tk.Label(self, text="Would you like to store a\nquestion or answer?") 
            self.new_filename_label.pack(pady=(10, 5))
            self.question_button = tk.Button(button_frame, text="Question", command=self._on_left)
            self.question_button.pack(side="left", padx=10)
            self.answer_button = tk.Button(button_frame, text="Answer", command=self._on_right)
            self.answer_button.pack(side="right", padx=10)
        elif self.set :                                                                                       
            self.question_button = tk.Button(button_frame, text="Ok", command=self._on_left)
            self.question_button.pack(side="bottom", padx=10)
        elif self.map or self.directory:                                                                      
            self.map_button = tk.Button(button_frame, text="Map", command=self._on_left)
            self.map_button.pack(side="left", padx=10)
            self.set_button = tk.Button(button_frame, text="Set", command=self._on_right)
            self.set_button.pack(side="right", padx=10)
        else :                                                                                                
            self.new_filename_label = tk.Label(self, text="Choose whether to enter a new file manually\nor employ the Scanner")
            self.new_filename_label.pack(pady=(10, 5))
            self.question_button = tk.Button(button_frame, text="Manual", command=self._on_left)
            self.question_button.pack(side="left", padx=10)
            self.answer_button = tk.Button(button_frame, text="Scan", command=self._on_right)
            self.answer_button.pack(side="right", padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
            
    def _on_left(self):
        """Should the user press left button, which indicates either a question or map for the type of document or 
        that the user wishes to add a new file path manually.
        """        
        self.result = True
        if self.map or self.set or self.directory:
            self.new_filename = self.filename_entry.get()
        self.destroy()

    def _on_right(self):
        """Should the user press right button, which indicates either an answer or set for the type of document or
        that the user wants to choose a file path by means of employing a Vgiliant.
        """        
        self.result = False
        if self.map or self.set or self.directory:
            self.new_filename = self.filename_entry.get()
            self.destroy()
        elif self.manner :
            if self.navigator.get_folder(True) == "":
                m = Message(self.navigator, "Please set the folder which ought to be monitored before scanning")
                response = m.show_message
                self.destroy()   
                return         
            self.answer_button.config(text="Stop Scanning")
            self.navigator.scan()
        elif self.question :
            self.destroy()
        
    def get_result(self) -> list:
        """Allows the Navigator and Directory to instruct the Popup to start up and wait for user input

        :return: whether the left-or right button is pressed, name of the file and file path (if applicable)
        :rtype: list
        """        
        self.wait_window()
        if self.new_filename == "" and not self.question:
            if self.map or self.set :
                return ["Nope"]
            else :
                return self.result
        if self.map or self.directory or self.scan:
            return [self.result, self.new_filename]
        else:
            path = self.get_path()
            return [self.result, self.new_filename, path]
        
        
    def get_path(self) -> str:
        """ Should the user opt for manually adding a file, this method opens a filedialog.
        Now, the user can choose a file from the computer's directory.
        The method checks whether the provided file is compatible with the program.
        Should this not be the case, a new window appears stating what went wrong and asking the user for new input.

        :return: path to the new file
        :rtype: string
        """        
        path = self.prepare_path(filedialog.askopenfilename())
        if path == "" :
            return
        else :
            try :
                Image.open(path)
            except :
                message = Message(f"The file you have chosen at {path} is of unvalid format for this application")
                fine = False
                while not fine :
                    fine = message.show_message()
                return self.get_path()
            return path
        
    def prepare_path(self, path : str) -> str:
        """Trims any excess tokens off the provided path, ensures the path start with "C" and ends with "g".
        This way, the program fully supports .png and .jpg files stored inside a Windows operating system.

        :param path: path possibly containging excess elements
        :type path: string
        :return: path which can be used by the program to display images
        :rtype: string
        """        
        first = ""
        second = ""
        found_C = False
        found_g = False
        for _ in path:
            if _ == "C":
                found_C = True
            if found_C:
                first =  first + _
        reversed = first[::-1]
        for _ in reversed:
            if _ == "g":
                found_g = True
            if found_g:
                second = second + _
        return second[::-1]
       
    def on_close(self) -> None:
        """If the menu is closed, the get_result  returns an empty string as the new filename and the default value
        for the type of data chosen.
        """                
        self.new_filename= ""
        self.destroy()

