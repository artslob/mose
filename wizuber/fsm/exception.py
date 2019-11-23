class ActionException(Exception):
    """ Base exception class for Action custom errors. """


class ActionNotFound(ActionException):
    """ Raise when attempt to find action by name is failed. """
