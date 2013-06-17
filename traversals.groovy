def getInviter( _id ) {
		return g.v(_id).in("invited")
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
