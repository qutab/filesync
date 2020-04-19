from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Command(AutoName):
    ADD = auto()
    DELETE = auto()
    UPDATE = auto()

    def __str__(self):
        return str(self.name)


def get_commands(prev: dict, curr: dict):
    """
    A command is an internal representation of the action to be done by the server on the file.
    Each command is a key-value pair with keys being the filename and value being the desired
    list of actions on the file. The action can have zero or more optional arguments.

    :return: dictionary of commands
    """
    cmd = {}

    # check delete / move
    for filename, checksum in prev.items():
        if filename not in curr:  # file does not exist in new map
            assert checksum not in curr.values()  # Checksums are always unique
            cmd[filename] = [Command.DELETE]

    # check add/modify
    for filename, checksum in curr.items():
        if filename in prev:  # if file existed before
            if checksum != prev[filename]:  # if file contents are different
                cmd[filename] = [Command.UPDATE]
        else:  # file did not exist before
            cmd[filename] = [Command.ADD]

    return cmd
