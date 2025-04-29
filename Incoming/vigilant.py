import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
import Interface

class Vigilant():
    """Used to monitor whether a file is added to the folder specified in the storage
    """    
    def __init__(self, navigator : object):
        """Creates an instance of a Vigilant, incorporating a watchdog Observer and FileSystemEventHandler.

        :param navigator: Navigator used to instruct the Vigilant and retreive necessary information from the storage
        :type navigator: navigator
        """        
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
        self.is_monitoring = False
        self.navigator = navigator
        self.folder = self.navigator.get_folder(True)
        self.src_paths = []
        self.lock = threading.Lock()
        self.event_handler.on_created = self.on_created
        #self._setup_event_handler()

    #def _setup_event_handler(self):
        #self.event_handler.on_created = self.on_created

    def start_monitoring(self) -> None:
        """Checks whether the path to the folder which is to be scanned is correct.
        Then, the Observer is started to watch for files being created.
        Also, a thread is initiated upon which the Observer carries out the monitorin, this is done on top of 
        the thread created by the Observer, as this enables the program to ensure the tkinter windows are updated
        solely from the main thread.
        """        
        if not os.path.exists(self.folder):
            print(f"Error: The directory {self.folder} does not exist.")
            self.navigator.ask_for_folder()
            return
        self.observer.schedule(self.event_handler, self.folder, recursive=False)
        self.observer_thread = threading.Thread(target=self.observer.start)
        self.observer_thread.start()
        
    def stop_monitoring(self) -> None:
        """Instructs the Observer to stop monitoring and joins the initiated thread.
        """        
        self.observer.stop()
        self.observer_thread.join()

    def on_created(self, event : FileCreatedEvent) -> None: 
        """Verifies that the file which is created is indeed a file.
        Then using the Lock, the Observer is instructed to stop monitoring and the observer_thread is joined.
        With the Lock the program ensures that the tkinter windows are updated strictly from the main thread.

        :param event: indicating a file has been created inside the specified folder
        :type event: FileCreatedEvent
        """        
        if event.is_directory:
            return 
        with self.lock:
            self.stop_monitoring()
            self.navigator.get_path(event.src_path)
        
    def change_folder(self, path : str) -> None :
        """Changes the foldr withc the Observer monitors

        :param path: path to the folder
        :type path: string
        """        
        self.folder = path         
            
    #def get_path(self) -> str:
    #    """_summary_

    #    :return: _description_
    #    :rtype: _type_
    #    """        
    #    return self.src_path
            
    
        

        

            


        