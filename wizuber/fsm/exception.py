class ActionException(Exception):
    """ Base exception class for Action custom errors. """


class ActionNotFound(ActionException):
    """ Raise when attempt to find action by name is failed. """


class ActionAccessDenied(ActionException):
    """ Raise when user dont have rights to execute action. """
