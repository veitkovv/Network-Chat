class Chat:
    def __init__(self, name):
        self.name = name  #
        self.members = dict()  # {user1: role, user2: role....}

    def __repr__(self):
        return f'{self.name}: {self.members}'

    def add_member(self, user, role='user'):
        self.members.update({user: role})

    def remove_member(self, user_to_delete):
        for user in self.members.keys():
            if user == user_to_delete:
                self.members.pop(user)
                return user

    def check_membership(self, account_name):
        for user in self.members.keys():
            if user.account_name == account_name:
                return True

    @property
    def chat_members_names(self):
        for user in self.members.keys():
            yield user.account_name
