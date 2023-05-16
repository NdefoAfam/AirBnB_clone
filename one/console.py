#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl

class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    command_prompt = "(hbnb) "
    valid_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        command_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            split_args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", split_args[1])
            if match is not None:
                command = [split_args[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in command_dict.keys():
                    call = "{} {}".format(split_args[0], command[1])
                    return command_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

def do_quit(self, arg):
    """Quit command to exit the program."""
    return True

def do_EOF(self, arg):
    """EOF signal to exit the program."""
    print("")
    return True

def do_create(self, arg):
    """Usage: create <class>
    Create a new class instance and print its id.
    """
    arg_list = parse(arg)
    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    else:
        print(eval(arg_list[0])().id)
        storage.save()

def do_show(self, arg):
    """Usage: show <class> <id> or <class>.show(<id>)
    Display the string representation of a class instance of a given id.
    """
    arg_list = parse(arg)
    obj_dict = storage.all()
    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    elif len(arg_list) == 1:
        print("** instance id missing **")
    elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
        print("** no instance found **")
    else:
        print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

def do_destroy(self, arg):
    """Usage: destroy <class> <id> or <class>.destroy(<id>)
    Delete a class instance of a given id."""
    arg_list = parse(arg)
    obj_dict = storage.all()
    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    elif len(arg_list) == 1:
        print("** instance id missing **")
    elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
        print("** no instance found **")
    else:
        del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
        storage.save()

def do_all(self, arg):
    """Usage: all or all <class> or <class>.all()
    Display string representations of all instances of a given class.
    If no class is specified, displays all instantiated objects."""
    arg_list = parse(arg)
    if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__classes:
        print("** class doesn't exist **")
    else:
        obj_list = []
        for obj in storage.all().values():
            if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                obj_list.append(obj.__str__())
            elif len(arg_list) == 0:
                obj_list.append(obj.__str__())
        print(obj_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args_list = parse(arg)
        count = 0
        for obj in storage.all().values():
            if args_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args_list = parse(arg)
        obj_dict = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
            return False
        if args_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args_list[0], args_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args_list) == 2:
            print("** attribute name missing **")
            return False
        if len(args_list) == 3:
            try:
                type(eval(args_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False


        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
