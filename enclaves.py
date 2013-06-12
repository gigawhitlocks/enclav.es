
#Enclave object and related are below
class Enclave(Node):
  created = DateTime(default=current_datetime, nullable=False)
  name = String(nullable=False)
  
  #gov_type will define government type for a given Enclave
  #Will hopefully eventually include Monarchy and Democracy at least
  #If not some combinations as well
  gov_type = String(nullable=False, default="monarchy")

  #determines whether or not subscribers can post
  membership_required = Integer(nullable=False, default=0)

  #determines whether posts in the enclave are visible to the wider community
  #when set to 1, membership_required is assumed to be 1
  private = Integer(nullable=False, default=0)
  
