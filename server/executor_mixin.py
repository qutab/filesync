import logging


class ExecutorMixin(object):
    """
    This mixin maps client commands to handler functions
    """

    def __init__(self, *args, **kwargs):
        super(ExecutorMixin, self).__init__(*args, **kwargs)

    def execute_command(self) -> bool:
        command = self.path.split('/', 1)[1]

        mapping = {
            "add": lambda: self.handle_add(),
            "delete": lambda: self.handle_delete(),
            "update": lambda: self.handle_update()
        }

        try:
            mapping[command]()
        except KeyError:
            logging.error("Unsupported command received from client")
            return False

        return True
