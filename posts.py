from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

"""
Don't instantiate a plain Post. This just serves
as a parent class for the other Post types for shared values
"""
class Post(Node):
	
	# when was it created?
	created = DateTime(default=current_datetime, nullable=False)

	# title of the post?
	title = String(nullable=False)


"""
Similar to a "self-post" on Reddit.
"""
class TextPost(Post):
	element_type = "text_post"
	body_text = String(nullable=False)


class Comment(TextPost):
	element_type = "comment"

"""
Same as a link post on Reddit,
but should only be used for links to other sites.
multimedia LinkPosts are defined below.
"""
class LinkPost(Post):
	element_type = "link_post"
	url = String(nullable=False)


"""
Multimedia LinkPosts:


Specifically for Images
"""
class ImagePost(LinkPost):
	element_type = "image_post"



"""
Not exactly sure how we want to handle Video & Audio
posts but we do want to differentiate them for sorting
teebs
Specifically for Videos
"""
class VideoPost(LinkPost):
	element_type = "video_post"

"""
Specifically for Audio 
"""
class AudioPost(LinkPost):
	element_type = "audio_post"



"""Relationship defining who posted what
Comment--posted_by-->Identity OR
Post--posted_by-->Identity
"""
class PostedBy(Relationship):
	label = "posted_by"
	created = DateTime(default=current_datetime, nullable=False)

"""Relationship defining to what enclave a post is posted
Post--posted_to-->Enclave
"""
class PostedTo(Relationship):
	label = "posted_to"
	created = DateTime(default=current_datetime, nullable=False)

"""Relationship for threading conversations
Post--has_reply-->Comment OR 
Comment--HasReply-->Comment"""
class HasReply(Relationship):
	label = "has_reply"
	created = DateTime(default=current_datetime, nullable=False)
