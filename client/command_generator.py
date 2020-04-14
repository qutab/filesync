import bidict
from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Command(AutoName):
    ADD = auto()
    DELETE = auto()
    MOVE = auto()
    UPDATE = auto()

    def __str__(self):
        return str(self.name)


def get_commands(prev: bidict.bidict, curr: bidict.bidict):
    """
    A command is an internal representation of the action to be done by the server on the file.
    Each command is a key-value pair with keys being the filename and value being the desired
    list of actions on the file. The action can have zero or more optional arguments.

    :return: dictionary of commands
    """
    moved_files = []
    cmd = {}

    # check delete / move
    for k, v in prev.items():
        if k not in curr:  # file does not exist in new map
            if v not in curr.values():  # checksum does not exist in new map
                cmd[k] = [Command.DELETE]
            else:  # checksum exists in new map
                cmd[k] = [Command.MOVE, f"{curr.inverse[v]}"]  # command and new location
                moved_files.append(curr.inverse[v])

    # check add/modify
    for k, v in curr.items():
        if k in prev:  # if file existed before
            if v == prev[k]:  # if file contents are same
                pass
            else:  # if contents have changed
                cmd[k] = [Command.ADD]  # this could be optimized to update
        elif k not in moved_files:  # file did not exist before and has not been moved
            cmd[k] = [Command.ADD]

    return cmd
