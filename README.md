qubench
=======

sql query benchmark

<pre>
usage: qubench.py [-h] [-a HOST] -u USER [-p PASSWD] -d DB [-c CLIENTS] -n
                  NUMBER [-v VEBROSE] -f FILE

optional arguments:
  -h, --help            show this help message and exit
  -a HOST, --host HOST  db hostname
  -u USER, --user USER  db username
  -p PASSWD, --passwd PASSWD
                        db password
  -d DB, --db DB        db name
  -c CLIENTS, --clients CLIENTS
                        clients count (no concurrency = 1)
  -n NUMBER, --number NUMBER
                        queries count (more queries - more precision
  -v VEBROSE, --vebrose VEBROSE
                        if set to '1' then vebrose more is on
  -f FILE, --file FILE  path to file contains sql query
</pre>
