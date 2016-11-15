"""
A User is a node in the graph.
Users is a lookup index for all nodes (a dictionary with the user id as a key
"""

class User(object):
    """An object holding the user id and the transactions of a user """

    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_ids = set()

    def add_transaction(self, other_user):
        self.transaction_ids.add(other_user)

UNVERIFIED = "unverified"
TRUSTED = "trusted"




class Users(object):

    def __init__(self):
        # this object contains all the users in a dictionary
        # so we can easily get a user by id, and start looking at their friends
        self.users = {}

    def create_or_get_user(self, id1):
        """ Returns an existing user, or creates them (adds them to the users dictionary)
        and then returns them"""
        if not self.user_exists(id1):
            self.users[id1] = User(id1)
        return self.users[id1]

    def can_reach(self, id1, id2, max_depth):
        """ This functions returns True if user with id=id1
        can reach user with id2
        if max_depth=1: can reach only if user1 is directly connected to user2
        if max_depth=2: can reach if user1 has a direct friend connected to user2
        if max_depth=3: can reach only is user 1 has a direct friend who has a direct friend connected to user2
        etc etc
        We are essentially doing a BREADTH FIRST SEARCH with bounded DEPTH
        """
        user1 = self.create_or_get_user(id1) 
        already_seen = set()
        initial_depth = 0
        queue = [(user1, initial_depth)] # start at the first user and ask their friends
        while(len(queue)>0):
            current_user, depth = queue.pop(0) # remove the first element in the queue
            if depth > max_depth: # if the user is too far removed then we can't reach them
                return False
            if current_user.user_id in already_seen: # ignore if we've already seen them
                continue
            if current_user.user_id == id2: # if we've reached the user we are looking for, return True
                return True
            already_seen.add(current_user.user_id) #mark the user as already seen
            # for each of the users friends
            # add them to the queue to ask them later (if we haven't already seen them)
            for user_id in current_user.transaction_ids:
                if user_id in already_seen:
                    continue
                user = self.create_or_get_user(user_id)
                queue.append((user, depth+1)) # the users friends are one level deeper in the graph
        return False


    def user_exists(self, user_id):
        return user_id in self.users # this is a query in a dictionary, which is optimized for performance in comparison to, say, a list

    def get_trust_level_of_transaction(self, id1, id2, degree_of_trust=1):
        # if any of the users is new, then by default the trust level is unverified
        # because at least one of them hasn't done a transaction before
        if not self.user_exists(id1) or not self.user_exists(id2):
            return UNVERIFIED
        else:
            if self.can_reach(id1, id2, max_depth=degree_of_trust):
                return TRUSTED
            else:
                return UNVERIFIED

    def add_transaction(self, id1, id2):
        """ Add a connection between the two users """

        user1 = self.create_or_get_user(id1) 
        user2 = self.create_or_get_user(id2) 

        user1.add_transaction(id2)
        user2.add_transaction(id1)

