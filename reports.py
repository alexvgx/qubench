
import math

class BasicReport(object):

	def __init__(self, percentiles):

		self.percentiles = percentiles


	def output(self, sql_query, durations_list, total_duration):
		
		print "\nSQL:"
		print "\n %s\n" % sql_query

		durations_list.sort()

		# summary stat

		queriesPerSecond = len(durations_list) / total_duration
		maxDuration = durations_list[len(durations_list)-1]*1000
		minDuration = durations_list[0]*1000

		print "\n-----------------------------------------"
		print "\nExecution time:"
		print "\n %.2fs (%.1f rps)" % (total_duration, queriesPerSecond)
		print "\n-----------------------------------------"
		print "\nMin - Max:"
		print "\n %.2f ms - %.2f ms" % (minDuration, maxDuration)
		print "\n-----------------------------------------"

		# percentile stat

		print "\nPercentiles: "
		print "\n"

		for percentile in self.percentiles:
			percentPosition = int(math.ceil((len(durations_list)-1) * percentile / 100))
			print " " + str(percentile) + ":  %.2f ms" % (durations_list[percentPosition]*1000)

		print "\n-----------------------------------------"
