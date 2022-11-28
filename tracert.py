from models import *
from time import sleep
from sockets import *

PING_COUNT = 3
PING_INTERVAL = 0.05
PING_TIMEOUT = 2
MAX_HOP = 30


def traceroute(address, id=None, **kwargs):
    if is_hostname(address):
        address = resolve(address)[0]

    sock = ICMPSocket()

    id = id or unique_identifier()
    ttl = 1
    host_reached = False
    hops = []

    while not host_reached and ttl <= MAX_HOP:
        reply = None
        packets_sent = 0
        rtts = []

        ###############################
        # TODO:
        # Create ICMPRequest and send through socket,
        # Resolve reply
        ################################

        if reply:
            hop = Hop(
                address=reply.source,
                packets_sent=packets_sent,
                rtts=rtts,
                distance=ttl)

            hops.append(hop)

        ttl += 1

    return hops


if __name__ == "__main__":
    hops = traceroute("jp.nuxjc.com")
    for hop in hops:
        print(hop.__str__())
