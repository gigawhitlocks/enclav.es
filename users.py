from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime
import random
import hashlib
import string

def generate_salt():
	salt = ""
	for i in range(0, random.randint(10,30)):
		salt += random.choice(string.digits+string.letters)
	return salt

def check_password(raw_input, hash):
	hash = hash.split('$')
	pword = hash[2]+raw_input
	for i in range(0, int(hash[1])):
		pword = hashlib.sha256(pword).hexdigest()
	return hash[3] == pword

def generate_storable_password(raw_password):
		version_number = 1
		salt = generate_salt()
		pword = salt+raw_password
		times_hashed = 0
		for i in range(0, random.randint(5,10)):
			times_hashed += 1 
			pword = hashlib.sha256(pword).hexdigest()
		return "%s$%s$%s$%s" %(version_number, times_hashed, salt, pword)

class User(Node):
	element_type = "user"
	userid = String(nullable=False)
	password = String(nullable=False)
	created = DateTime(default=current_datetime, nullable=False)

class Invitee(Node):
	element_type = "invitee"
	email = String(nullable=False)
	token = String(nullable=False)
	created = DateTime(default=current_datetime, nullable=False)
	invited_by = String(nullable=False)

class Follows(Relationship):
	label = "follows"
	created = DateTime(default=current_datetime, nullable=False)


