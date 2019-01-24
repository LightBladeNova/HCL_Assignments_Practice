import os
import time
import sqlite3
from collections import Counter
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def createLogcatDatabase():
	# Create log table if it doesn't exist
	conn = sqlite3.connect('log_analytics.sqlite')
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS Log_Analytics")
	cursor.execute("CREATE TABLE IF NOT EXISTS Log_Analytics (Date VARCHAR, Code VARCHAR, Service VARCHAR)")
	conn.commit()
	conn.close()

def readLogcatIntoDatabase():
	# Read logcat and extract information, store into database
	conn = sqlite3.connect('log_analytics.sqlite')
	cursor = conn.cursor()
	time_to_run_in_seconds = float(input("Get most recent logcat lines since [enter number] seconds ago: "))
	timeout = time.time() - time_to_run_in_seconds
	os.system("adb logcat -t " + str(timeout) + " > logcat.txt")
	with open("logcat.txt", "r") as logcat_file:
		logcat_lines = [line for line in logcat_file.readlines() if "-----" not in line]
		for line in logcat_lines:
			line_data = line.split()
			date = line_data[0] + " " + line_data[1]
			code = line_data[4]
			service = line_data[5]
			cursor.execute("INSERT INTO Log_Analytics VALUES (?, ?, ?)", (date, code, service))
			conn.commit()
		logcat_file.close()

	# Get codes information from database
	cursor.execute("SELECT * FROM Log_Analytics")
	data = cursor.fetchall()
	conn.close()
	return data

def plotLogcatCodes(data):
	# Plot logcat codes from data
	counter = Counter(elem[1] for elem in data)
	codes_nums = {key: value for (key, value) in counter.items()}

	codes_names = ["Dalvikvm", "Error", "Fatal Error", "Information", "Verbose", "Warning"]
	codes_letters = ["D", "E", "F", "I", "V", "W"]
	codes = list(zip(codes_names, codes_letters))
	frequencies = [(codes_nums[code_letter] if code_letter in codes_nums else 0) for code_letter in codes_letters]
	y_pos = np.arange(len(codes))
	 
	plt.barh(y_pos, frequencies, align='center', alpha=0.5)
	plt.yticks(y_pos, codes)
	plt.xlabel('Frequency')
	plt.title('Logcat Codes')
	for i, v in enumerate(frequencies):
	    plt.text(v, i, str(v), color='black', fontweight='bold')
	plt.tight_layout()
	plt.savefig('Logcat_Codes.png')

if __name__ == '__main__':
	createLogcatDatabase()
	data = readLogcatIntoDatabase()
	plotLogcatCodes(data)