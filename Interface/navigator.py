import tkinter as tk
from tkinter import Event, ttk
from tkinter import filedialog
import copy as c
from .window import Window
from .popup import Popup
from .message import Message
from Internal.directory import Directory
from Incoming.vigilant import Vigilant

class Navigator(tk.Tk):
    """Allows to be user to view and browse through all the items stored in the storage.
    On top of that, the user can add items and view the images stored in items where this is appropriate.
    Lastly, the option exists to change the folder the Vigilant monitors.

    :param tk: tkinter window, employs the main thread of the program
    :type tk: tkinter window
    """    
    def __init__(self):
        """Initiates all the relevant elements for the user to navigate the storage, these include amongst others:
        an Entry to search for specific items, a Treeview to facilitate the display of the nested structure of the storage.
        Lastly, the create_items method actually creates the items displayed in th Treeview.
        """        
        super().__init__()
        self.title("Manage thy Screenshots")
        self.geometry ="500x500"

        self.label = tk.Label(self, text="Type to search", font=("Helvetica", 8), fg="black")
        self.label.pack(padx=10, pady=5)

        self.entry = tk.Entry(self, font=("Helvetica", 12))
        self.entry.pack(padx=10, pady=7.5)
        self.entry.bind("<KeyRelease>", self.check)

        self.frame = tk.Frame(self)
        self.frame.pack(pady=15, fill="both", expand=True)

        self.listbox = tk.Listbox(self.frame, height=10, width=30)
        self.listbox.grid(row=0, column=0, padx=10, sticky="ns")

        self.tree_view = ttk.Treeview(self.listbox)
        self.tree_view.bind('<Button-3>', self.button_clicked)
        
        #Each item gets assigned a different popup menu, with different options depending in the type of item
        self.popup_d = tk.Menu()                                                        
        self.popup_d.add_command(label="Never Mind", command=self.popup_d.unpost)
        self.popup_d.add_command(label="Add here", command=self.add_map)
        self.popup_d.add_command(label="Change Folder", command=self.ask_for_folder)
        
        self.popup_1 = tk.Menu()                                                         
        self.popup_1.add_command(label="Never Mind", command= self.popup_1.unpost)
        self.popup_1.add_command(label="Add here", command=self.add_map)
        self.popup_1.add_command(label="Delete", command=self.delete)

        self.popup_2 = tk.Menu()                                                         
        self.popup_2.add_command(label="Never Mind", command=self.popup_2.unpost)
        self.popup_2.add_command(label="Show", command=self.show)
        self.popup_2.add_command(label="Add here", command=self.add_map)
        self.popup_2.add_command(label="Delete", command=self.delete)
        
        self.popup_3 = tk.Menu()                                                         
        self.popup_3.add_command(label="Never Mind", command= self.popup_3.unpost)
        self.popup_3.add_command(label="Quiz", command=self.start_quiz)
        self.popup_3.add_command(label="Add here", command=self.add_map)
        self.popup_3.add_command(label="Delete", command=self.delete)
        
        self.directory = Directory(self)
        self.vigilant = None
        self.path = None
        self.choice_1 = None
        self.choice_2 = None
        
        self.create_items()
        
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.mainloop()   

    def create_items(self) -> None :
        """Starts the recursion used to create the items. Here, the root items are created, for  each of which
        the method insert_child inserts its children and the children of the children etc.
        
        This method and insert_child make use of a custom code for the iid attribute of a Treeview item.
        Each code start with a letter, indicating either a map ('m'), set ('s') or question ('q'). Then, a '.' seperates 
        this letter and the place of the root item within the directory, indicated by a number larger or equal than 0.
        Then, this number and the number indicating the place of the child within the parent is seperated by another '.',
        upon which the place of the child follows etc.
        """        
        self.tree_view.delete(*self.tree_view.get_children())
        self.tree_view.insert('', 'end', text="Directory", iid="Directory")
        self.data = self.directory.get_data()
        iid = 0 
        for key in self.data.keys() :
            if isinstance(self.data[key], dict) :
                code = 'm.' + str(iid)
            else :
                code = 's.' + str(iid)
            parent = self.tree_view.insert(parent='', index='end', text=key, iid=code)
            self.insert_child(self.data[key], parent, str(iid))
            self.directory.update_look_up(code, key)
            iid = iid + 1
        self.tree_view.pack(pady=20)
        
    def insert_child(self, data : object, parent : object, parent_iid : str) -> None :
        """Continues the recursion intiated by  create_items, where the stopping condition is whether the data
        passed ot the method is of the list type. Should this be the case, the recursion is terminated

        :param data: all children of the parent for which the method is called
        :type data: dictionary or list
        :param parent: parent item to which the child belongs
        :type parent: object
        :param parent_iid: iid of the parent
        :type parent_iid: string
        """        
        iid = 0
        if not isinstance(data, list) : 
            for key in data.keys() :
                if isinstance(data[key], dict) :
                    code = 'm.' + parent_iid + '.' + str(iid)
                else :
                    code = 's.' + parent_iid + '.' + str(iid)
                child = self.tree_view.insert(parent=parent, index='end', text=key, 
                                              iid=code)
                self.insert_child(data[key], child, parent_iid + '.' + str(iid))
                self.directory.update_look_up(code, key)
                iid = iid + 1
        else :
            for item in data :
                code = 'q.' + parent_iid + '.' + str(iid)
                child = self.tree_view.insert(parent=parent, index='end', text=item["question"], 
                                              iid= code)
                self.directory.update_look_up(code, item)
                iid = iid + 1 
        
    def button_clicked(self, event: Event) -> None:
        """The appropriate popup menu appears, depending on which item receives the right-click.

        :param event: Indicates where the right-click occured on the GUI
        :type event: Event
        """        
        self.item = self.tree_view.identify_row(event.y)
        coors = self.tree_view.bbox(self.item)
        x, y, h, w = coors
        popup_x = self.tree_view.winfo_rootx() + x + w
        popup_y = y + h
        if self.item[0] == 'q' :
            self.popup_2.tk_popup(popup_x, popup_y)
        elif self.item == "Directory" :
            self.popup_d.tk_popup(popup_x, popup_y)
        elif self.item[0] == 's' :
            self.popup_3.tk_popup(popup_x, popup_y)
        else :
            self.popup_1.tk_popup(popup_x, popup_y)
            
    def check(self, e : Event) -> None:
        """Checks what the user entered into the search bar. Depending on the entered characters,
        the appropriate items in the storage are displayed. Should the user input correspond to a folder or set,
        all items placed inside these items are displayed as well.
        This is done by calling the insert_filtered_children method, for each of the first items in the storage,
        effectively starting a recursion.

        :param e: event indicating that the Entry widget has received input
        :type e: Event
        """        
        typed = self.entry.get().lower()
        self.tree_view.delete(*self.tree_view.get_children())
        if typed == "" :
            self.create_items()
        else :
            for key, value in self.data.items() :
                root = False
                parent = ""
                if typed in key.lower() :
                    root = True
                    parent = self.tree_view.insert("", "end", text=key)
                self.insert_filtered_children(parent, value, typed, root)

    def insert_filtered_children(self, parent : str, data : object, typed : str, previous : bool) -> None:
        """Continues the recursion initiated in the check method.
        Should the data passed to this method be of the list type, the recursion stops.
        
        :param parent: parent item from which the check or insert_filtered_children method is called
        :type parent: str
        :param data: contains all the children of the parent
        :type data: dictionary or list
        :param typed: user input
        :type typed: string
        :param previous: True if the parent fits the user input
        :type previous: boolean
        """        
        if not isinstance(data, list) :
            for key, value in data.items():
                next = False
                item = ""
                if typed in key.lower() or previous: 
                    next = True
                    item = self.tree_view.insert(parent, "end", text=key)
                self.insert_filtered_children(item, value, typed, next)
        else :
            for item in data :
                if typed in item["question"].lower() or previous:
                    item = self.tree_view.insert(parent, "end", text=item["question"])
            
    def add_map(self) -> None:
        """Acquires input from the user using a Popup Toplevel object. Depending on the type of the clicked item,
        Popups appear asking the user how he/she whishes to enter the file and the type of the file.
        Then, the Directory is instrcuted to add the new item to the storage.
        Lastly, the create_items method ensure that after the new item has been created, the GUI is updated.
        """
        
        #Adding to a map or the Directory can only be a set or map, hence the user does not need to specify
        #whether he/she would like to enter the file manually or via the Vigilant        
        if self.item[0] == "m" or self.item == "Directory":
            popup = Popup(self, self.item, False)
            info = popup.get_result()
            self.directory.add_map(self.item, info)
        
        #Should the clicked item be a set or question, the user needs to specify how the path to the image is to
        #be acquired, manually or via the Vigilant
        else :
            self.choice_1 = Popup(self, "Manner", False)
            manner = self.choice_1.get_result()
            self.choice_2 = Popup(self, self.item, not manner)
            info = self.choice_2.get_result()
            if self.item[0] == 'q' :
                info[1] = self.tree_view.item(self.item, "text")
            if not manner :
                info.append(self.path)
            self.directory.add_map(self.item, info)
        self.create_items()
        
    def scan(self) -> None:
        """Should the user indicate he/she whishes to enter a file path via the Vigilant,
        a Vigilant instance is created and instructed to start monitoring.
        """        
        # self.get_folder()
        self.vigilant = Vigilant(self)
        self.vigilant.start_monitoring()
    
    def stopped_scanning(self) -> None:
        """Instructs the Vigilant to stop scanning, own information is updated and the popup asking for the manner 
        in which a path is added is destroyed.
        """        
        self.vigilant.stop_monitoring()
        self.vigilant = None
        self.choice_1.destroy()
        
    def get_path(self, path : str) -> None:
        """Communicates with the Vigilant to pass the path of the newly created screenshot
        
        :param path: path to the newly created screenshot
        :type path: string
        """        
        self.stopped_scanning()
        if path is not None :
            self.path = path
        
    def choose_manner(self) -> list:
        """Creates a new Popup to ask the user how the path should be acquired, chosen from the laptop's directory
        or by instructing the Vigilant to stop monitoring.

        :return: boolean which indicates True if the user wants to add manually, 
                an emtpy string
        :rtype: list
        """        
        popup = Popup(self, "Manner", False)
        return popup.get_result()
    
    def show(self) -> None:
        """Shows the question and answer stored at a specific question item.
        """        
        self.window = Window(self, "Showcase", [self.directory.get_item(self.item)])
        
    def delete(self) -> None:
        """After asking the user whether they are sure they want to delete the specific item,
        the method instructs the Dierctory to remove the item from the storage.
        Should the user have indicated that the item ought to be removed,
        the create_items method updates the items displayed on the GUI.
        """        
        item = self.directory.get_item(self.item)
        if isinstance(item, dict) :
            name = item["question"] 
        else :
            name  = item
        message = Message(self, f"Are you sure you want me to get rid off {name}?")
        response = message.show_message()
        if response:
            self.directory.delete(item, self.item)
        else:
            return
        self.after_idle(self.create_items)
        
    def start_quiz(self) -> None:
        """Starts a quiz from the selected set by getting the relevant questions from the directory and passing them
        to a Window object
        """        
        questions = self.directory.get_place(self.item, True, False)
        Window(self, "Quiz", questions)
    
    def get_folder(self, check : bool) -> str:
        """Retreives the path to folder whch a Vigilant is supposed to monitor from the Directory. 
        Should there not be a folder present, the ask_for_folder method is called to prompt the user to choose one.

        :return: _description_
        :rtype: _type_
        """
        if(not check):        
            if self.directory.get_folder() == "" :
                message = Message(self, "please select a folder in which you want to be monitored")
                response = message.show_message()
                if(response):
                    self.ask_for_folder
                else:
                    return
        return self.directory.get_folder()
    
    def ask_for_folder(self) -> None:
        """ Opens a filedialog asking the user for a folder.
        Then, the path is passed to the Directory, which stores it inside the storage.
        """        
        folder_path = filedialog.askdirectory(title="Select a Folder")
        self.directory.change_folder(folder_path)
        
        
        
                
     
                
        