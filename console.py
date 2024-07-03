#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' \
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        return False

    def do_create(self, args):
        """ Create an object of any class"""

        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        # assumes first arg is class name
        class_name = args_list[0]

        # checks if arg is valid <class name> (in class_dict)
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # since class name is taken care of
        # now evaluate remaining args from input
        args_list = args_list[1:]

        attributes = {}

        # search through the list of arguments
        for arg in args_list:
            # key/value pairs split and saved into arg_toks list
            arg_toks = arg.split("=")

            # if len(args_list) != 2:
            #     continue
            key, value = arg_toks[0], arg_toks[1]

            # Unquote, underscore to space
            # convert values to appropriate data types
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ')
            try:
                value = float(value)
            except ValueError:
                pass
            try:
                value = int(value)
            except ValueError:
                pass

            attributes[key] = value

        new_instance = HBNBCommand.classes[class_name](**attributes)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            obj = storage.all()[key]
            storage.delete(obj)
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        # first initialize list to store python obj instances
        print_list = []
        # split args (input) and grab first (or only) argument
        # assign to class_name variable
        class_name = args.split()[0] if ' ' in args else args

        # if no class name is specified, add all obj instances to list
        # add dictionary of objs to list as string representations
        if class_name == "":
            # gets all objs from all classes from storage
            obj_dict = storage.all()
            for key in obj_dict:
                print_list.append(str(obj_dict[key]))
            for item in print_list:
                print(item)
            return

        # if arg is passed, but not a valid class, give below error
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # here on assumes valid class name was passed
        # only adds objs from specified class
        obj_dict = storage.all(HBNBCommand.classes[class_name])
        for key, value in obj_dict.items():
            if class_name in key:
                print_list.append(str(value))
            for item in print_list:
                print(item)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """updates an object with a given attribute

        requires class name and id as input arguments
        only one attribute can be updated at a time
        """

        if not args:
            print("** class name missing **")
            return

        args_list = args.split()

        # make sure args (input) includes all parameters
        if len(args_list) == 0:
            print("** class name missing **")
            return
        elif len(args_list) == 1:
            print("** instance id missing **")
            return
        elif len(args_list) == 2:
            print("** attribute name missing **")
            return
        elif len(args_list) == 3:
            print("** value missing **")
            return

        # ensures list of arguments is 4 (args after 4 discarded)
        while (len(args_list) > 4):
            args_list.pop()

        class_name = args_list[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        class_id = args_list[1]

        key = f"{class_name}.{class_id}"

        obj_dict = storage.all()
        if key not in obj_dict:
            print("** no instance found **")
            return

        attr_name = args_list[2]
        attr_val = args_list[3]

        # gets dictionary representation of object
        instance = obj_dict[key]

        # attempts to update below attributes will fail
        if attr_name in ['id', 'created_at', 'updated_at']:
            return

        # cast attr_val to appropriate data type
        try:
            # checks if attr_val is a float (if it has decimal point)
            if "." in attr_val:
                attr_val = float(attr_val)
            else:
                attr_val = int(attr_val)
        except ValueError:
            # attr_val stays a string in this case
            pass

        setattr(instance, attr_name, attr_val)
        instance.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
