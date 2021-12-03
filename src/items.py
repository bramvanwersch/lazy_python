

class Items:

    LOG = "log"
    OAK_LOG = "oak log"
    BRANCH = "branch"
    LEAF = "leaf"
    COBWEB = "cobweb"


# class Item:
#     def __init__(self, name, quantity):
#         self.name = name
#         self.quantity = quantity
#
#     def __hash__(self):
#         return hash((self.name, self.quantity))
#
#     def __eq__(self, other):
#         if isinstance(other, Item):
#             return other.name == other.quantity
#         return False
