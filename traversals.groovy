def getInviter( _id ) {
		return g.v(_id).in("invited")
}

def getIdentities( _id ) {
		//_id is the eid of the current user
		return g.v(_id).out("is")
}


/*
		returns a generator of vertices one hop in direction from _id along any edge with the given relationship
*/
def getNeighboringVertices( _id, relationship, direction ) {
		if ( direction == "out" )
				return g.v(_id).out(relationship)
		else
				return g.v(_id).in(relationship)
}
