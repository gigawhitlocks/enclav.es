from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime

"""
Don't instantiate a plain Post. This just serves
as a parent class for the other Post types for shared values
"""
class Post(Node):
	
	# who created this Post?
	author = String(nullable=False)

	# when was it created?
	created = DateTime(default=current_datetime, nullable=False)

	# to what enclave was it posted?
	enclave = String(nullable=True, default=None)


"""
Similar to a "self-post" on Reddit.
"""
class TextPost(Post):
	element_type = "text_post"

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

Specifically for Videos
"""
class VideoPost(LinkPost):
	element_type = "video_post"

"""
Specifically for Audio 
"""
class AudioPost(LinkPost):
	element_type = "audio_post"
