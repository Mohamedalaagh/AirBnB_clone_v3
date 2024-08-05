#!/usr/bin/python3
"""
This is the file_storage module.

This module defines one class, FileStorage.
This class handles saving the information in JSON format in a file.
"""

from datetime import datetime
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os


class FileStorage:
    """
    Stores objects in a file in a JSON format.

    **Class Attributes:**
        __file_path (str): Private. The path to the JSON file.
        __objects (dict): Private. A dictionary of all the objects.

    **Instance Attributes:**
        __models_available (dict): Private. Classes currently handled by FileStorage.
    """
    __file_path = "file.json"
    if os.getenv("FS_TEST", "no") == "yes":
        __file_path = "test_file.json"
    __objects = {}

    def __init__(self):
        """
        Initializes the FileStorage instance.
        
        Sets up the available models and reloads any existing data from the file.
        """
        self.__models_available = {
            "User": User, "BaseModel": BaseModel,
            "Amenity": Amenity, "City": City,
            "Place": Place, "Review": Review,
            "State": State
        }
        self.reload()

    def all(self, cls=None):
        """
        Returns the required objects.

        **Arguments:**
            cls (str): Optional. A valid Class Name. If provided, only objects of that class will be returned.

        **Returns:**
            dict: A dictionary of objects. If cls is provided, returns objects of that class; otherwise, returns all objects.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            result = {k: v for k, v in FileStorage.__objects.items() if v.__class__.__name__ == cls}
            return result

    def new(self, obj):
        """
        Adds a new object to __objects.

        **Arguments:**
            obj (BaseModel): An instance of a class derived from BaseModel.
        """
        if obj is not None:
            FileStorage.__objects[obj.id] = obj

    def save(self):
        """
        Serializes all objects to the JSON file.
        
        Converts the objects to JSON format and writes them to the file specified by __file_path.
        """
        store = {k: v.to_json() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, mode="w+", encoding="utf-8") as fd:
            fd.write(json.dumps(store))

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        
        Loads the objects from the JSON file specified by __file_path. 
        Silently skips any errors encountered during the process.
        """
        FileStorage.__objects = {}
        try:
            with open(FileStorage.__file_path, mode="r+", encoding="utf-8") as fd:
                temp = json.load(fd)
        except Exception as e:
            return
        for k, v in temp.items():
            cls = v.pop("__class__", None)
            if cls in self.__models_available:
                FileStorage.__objects[k] = self.__models_available[cls](**v)

    def delete(self, obj=None):
        """
        Removes an object from __objects and saves the changes.

        **Arguments:**
            obj (BaseModel): Optional. The object to be removed. If not provided, no action is taken.
        """
        if obj:
            FileStorage.__objects.pop(obj.id, None)
            self.save()

    def close(self):
        """
        Reloads the storage.

        This method is typically called at the end of a session to ensure the latest data is loaded from the file.
        """
        self.reload()

    def get(self, cls, id_):
        """
        Retrieves one object based on the class and id.

        **Arguments:**
            cls (str): The name of the class.
            id_ (str): The id of the object.

        **Returns:**
            BaseModel: The object with the given class name and id, or None if not found.
        """
        if cls not in self.__models_available:
            return None
        all_objs = self.all(cls)
        return all_objs.get(id_, None)

    def count(self, cls=None):
        """
        Counts the number of objects in a certain class or in total.

        **Arguments:**
            cls (str): Optional. The name of the class. If provided, counts only objects of that class.

        **Returns:**
            int: The number of objects in that class, or in total if no class is specified. Returns -1 if the class is not valid.
        """
        if cls is None:
            return len(self.__objects)
        if cls in self.__models_available:
            return len(self.all(cls))
        return -1

