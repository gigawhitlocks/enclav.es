from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

class User(Node):
	element_type = "user"
	userid = String(nullable=False)
	password = String(nullable=False)
	created = DateTime(default=current_datetime, nullable=False)

class Friends(Relationship):
	label = "is friends with"
	created = DateTime(default=current_datetime, nullable=False)
