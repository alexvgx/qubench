#
# TODO:
#
#	- correct queries distribution between threads
#	- add cli support for query setup
#	- add output usability
#	- stream percentile calculation
#	- add logger
#	- add application abstraction level
#

import time
import math
import argparse
import logging
import sys

import MySQLdb

import querythread
import benchsession
import reports


QUERIES_NUMBER = 1000
sqlQuery = "SELECT * FROM StatsDailyByWindow WHERE Clients_Id = 15 AND Date >= '2012-11-01' AND Date <= '2012-11-30' ORDER BY Date ASC";


# init arguments

optionsParser = argparse.ArgumentParser()
optionsParser.add_argument('-a', '--host', default="localhost")
optionsParser.add_argument('-u', '--user', required=True)
optionsParser.add_argument('-p', '--passwd', default="")
optionsParser.add_argument('-d', '--db', required=True)
optionsParser.add_argument('-c', '--clients', default=5)
optionsParser.add_argument('-v', '--vebrose')
cliOptions = optionsParser.parse_args()


# init logger

if "1" == cliOptions.vebrose:
	logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.DEBUG)
else:
	logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.INFO)

# init db pool

THREADS_NUMBER = int(cliOptions.clients)

logging.debug("Initializing db pool (count="+str(THREADS_NUMBER)+")")

try:
	dbPool = []
	for dbConnIdx in range(0, THREADS_NUMBER):
		db = MySQLdb.connect(host=cliOptions.host, user=cliOptions.user, passwd=cliOptions.passwd, db=cliOptions.db)
		dbPool.append(db)
except:
	logging.error("ERROR: can`t connect to database")
	sys.exit(-1)

queriesPerThread = int(math.ceil(QUERIES_NUMBER / THREADS_NUMBER))
queriesDurations = []

# starting threads

benchSession = benchsession.BenchSession()

logging.debug("Initializing threads (count=" + str(THREADS_NUMBER) + ")")
threadsList = []
for threadIdx in range(0, THREADS_NUMBER):
  queryThread = querythread.QueriesThread(benchSession, dbPool[threadIdx], sqlQuery, queriesPerThread, queriesDurations)
  threadsList.append(queryThread)
  queryThread.start()


# starting benchmark

logging.debug("Starting threads")
startTime = time.clock()
benchSession.setState(1)
for threadIdx in range(0, THREADS_NUMBER):
  threadsList[threadIdx].join()
total_duration = time.clock() - startTime

# calculating stats

basicReport = reports.BasicReport([50, 85, 90, 95, 99])
basicReport.output(queriesDurations, total_duration)
