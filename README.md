qubench
=======

sql query benchmark<br />
calculates query execution time distribution: min, max, percentiles. 

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

EXAMPLE:

<pre>
PS qubench> python .\qubench.py -uroot -dtmon -n5000 -c100 --file=query.txt

SQL:

<code>
 SELECT * FROM Stats WHERE Clients_Id = 15 AND Date >= '2012-11-01' AND Date <= '2012-11-30'
</code>

-----------------------------------------

Execution time:

 49.72s (100.6 rps)

-----------------------------------------

Min - Max:

 799.62 ms - 1125.36 ms

-----------------------------------------

Percentiles:


 50:  986.26 ms
 85:  1023.13 ms
 90:  1034.89 ms
 95:  1068.75 ms
 99:  1105.44 ms

-----------------------------------------
</pre>