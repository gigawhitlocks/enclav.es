from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime
import random
import hashlib
import string


"""
The following three functions are helper functions
"""

"""
Creates a salt for use generating password hashes
"""
def generate_salt():
	salt = ""
	for i in range(0, random.randint(10,30)):
		salt += random.choice(string.digits+string.ascii_letters)
	return salt


"""
Checks plaintext passwords against hashes in memory for validity. Returns a boolean.
"""
def check_password(raw_input, hash):
	hash = hash.split('$')
	pword = hash[2]+raw_input
	for i in range(0, int(hash[1])):
		pword = hashlib.sha256(pword).hexdigest()
	return hash[3] == pword

"""
Hashes a plaintext password into a secure storable hash
"""
def generate_storable_password(raw_password):
		version_number = 1
		salt = generate_salt()
		pword = salt+raw_password
		times_hashed = 0
		for i in range(0, random.randint(5,10)):
			times_hashed += 1 
			pword = hashlib.sha256(pword).hexdigest()
		return "%s$%s$%s$%s" %(version_number, times_hashed, salt, pword)

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

