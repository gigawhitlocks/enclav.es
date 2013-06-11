def getInviter( _id ) {
	return g.v(_id).in("invited")
}


def getPoster( _id ) {
	return g.v(_id).out("posted_by")
}
