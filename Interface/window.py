import tkinter as tk
from PIL import Image as PILImage, ImageTk

class Window(tk.Toplevel):
    """Runs a quiz or showcases a specific question

    :param tk: inherits from tkinter Toplevel, meaning it is controlled from the main window, the Navigator
    :type tk: tkinter Toplevel
    """    
    
    def __init__(self, root : object, type : str, questions : list):
            """A Canvas and Scrollbar are initiated to display the images, the button is as of yet left empty.
            Finally, the show_question method is called to start either the quiz or showcase.

            :param root: Navigator object to which the Window is Toplevel
            :type root: navigator
            :param type: indicates whether the ibject is used for a quiz or showcase 
            :type type: string
            :param questions: dictionaries corresponding to the questions and answers which need to be shown
            :type questions: list
            """        
            super().__init__(root)
            self.type = type
            self.title(self.type)
            self.geometry = "1600x600"
            self.image_label = tk.Label(self)
            self.image_label.grid()
            
            self.canvas = tk.Canvas(self)
            self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scrollable_frame = tk.Frame(self.canvas)
        
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )

            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.scrollbar.grid(row=0, column=1, sticky="ns")

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
        
            self.protocol("WM_DELETE_WINDOW", self.destroy)
            
            self.next_button = ""
            self.index = 0
            if self.type == "Quiz":
                self.questions = list(filter(lambda x : x["answer"] != "", questions))      #filter out the questions for which there is no answer
            else:
                self.questions = questions
            
            self.show_question(self.questions[self.index])
       
    def show_question(self, pair : dict):
        """shows the images belonging to a question

        :param pair: contains the names and paths of the question and answer
        :type pair: dictionary
        """        
        self.next_button = tk.Button(self, text="Show Answer", command= lambda: self.show_answer(pair["answer_path"]))
        self.next_button.grid(row=1, column=0, columnspan=3, pady=20, sticky="ew")
        self.after_idle( lambda : self.process_image(list(filter(lambda x : x != "", pair["question_path"] ))))
            
    def show_answer(self, list):
        """shows the images belonging to an answer

        :param list: contains all the paths for the to-be-shown images
        :type list: list
        """        
        self.index = self.index + 1
        if self.index >= len(self.questions) :
            if self.type == "Quiz" :
                self.next_button = tk.Button(self, text="End Quiz", command=self.destroy)
            else:
                self.next_button = tk.Button(self, text="End Showcase", command=self.destroy)
        else:
            self.next_button = tk.Button(self, text="Next Question", command= lambda: self.show_question(self.questions[self.index]))
        self.after_idle(lambda : self.process_image(list))
        self.next_button.grid(row=1, column=0, columnspan=3, pady=20, sticky="ew")

    def process_image(self, list : list):
        """Uses the Pillow library to access the image stored at a specific path,
        converts it into the correct format so tkinter can work with it.
        Lastly, the image is displayed on the window.

        :param list: paths that need to be processed
        :type list: list
        """        
        try:
            for path in list:
                print(f"Loading image from: {path}")
                img = PILImage.open(path)
                img.thumbnail((800, 500))
                img_tk = ImageTk.PhotoImage(img)
                label = tk.Label(self.scrollable_frame, image=img_tk)
                label.image = img_tk
                label.pack(pady=10)
        except Exception as e:
            print(f"Failed to load image {path}: {e}")