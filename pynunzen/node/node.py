import json
import datetime
from pynunzen.helpers import utcts


def cmd_ping(data):
    """Implenets a simple PING command. The message will return the current UTC timestamp

    :data: Received data
    :returns: Message

    """
    response = {}
    response["type"] = "response"
    response["success"] = True
    response["data"] = utcts(datetime.datetime.utcnow())
    return encode_json_msg(response)


def recv(json_msg):
    """Will parse the given message and triggers whatever action is
    needed. Finally the message will return a response. If the message
    con not be parsed a :class:MessageParseException will be raised.

    :json_msg: TODO
    :returns: TODO

    """
    msg = decode_json_msg(json_msg)
    command = msg["command"]
    func = CMD2FUNC.get(command)
    if func:
        return func(msg["data"])
    else:
        raise MessageParseException("Command {} not known".format(command))


def decode_json_msg(json_msg):
    try:
        return json.loads(json_msg)
    except:
        raise MessageParseException("Message can not be parsed")


def encode_json_msg(msg):
    if not isinstance(msg, dict):
        raise MessageParseException("Message can not be parsed")
    try:
        return json.dumps(msg)
    except:
        raise MessageParseException("Message can not be parsed")


class MessageParseException(ValueError):
    pass


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
