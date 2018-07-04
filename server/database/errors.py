class ContactDoesNotExist(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Contact {} does not exist'.format(self.name)


class ContactAlreadyInDatabase(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Contact {} already exists'.format(self.name)
