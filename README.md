This is a simple server-client application using network for the communication.

 * How to run
 	- You need at least 2 separate terminals.
 	- On one terminal: `python3 server.py`
 	- On the other terminal: `python3 client.py`
 	- If you want to try with more clients, just open another terminal and `python3 client.py`

 * Restrictions:
 	- Only compatible with Python3+
 	- Unix OS

 * Commands:
	- create basket {basketname}
	- remove basket {basketname}
	- add product {option} {basketname}
		* options = PEN, TSHIRT, MUG
	- checkout
	- quit
	- help
