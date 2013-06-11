from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

class Post(Node):
    """
    don't instantiate a plain post. this just serves
    as a parent class for the other post types for shared values
    """
    
    # when was it created?
    created = DateTime(default=current_datetime, nullable=False)

    # title of the post?
    title = String(nullable=False)


class TextPost(Post):
    """ Similar to a "self-post" on Reddit. """
    element_type = "text_post"
    body_text = String(nullable=False)


class Comment(TextPost):
    element_type = "comment"

class LinkPost(Post):
    """
    Same as a link post on Reddit,
    but should only be used for links to other sites.
    multimedia LinkPosts are defined below.
    """
    element_type = "link_post"
    url = String(nullable=False)


#Multimedia LinkPosts:


class ImagePost(LinkPost):
    element_type = "image_post"



#Not exactly sure how we want to handle Video & Audio
#posts but we do want to differentiate them for sorting
#Specifically for Videos

class VideoPost(LinkPost):
    """Specifically for Video"""
    element_type = "video_post"

class AudioPost(LinkPost):
    """Specifically for Audio"""
    element_type = "audio_post"



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
