
import time
import threading

class QueriesThread(threading.Thread):
    
	def __init__(self, bench_session, db, sql_query, queries_count, querires_durations):
		threading.Thread.__init__(self)
		self.db = db
		self.sqlQuery = sql_query
		self.queriesCount = queries_count
		self.queriesDurations = querires_durations
		self.benchSession = bench_session


	def run(self):

		# waiting benchmark start
		while (self.benchSession.getState() == 0):
			pass

		# process N queries
		for queryIdx in range(0, self.queriesCount):
			
			queryStartTime = time.clock()
			cur = self.db.cursor() 
			cur.execute(self.sqlQuery)
			queryEndTime = time.clock()

			self.queriesDurations.append(queryEndTime-queryStartTime)
		return True