#!/usr/bin/python3
""" The console module """
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models import storage


class HBNBCommand(cmd.Cmd):
    """ The console HBNB class """
    prompt = "(hbnb)"

    __classes = ["basemodel", "user", "state",
                 "city", "place", "review", "amenity"]

    def do_quit(self, line):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, line):
        """ Used to quit the console - Used by typing - Control + D """
        print()
        return True

    def emptyline(self):
        """ The console shouldn't do anything if nothing is entered """
        pass

    def do_create(self, line):
        """
        Creates a new instance of Model,
        saves it (to the JSON file) and prints the id
        """
        if line:
            if line.lower() in self.__classes:
                if line.lower() == 'basemodel':
                    model = BaseModel()
                if line.lower() == 'user':
                    model = User()
                if line.lower() == 'state':
                    model = State()
                if line.lower() == 'city':
                    model = City()
                if line.lower() == 'place':
                    model = Place()
                if line.lower() == 'review':
                    model = Review()
                if line.lower() == 'amenity':
                    model = Amenity()
                model.save()
                print(model.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, line):
        """
         Prints the string representation of an
         instance based on the class name and id
        """
        if line:
            className = None
            instanceId = None
            lines = line.split(" ")
            if len(lines) == 2:
                className = lines[0]
                instanceId = lines[1]
            elif len(lines) == 1:
                className = lines[0]
            if className.lower() in self.__classes:
                if instanceId:
                    objs = storage.all()
                    key = "{}.{}".format(className, instanceId)
                    if key in objs:
                        print(objs[key])
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file).
        """
        if line:
            className = None
            instanceId = None
            lines = line.split(" ")
            if len(lines) == 2:
                className = lines[0]
                instanceId = lines[1]
            elif len(lines) == 1:
                className = lines[0]
            if className.lower() in self.__classes:
                if instanceId:
                    objs = storage.all()
                    key = "{}.{}".format(className, instanceId)
                    if key in objs:
                        del objs[key]
                        storage.save()
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """
        Prints all string representation of all
        instances based or not on the class name.
        """
        objs = storage.all()
        if line:
            if line.lower() in self.__classes:
                class_objs = {}
                for i in objs:
                    if i.startswith(line):
                        class_objs[i] = objs[i]
                for i in class_objs:
                    print(class_objs[i])
            else:
                print("** class doesn't exist **")
        else:
            for i in objs:
                print(objs[i])

    def do_update(self, line):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute.
        update <class name> <id> <attribute name> "<attribute value>"
        """
        if line:
            className = None
            instanceId = None
            attribute_name = None
            attribute_value = None
            lines = line.split(" ")
            if len(lines) == 4:
                className, instanceId, attribute_name, attribute_value = lines
                attribute_value = attribute_value[1:-1]
            elif len(lines) == 3:
                className, instanceId, attribute_name = lines
            elif len(lines) == 2:
                className, instanceId = lines
            elif len(lines) == 1:
                className = lines[0]
            else:
                print('update <class name> <id> <attribute name>'
                      ' "<attribute value>"')
                return False
            if className.lower() in self.__classes:
                if instanceId:
                    objs = storage.all()
                    key = "{}.{}".format(className, instanceId)
                    if key in objs:
                        if attribute_name and attribute_name \
                                not in ["id", "created_at" "updated_at"]:
                            if attribute_value:
                                model = objs[key]
                                if attribute_name in model.__dict__.keys():
                                    attribute_type = type(model.__dict__
                                                          [attribute_name])
                                    model.__dict__[attribute_name] = \
                                        attribute_type(attribute_value)
                                    model.save()
                                else:
                                    model.__dict__[attribute_name] = \
                                        attribute_value
                                    model.save()
                            else:
                                print("** value missing **")
                        else:
                            print("** attribute name missing **")
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def count(self, line):
        """
        Prints all string representation of all
        instances based or not on the class name.
        """
        objs = storage.all()
        if line:
            if line.lower() in self.__classes:
                class_objs = {}
                for i in objs:
                    if i.startswith(line):
                        class_objs[i] = objs[i]
                print(len(class_objs))
            else:
                print("** class doesn't exist **")

    def default(self, line):
        args = line.split(".")
        if len(args) == 2:
            class_name, function = args
            if class_name.lower() in self.__classes:
                if function == "all()":
                    self.do_all(class_name)
                if function == "count()":
                    self.count(class_name)
                if function.startswith("show"):
                    function = function[5:-1]
                    self.do_show(class_name + " " + function)
                if function.startswith("destroy"):
                    function = function[8:-1]
                    self.do_destroy(class_name + " " + function)
        else:
            super().default(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
