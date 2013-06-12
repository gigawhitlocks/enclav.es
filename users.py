from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

# pretty self-explanatory
class User(Node):
    element_type = "user"
    userid = String(nullable=False)
    password = String(nullable=False)
    created = DateTime(default=current_datetime, nullable=False)


# A User has many Identities. Identities are unqiue.
# User --Is--> Identity
class Identity(Node):
    element_type = "identity"
    identity = String(nullable=False)

# Identity --subscribes_to--> Enclave OR
# Identity --is_member_of--> Enclave when there is a distinction
class SubscribesTo(Relationship):
    label = "subscribes_to"
    created = DateTime(default=current_datetime, nullable=False)

class IsMemberOf(Relationship):
    label = "is_member_of"
    created = DateTime(default=current_datetime, nullable=False)

# nodes that exist before a user actually signs up but after invitation
class Invitee(Node):
    element_type = "invitee"
    email = String(nullable=False)
    token = String(nullable=False)
    created = DateTime(default=current_datetime, nullable=False)

# this relationship defines which Indentities belong to a User
# User --Is--> Identity
class Is(Relationship):
    label = "is"
    created = DateTime(default=current_datetime, nullable=False)

# This relationship defines relationships between users
# User --Follows--> User
class Follows(Relationship):
    label = "follows"
    created = DateTime(default=current_datetime, nullable=False)

# This relationship defines which user invited which user or invitee
# User --Invited--> Invitee OR User --Invited--> User
class Invited(Relationship):
    label = "invited"
    created = DateTime(default=current_datetime, nullable=False)

