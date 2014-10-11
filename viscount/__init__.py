import argparse

from viscount.server import Server

def main():
	import argparse

	parser = argparse.ArgumentParser(prog="run")

	parser.add_argument("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")
	parser.add_argument("-i", "--host", action="store", type=str, dest="host", help="Specify the host interface for the server (default all)")
	parser.add_argument("-p", "--port", action="store", type=int, dest="port", help="Specify the port for the server (default 5000)")
	parser.add_argument("-r", "--root", action="store_true", dest="allowRoot", help="Allow viscount to be run as root")

	args = parser.parse_args()

	if not args.host:
		args.host = "0.0.0.0"
	if not args.port:
		args.port = 5000

	viscount = Server(args.host, args.port, args.debug, args.allowRoot)
	viscount.run()

if __name__ == "__main__":
	main()
