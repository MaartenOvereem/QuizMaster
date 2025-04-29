import tkinter as tk

class Message(tk.Toplevel):
    """Toplevel used to show a message to the user, ussually when a requirement for a certain action has not been
    meet with. 

    :param tk: inhertis from the tkinter Toplevel object, as it is instructed by the Navigator on the main loop
    :type tk: Toplevel
    """    
    def __init__(self, navigator : object, text : str):
        """Creates all the relevant features for the window to be operational.
        What stands out are the two sets of buttons, one set in case the Message is triggered by the user wanting 
        to delete an item.. The other is a generic "Ok" button, used when the user is simply shown a message.

        :param navigator: Navigator on the main loop, necessary for the Toplevel to function
        :type navigator: navigator
        :param text: text to be displayed on the window
        :type text: string
        """        
        super().__init__(navigator)
        self.text = text
        self.do_it = False
        self.title = "Message"
        self.geometry = "400x300"
        
        message_label = tk.Label(self, text=text, wraplength=350, font=("Arial", 12))
        message_label.grid(row=0, column=0, padx=20, pady=40)

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=(20, 40))

        if "rid" in self.text :
            yes_button = tk.Button(button_frame, text="Do it", command=self.yes)
            yes_button.pack(side="left", padx=10)

            no_button = tk.Button(button_frame, text="Maybe not", command=self.no)
            no_button.pack(side="right", padx=10)
        else :
            ok_button = tk.Button(button_frame, text="OK", command=self.yes)
            ok_button.pack()

        self.grid_columnconfigure(0, weight=1)
        
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
    def yes(self) -> None:
        """The user wants to delete the item, or has read the massage and agrees
        """        
        self.do_it = True
        self.destroy()
    
    def no(self) -> None:
        """The user does not want to delete the item
        """        
        self.do_it = False
        self.destroy()
        
    def show_message(self) -> bool:
        """Allows the Navigator to instruct the Message to show its message

        :return: whether the user does or does not want to delete the message, or the user has read the message
        :rtype: boolean
        """        
        self.wait_window()
        return self.do_it