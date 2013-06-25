from bulbs.model import Node, Relationship
from bulbs.property import String, DateTime
from bulbs.utils import current_datetime

class Post(Node):
    """
    don't instantiate a plain post. this just serves
    as a parent class for the other post types for shared values
    """
    element_type = "post"
    post_type = String(nullable=False)
    
    # when was it created?
    created = DateTime(default=current_datetime, nullable=False)

    # title of the post?
    title = String(nullable=False)

    url = String(nullable=True)
    body_text = String(nullable=True)

class Comment(Post):
    element_type = "comment"

class PostedBy(Relationship):

    """Relationship defining who posted what
    Comment--posted_by-->Identity OR
    Post--posted_by-->Identity
    """
    label = "posted_by"
    created = DateTime(default=current_datetime, nullable=False)

class PostedTo(Relationship):
    """Relationship defining to what enclave a post is posted
    Post--posted_to-->Enclave
    """
    label = "posted_to"
    created = DateTime(default=current_datetime, nullable=False)

class HasReply(Relationship):
    """Relationship for threading conversations
    Post--has_reply-->Comment OR 
    Comment--HasReply-->Comment"""
    label = "has_reply"
    created = DateTime(default=current_datetime, nullable=False)
