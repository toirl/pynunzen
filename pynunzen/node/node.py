class Node(object):

    """A single node in the P2P network. Nodes are used to share updates
    to the the blockchain with all other nodes. Nodes can receive
    updates on the blockchain and will spread this updates to all other
    nodes it is connected to.
    """

    def __init__(self, address):
        """Given a address the node will be initialized to listen on the
        given address for incomming connections.

        :address: Address of the node
        :returns: :class:Node instance

        """
        self.address = address
        """Address on which this node is listening for incoming
        connections."""
        self.peers = []
        """List of peers this node is connected to"""
