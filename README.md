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

 * Extra features&controls:
 	- unique basket name
 	- missing parameters
 	- undefined product
 	- adding products to the same basket from different clients
 	- listing products on a basket

 * Regarding Dockerfile: Unfortunately it's not finished but also it does not make that much sense to have it. Since I am out of time, I am leaving it as it is.