def getInviter( _id ) {
	return g.v(_id).in("invited")

}
