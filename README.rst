************
Dependencies
************

- Python 3.7+
- aiohttp
- zlib


****************
Operating system
****************
Tested on Microsoft Windows 10

******
Usage
******

**Server**

(venv) \path\to\filesync>python -m server.server --help
    usage: server.py [-h] [-p PATH] [-v] [-c]

    file sync program

    optional arguments:
      -h, --help            show this help message and exit
      -p PATH, --path PATH  directory path to be synced
      -v, --verbose         increase output verbosity
      -c, --compress        use compression

**Client**

(venv) \path\to\filesync>python -m client.client --help
    usage: client.py [-h] [-p PATH] [-v] [-c]

    file sync program

    optional arguments:
      -h, --help            show this help message and exit
      -p PATH, --path PATH  directory path to be synced
      -v, --verbose         increase output verbosity
      -c, --compress        use compression


**************
Known caveats
**************
- Server must start before client because server is not able to report its contents
- Empty directories may be left out on server due to this
- Always hashes are used to compute file diffs, timestamps could suffice in most cases. Also this could be better abstracted
- Empty folders are not synced
- Updates are just new file transfers instead of an rsync like algorithm
- Persistent ClientSession could be used in client but I don't know how to do it
- Asyncio could be used on server side when handling multiple requests
- Only tested on local machine
- Could run pylint on the code, not done so far
- Queuing could be implemented to mitigate the situation when file transfer takes longer than file monitoring interval (2 seconds)
- Client does not retransmit failed commands (e.g. due to temporary server disconnection etc.)
