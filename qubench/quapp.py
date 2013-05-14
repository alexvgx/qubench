
import time
import math
import argparse
import logging
import sys

import MySQLdb


import querythread
import benchsession
import reports



class QuApp(object):

	def __init__(self):
		self.threadsNumber = 1 
		self.queryFile = 'query.txt'
		self.queriesNumber = 1000
		self.query = None
		self.dbPool = []

		self.threadsCapacity = []

	def bootstrap(self):

		# init arguments

		optionsParser = argparse.ArgumentParser()
		optionsParser.add_argument('-a', '--host', default="localhost", help="db hostname")
		optionsParser.add_argument('-u', '--user', required=True, help="db username")
		optionsParser.add_argument('-p', '--passwd', default="", help="db password")
		optionsParser.add_argument('-d', '--db', required=True, help="db name")
		optionsParser.add_argument('-c', '--clients', default=1, help="clients count (no concurrency = 1)")
		optionsParser.add_argument('-n', '--number', required=True, help="queries count (more queries - more precision")
		optionsParser.add_argument('-v', '--vebrose', help="if set to '1' then vebrose more is on")
		optionsParser.add_argument('-f', '--file', required=True, help="path to file contains sql query")
		cliOptions = optionsParser.parse_args()

		# init logger

		if "1" == cliOptions.vebrose:
			logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.DEBUG)
		else:
			logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.INFO)


		# setup input params

		self.threadsNumber = int(cliOptions.clients)
		self.queryFile = cliOptions.file
		self.queriesNumber = int(cliOptions.number)


		# get query from file

		self.query = open(self.queryFile, 'r').read()


		# queries distribution through threads

		queriesRests = self.queriesNumber

		for threadIdx in range(0, self.threadsNumber):
			self.threadsCapacity.append(0)

		while (queriesRests > 0):
			for threadIdx in range(0, self.threadsNumber):
				self.threadsCapacity[threadIdx] += 1
				queriesRests -= 1
				if queriesRests <= 0:
					break

		threadIdx = 0
		for threadCapcity in self.threadsCapacity:
			logging.debug("Thread #" + str(threadIdx) + " = " + str(threadCapcity))
			threadIdx += 1


		# init db pool

		logging.debug("Initializing db pool (count="+str(self.threadsNumber)+")")

		try:
			for dbConnIdx in range(0, self.threadsNumber):
				db = MySQLdb.connect(host=cliOptions.host, user=cliOptions.user, passwd=cliOptions.passwd, db=cliOptions.db)
				self.dbPool.append(db)
		except:
			logging.error("ERROR: can`t connect to database")
			sys.exit(-1)


	def run(self):

		# starting threads

		queriesDurations = []
		benchSession = benchsession.BenchSession()

		logging.debug("Initializing threads (count=" + str(self.threadsNumber) + ")")
		threadsList = []
		for threadIdx in range(0, self.threadsNumber):
		  queryThread = querythread.QueriesThread(benchSession, self.dbPool[threadIdx], self.query, self.threadsCapacity[threadIdx], queriesDurations)
		  threadsList.append(queryThread)
		  queryThread.start()


		# starting benchmark

		logging.debug("Starting threads")
		startTime = time.clock()
		benchSession.setState(1)
		for threadIdx in range(0, self.threadsNumber):
		  threadsList[threadIdx].join()
		total_duration = time.clock() - startTime


		# calculating stats

		basicReport = reports.BasicReport([50, 85, 90, 95, 99])
		basicReport.output(self.query, queriesDurations, total_duration)