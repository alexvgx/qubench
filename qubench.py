#
# TODO:
#
#	- add application abstraction level
#	- stream percentile calculation
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


# init arguments

optionsParser = argparse.ArgumentParser()
optionsParser.add_argument('-a', '--host', default="localhost")
optionsParser.add_argument('-u', '--user', required=True)
optionsParser.add_argument('-p', '--passwd', default="")
optionsParser.add_argument('-d', '--db', required=True)
optionsParser.add_argument('-c', '--clients', default=1)
optionsParser.add_argument('-n', '--number', required=True)
optionsParser.add_argument('-v', '--vebrose')
optionsParser.add_argument('-f', '--file', required=True)
cliOptions = optionsParser.parse_args()


# init logger

if "1" == cliOptions.vebrose:
	logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.DEBUG)
else:
	logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.INFO)



# setup input params

THREADS_NUMBER = int(cliOptions.clients)
SQL_QUERY_FILE = cliOptions.file
QUERIES_NUMBER = int(cliOptions.number)


# get query from file

SQL_QUERY = open(SQL_QUERY_FILE, 'r').read()


# queries distribution through threads

threadsCapacity = []
queriesRests = QUERIES_NUMBER
queriesPerThread = int(math.floor(QUERIES_NUMBER / THREADS_NUMBER))
threadIdx = 0

while (queriesRests >= queriesPerThread):
	threadsCapacity.append(queriesPerThread)
	queriesRests -= queriesPerThread

if queriesRests != 0:
	threadsCapacity.append(queriesRests)
	queriesRests -= queriesRests

threadIdx = 0
for threadCapcity in threadsCapacity:
	logging.debug("Thread #" + str(threadIdx) + " = " + str(threadCapcity))
	threadIdx += 1


# init db pool

logging.debug("Initializing db pool (count="+str(THREADS_NUMBER)+")")

try:
	dbPool = []
	for dbConnIdx in range(0, THREADS_NUMBER):
		db = MySQLdb.connect(host=cliOptions.host, user=cliOptions.user, passwd=cliOptions.passwd, db=cliOptions.db)
		dbPool.append(db)
except:
	logging.error("ERROR: can`t connect to database")
	sys.exit(-1)


# starting threads

queriesDurations = []
benchSession = benchsession.BenchSession()

logging.debug("Initializing threads (count=" + str(THREADS_NUMBER) + ")")
threadsList = []
for threadIdx in range(0, THREADS_NUMBER):
  queryThread = querythread.QueriesThread(benchSession, dbPool[threadIdx], SQL_QUERY, threadsCapacity[threadIdx], queriesDurations)
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
basicReport.output(SQL_QUERY, queriesDurations, total_duration)
