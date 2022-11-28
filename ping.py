import sys

from models import *
from time import sleep
from sockets import *
import argparse

PING_INTERVAL = 0.05
PING_TIMEOUT = 3


def ping(address, n,payload):
	if is_hostname(address):
		address = resolve(address)[0]

	sock = ICMPSocket()
	id = unique_identifier()
	reply = None
	packets_sent = 0
	rtts = []

	###############################
	# TODO:
	# Create ICMPRequest and send through socket,
	# Resolve reply
	################################
	if reply:
		return Host(
			address=reply.source,
			packets_sent=packets_sent,
			rtts=rtts)
	return None


if __name__ == "__main__":
	target = sys.argv[1]
	parser = argparse.ArgumentParser(description="ping")
	parser.add_argument('--n', type=int, default=4)
	parser.add_argument('--l', type=str, default=None)
	args = parser.parse_args(sys.argv[2:])
	host = ping(target, args.n, args.l.encode())
	print(host.__str__())
