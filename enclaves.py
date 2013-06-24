from bulbs.model import Node, Relationship
from bulbs.property import String, DateTime
from bulbs.utils import current_datetime


class Enclave(Node):
    """
    Enclave defines the object for new Enclaves  
    """
    element_type = "enclave"
    created = DateTime(default=current_datetime, nullable=False)
    name = String(nullable=False)
#    tagline = String(nullable=False)

    #gov_type will define government type for a given Enclave
    #Will hopefully eventually include Monarchy and Democracy at least
    #If not some combinations as well
    gov_type = String(nullable=False, default="oligarchy")

    #determines whether posts in the enclave are visible to the wider community
    #when set to 1, membership_required is assumed to be 1
    privacy = String(nullable=False, default="public")

class Moderates(Relationship):
    """User --Moderates--> Enclave"""

    label = "moderates"
    created = DateTime(default=current_datetime, nullable=False)

class Owns(Relationship):
    label = "owns"
    created = DateTime(default=current_datetime, nullable=False)
