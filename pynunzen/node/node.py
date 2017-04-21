import datetime
from pynunzen.helpers import utcts
from pynunzen.network.message import (
    Response, Request,
    encode_message, decode_message
)


def cmd_ping(data):
    """Implenets a simple PING command. The message will return the current UTC timestamp

    :data: Received data
    :returns: Message

    """
    payload = utcts(datetime.datetime.utcnow())
    response = Response(payload)
    return encode_message(response)


def recv(json_msg):
    """Will parse the given message and triggers whatever action is
    needed. Finally the message will return a response. If the message
    con not be parsed a :class:MessageParseException will be raised.

    :json_msg: TODO
    :returns: TODO

    """
    msg = decode_message(json_msg)
    if isinstance(msg, Request):
        command = msg.command
        func = CMD2FUNC.get(command)
        if func:
            return func(msg.data)
        else:
            raise RuntimeError("Command {} not known".format(command))


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


CMD2FUNC = {
    "ping": cmd_ping
}
