def getInviter( _id ) {
		return g.v(_id).in("invited")
}

def getPoster( _id ) {
		return g.v(_id).out("posted_by")
}


def getIdentities( _id ) {
		//_id is the eid of the current user
		return g.v(_id).out("is")
}
