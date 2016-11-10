"""
A User is a node in the graph.
Users is a lookup index for all nodes (a dictionary with the user id as a key
"""

class User(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_ids = set()

    def add_transaction(self, other_user):
        self.transaction_ids.add(other_user)

UNVERIFIED = "unverified"
TRUSTED = "trusted"




class Users(object):

    def __init__(self):
        self.users = {}

    def create_or_get_user(self, id1):
        if not self.user_exists(id1):
            self.users[id1] = User(id1)
        return self.users[id1]

    def can_reach(self, id1, id2, steps):
        user1 = self.create_or_get_user(id1) 
        already_seen = set()
        queue = [user1]
        while(steps>0 and len(queue)>0):
            current_user = queue.pop(0)
            already_seen.add(current_user.user_id)
            if id2 in current_user.transaction_ids:
                return True
            steps -= 1
            if steps == 0:
                return False
            for user_id in current_user.transaction_ids:
                if user_id in already_seen:
                    continue
                user = self.create_or_get_user(user_id)
                queue.append(user)
        return False


    def user_exists(self, user_id):
        return user_id in self.users

    def get_trust_level_of_transaction(self, id1, id2, degree_of_trust=1):
        if not self.user_exists(id1) or not self.user_exists(id2):
            return UNVERIFIED
        else:
            if self.can_reach(id1, id2, steps=degree_of_trust):
                return TRUSTED
            else:
                return UNVERIFIED

    def add_transaction(self, id1, id2):

        user1 = self.create_or_get_user(id1) 
        user2 = self.create_or_get_user(id2) 

        user1.add_transaction(id2)
        user2.add_transaction(id1)

        

