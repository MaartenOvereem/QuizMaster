import json
import copy as c
import os
import sys
import Interface


class Directory():
    """ Used to manage what goes into the storage.JSON file.
    Also, whenever data is needed the Directory fetches it.
    """           

    def __init__(self, navigator):
        """A Directory holds the path to the storage, a reference to the data, a Navigator and empty instances
        of the data points which are used for storage.

        :param navigator: Navigator object used by the user of the application
        
        The constructor holds empty instances of each data type,
        alongside a dictionary used to store the combination of iid and item names.
        """ 
        
        # Change path based on whether running in .exe or .py
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
            exe_dir = os.path.dirname(exe_path)
            parts = exe_dir.split(os.sep)

            parts[-1] = "Internal"
            base_path = os.path.join(*parts)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.storage = os.path.join(base_path, "storage.JSON")
        self.data = self.get_data()
        self.navigator = navigator
        self.look_up = dict()
        self.map = {}
        self.set = []
        self.point = { "question" : "",
                    "question_path" : [], 
                    "answer" : "", 
                    "answer_path": [],
        }

    def store_question(self, name : str, path : str, match : list) -> None:
        """Used to store a question by preparing the point depending on whether a new question is stored
        or a path is added to an existing one. 
        Then, into_storage is called to 
        store the new point.

        :param name: name of question to be stored
        :type name: string
        :param path: path to image
        :type path: string
        :param match: keys which lead to the question inside the storage.JSON
        :type match: list
        """        
        if isinstance(match[len(match) - 1], dict) :    #Path is added to an existing question
            copy = c.deepcopy(match.pop())
        else  :
            copy = c.deepcopy(self.point)               #New question is added
        copy["question"] = name
        copy["question_path"].append(path)
        self.into_storage(True, False, copy, match)

    def into_storage(self, question : bool, map : bool, point : object, place : list) -> None:
        """Used to intitiate navigate_down to change the data at the location, place, into point.
        Then, write_data writes the new data into the storgae.JSON file.

        :param question: point to be stored is a question or answer
        :type question: boolean
        :param map: point to be stored is a map or a set
        :type map: boolean
        :param point: the new point which is to be added to / changed in the data
        :type point: list / dictionary 
        :param place: keys which lead to the value which needs to be changed inside the storage
        :type place: list
        """        
        index = 0
        self.data = self.navigate_down(question, map, index, point, place, self.get_data())
        self.write_data(self.data)

    def store_answer(self, name : str,  path : str, match : list) -> None:
        """Used to prepare a new answer depending onw whether it is a new answer or it is added to an
        existing one. Then, into_storage is used to store the point.

        :param name: name of the answer
        :type name: string
        :param path: path where the image is stored
        :type path: string
        :param match: keys leading to the answer inside storage.JSON
        :type match: list
        """        
        point = c.deepcopy(match[len(match) - 1])
        point["answer"] = name
        point["answer_path"].append(path)
        self.into_storage(False, False, point, match)   
            
    def add_map(self, iid : str, info : list) -> None:
        """Used for interaction with the GUI, prepares the input iid from the Treeview and 
        info from the Popup so the Directory can store the incoming data.

        :param iid: unique iid of the item selected by the user
        :type iid: string
        :param info: information added by the user on the new data
        :type info: list
        """        
        if iid == "Directory" :
            place = {}
        else :
            place = self.get_place(iid, False, False)
        if info[0] == "Nope" :
            return
        if len(info) == 3 :                                       #user information as retreived by the Popup  
            if info[2] is None :
                place.pop()
                return 
            elif info[0] :
                self.store_question(info[1], info[2], place)
            else:
                self.store_answer(info[1], info[2], place)
        else :
            self.into_storage(False, info[0], info[1], place)
    
    def delete(self, item : object, iid : str) -> None :
        """Sets up the call to the into_storage method, such that the specifiec item is deleted
            from the database.

        :param item: daa point to be deleted
        :type item: string / dict
        :param iid: iid of the item, used to retreive the data inside the storage which stores the item
                    and the keys which lead to this specific data.
        :type iid: string
        """        
        place = self.get_place(iid, True, True)
        list = self.get_place(iid, False, True)
        if isinstance(item, dict):                                  # In case a question is to be deleted  
            place.remove(item)
            self.into_storage(False, False, place, list)
        else:                                                       # In case a set or map is to be deleted
            place.pop(item)
            self.into_storage(False, True, place, list)
        
    def navigate_down(self, question : bool, map : bool, index : int, point : object, 
                      place : list, data : object) -> object:
        """Recursively goes down the stored data in order to access the data stored at a specific key,
            the road to which is specified by place. Then, point is used to ammend this specific subset of the data.

        :param question: point to be ammended is a question or answer
        :type question: boolean
        :param map: point to be ammended is a map or set
        :type map: boolean
        :param index: facilitates accessing different items in the place list 
        :type index: integer
        :param point: changed data 
        :type point: dict / list
        :param place: road to the subset of the data where point is to be stored
        :type place: list
        :param data: data at specific key, changes with the recursion
        :type data: dict / list
        :return: the ammended data if stopping condition has been reached, 
                or another call to the recursive function.
        :rtype: dict / list
        """        
        if index == len(place) - 1 or len(place) == 0: # stop the recursion at the last element of place, or do not begin when something is the be added to the Directory directly
            if question:                                                        
                already = False                                      #add a new question
                for _ in data[place[index]] :
                    if _["question"] == point["question"]:
                        _["question_path"] = point["question_path"]
                        already = True
                if not already:                                     #add to an existing question
                    data[place[index]].append(point)
                return data
            elif map :
                if len(place) > 0 and isinstance(point, str):   #add an empty map to an existing map
                    data[place[index]][point] = self.map
                if isinstance(point, dict):                   #in case a map/set is deleted                     
                    if len(place) > 0 :
                        data[place[index]] = point
                    else:
                        data = point
                else:                                         #add an empty map to the directory directly
                    data[point] = self.map
                return data
            elif not map and not isinstance(point, dict):
                print(place)
                if isinstance(point, str):
                    if len(place) > 0 :
                        data[place[index]][point] = []                  #add an empty set to an existing map
                    else : 
                        data[point] = []
                else :                                                  #add an empty set to the directory directly
                    data[place[index]] = point               
                return data
            else:                                                       # add a new answer image            
                for i in range(len(data)):
                    if data[i]["question"] == point["question"]:
                        data[i]["answer"] = point["answer"]
                        data[i]["answer_path"] = point["answer_path"]
                return data
        else:                                                          # continue the recursion
            dummy = c.deepcopy(data[place[index]])
            data[place[index]] = self.navigate_down(question, map, index + 1, point, place, dummy)
            return data
        
    def change_folder(self, path : str) -> None:
        """Changes the folder which the Vigilant monitors

        :param path: path to the new folder 
        :type path: string
        """        
        try:
            with open(self.storage, 'r') as file:
                data = json.load(file)
            data["To_be_scanned"] = path
            with open(self.storage, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"failed so save new folder")
    
    def update_look_up(self, key : str, value : str) -> None:
        """update the look_up dictionary

        :param key: code used to identify an item in the Treeview
        :type key: string
        :param value: name under which the item is stored in the database
        :type value: string
        """        
        self.look_up[key] = value 
        
    def get_item(self, item : str) -> str :
        """retreives the name under which an item is stored in the storage using the item's iid

        :param item: iid under which the item is stored in the Treeview
        :type item: string
        :return: the name under which the item is stored in the storage
        :rtype: string
        """        
        for iid in self.look_up.keys() :
            if iid == item :
                return self.look_up[iid]
    
    def get_folder(self) -> str :
        """Retreives the path to the folder which the Vigilant monitors

        :return: path to monitored foldr
        :rtype: string
        """        
        self.data = self.load_data()
        return self.data["To_be_scanned"]
    
    def get_data(self) -> dict :
        """retreives the data, as stored in the storage

        :return: data in storage
        :rtype: dictionary
        """        
        data = self.load_data()
        return data["Directory"]
    
    def get_place(self, iid : str, place : bool, delete : bool) -> object:
        """Depending on the value of delete, this place returns a list or a subset of the data containing the item
        associated with iid, in case delete is False. Otherwise, the method returns the same except it terminates
        on step earlier.
        The list contains all keys leading to the item, including the item in case delete is False.
        The subset of the data either contains the item, should delete be True, or is the data stored at the place
        for which the item is the key.
        :param iid: iid associated with a specific key in the storage
        :type iid: string
        :param place: the method returns a subset of the data if True, a list otherwise
        :type place: boolean
        :param delete: the method terminates one step earlier, returning the subset containing the item or 
                        the list without, in case of True
        :type delete: boolean
        :return: a subset of the data / list containing keys
        :rtype: dict / list
        """        
        filtered = iid.split('.')
        if place :
            output = self.get_data()
        else :
            output = []
        dummy = ""
        for _ in filtered[1:] :                                #skip the type identifier in the iid                 
            dummy = dummy+ _ + '.' 
            if len(dummy) + 1 == len(iid) and delete:
                break
            for key in self.look_up.keys() :
                if key[2:] + '.' == dummy :                             
                    if place :
                        key = self.look_up[key]
                        output = output[key]
                        break
                    else :
                        output = output + [self.look_up[key]]
                        break   
        return output
    
    def write_data(self, data : dict):
        """writes data into the storage

        :param data: data to be stored
        :type data: dictionary
        """        
        storage = self.load_data()
        storage["Directory"] = data
        try:
            with open(self.storage, 'w') as file:
                json.dump(storage, file, indent=4)
            print(f"Successfully saved to {self.storage}")
        except Exception as e:
            print(f"Failed to save to JSON file: {e}")
        self.data = self.load_data()
        
    def load_data(self) -> dict:
        """load the data from the storage and return it

        :return: data as stored in the storage
        :rtype: dictionary
        """        
        data = None
        try:
            with open(self.storage, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f"Failed to load data: {e}")
        return data