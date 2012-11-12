import subprocess
import os
import StringIO
import time


def change_number_of_cities(newNum):
	try:
		f = open("route.dat", "r+")
		
		content = f.readlines()
		
		f.seek(0)
		
		f.write(str(newNum)+"\n")
		
		content.pop(0)
		
		for line in content:
        	
        		f.write(str(line))
		
		f.close()
	except:
		print "Error while trying to change number of cities"

MIN_NUM_CITIES = 10
MAX_NUM_CITIES = 16

MIN_NUM_WORKERS = 1
MAX_NUM_WORKERS = 8

NUM_RUNS = 5

FILE_NAMES = ["RaceTrap", "precode", "iterative"]
NOT_CILK = ["precode", "iterative"]

f = open("secound_results.txt", "w+")

f.write("FILENAME, NUM_CITIES, NUM_WORKERS, RUNTIME\n")

# Running different versions
for file in FILE_NAMES:

	# Running different number of cities
	for curr_num_cities in range(MIN_NUM_CITIES, MAX_NUM_CITIES+1):
		
		change_number_of_cities(curr_num_cities)
		
		# Running different number of workers
		for curr_num_workers in range(MIN_NUM_WORKERS, MAX_NUM_WORKERS+1):

			avg = []
			
			print "Filename", file, "\tCities: ", curr_num_cities, "\tWorkers ", curr_num_workers
			
			for run in range(NUM_RUNS):
				
				if file in NOT_CILK:
					output = os.popen("./" + file).read()
				else:
					output = os.popen("./" + file + " -cilk_set_worker_count=" + str(curr_num_workers)).read()
				
				output = StringIO.StringIO(output)
				
				x =  output.readline().split(" ")
				#print x
				
				sumRunning = 0
				
				for count in range(0, len(x)):
					if x[count] == "min.":
						
						sumRunning += int(x[count - 1]) * 60000
			
					if x[count] == "seconds":
						sumRunning += int(x[count -1])*1000
			
					if x[count] == "ms":
						ms =  int(x[count-1])
						sumRunning += ms   
						
				avg.append(sumRunning)		
				print "RUNTIME", sumRunning
			
			avg_runtime = sum(avg) / len(avg)
			print "AVG: ", avg_runtime
			results = "%s, %d, %d, %d \n" % (file, curr_num_cities, curr_num_workers, avg_runtime)
			f.write(results)
			if file in NOT_CILK:
				print "not cilk"
				break
f.close()
		
