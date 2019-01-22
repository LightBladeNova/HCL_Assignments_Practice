import os
import time
import csv

time_to_run_in_seconds = float(input("Enter how long script should run (in seconds): "))
timeout_start = time.time()

with open("android_data.csv", "w") as file:
	writer = csv.writer(file, lineterminator='\n')
	writer.writerow(["Current Foreground Package", "CPU Info", "DiskStats", "MemInfo", "Battery", "BatteryStats", "Wifi", "Wifi Additional Info", "mSignalStrength"])
	while time.time() < timeout_start + time_to_run_in_seconds:
		time.sleep(0.05)

		os.system("adb shell dumpsys usagestats > usagestats.txt")
		usagestats = open("usagestats.txt", "r")
		usagestats_lastline = usagestats.readlines()[-1]
		current_foreground_package = usagestats_lastline[usagestats_lastline.find("=") + 1:len(usagestats_lastline)]
		usagestats.close()

		os.system("adb shell dumpsys cpuinfo > cpuinfo.txt")
		cpuinfo = open("cpuinfo.txt", "r")
		cpuinfo_totals = cpuinfo.readlines()[-1]
		cpuinfo.close()

		os.system("adb shell dumpsys diskstats > diskstats.txt")
		diskstats = open("diskstats.txt", "r")
		diskstats_read = diskstats.readlines()
		diskstats_all = "" + diskstats_read[0][:-1]
		for i in range(1, len(diskstats_read)):
			diskstats_all += (", " + diskstats_read[i][:-1])
		diskstats.close()

		os.system("adb shell dumpsys meminfo > meminfo.txt")
		meminfo = open("meminfo.txt", "r")
		meminfo_read = meminfo.readlines()
		meminfo_read = meminfo_read[-5:]
		meminfo_RAM = "" + meminfo_read[0][:-1]
		for i in range(1, len(meminfo_read)):
			meminfo_RAM += (", " + meminfo_read[i][:-1])
		meminfo.close()

		os.system("adb shell dumpsys battery > battery.txt")
		battery = open("battery.txt", "r")
		battery_read = battery.readlines()
		battery_all = battery_read[0][:-1] + " " + battery_read[1][:-1]
		for i in range(2, len(battery_read)):
			battery_all += (", " + battery_read[i][:-1])
		battery.close()

		os.system("adb shell dumpsys batterystats > batterystats.txt")
		batterystats = open("batterystats.txt", "r")
		batterystats_read = batterystats.readlines()
		batterystats_start = -1;
		batterystats_end = -1
		batterystats_all = ""
		for i in range(0, len(batterystats_read)):
			if batterystats_start != -1 and batterystats_end != -1:
				break
			if batterystats_read[i].find("Statistics since last charge:") != -1:
				batterystats_start = i
			if batterystats_read[i].find("Resource Power Manager Stats") != -1:
				batterystats_end = i
		for i in range(batterystats_start, batterystats_end - 1):
			batterystats_all += (batterystats_read[i][:-1] + ", ")
		batterystats.close()

		os.system("adb shell dumpsys wifi > wifi.txt")
		wifi = open("wifi.txt", "r")
		wifi_read = wifi.readlines()
		wifi_info = wifi_read[0][:-1] + ", "
		wificonfigmanager_start = -1
		wificonfigmanager_end = -1
		for i in range(0, len(wifi_read)):
			if wificonfigmanager_start != -1 and wificonfigmanager_end != -1:
				break
			if wifi_read[i].find("WifiConfigManager - Configured networks Begin ----") != -1:
				wificonfigmanager_start = i
			if wifi_read[i].find("WifiConfigManager - Configured networks End ----") != -1:
				wificonfigmanager_end = i
		for i in range(wificonfigmanager_start, wificonfigmanager_end + 1):
			wifi_info += (wifi_read[i][:-1] + ", ")
		wifi.close()

		os.system("adb shell dumpsys wifi | grep RSSI: > mWifiInfo.txt")
		mWifiInfo = open("mWifiInfo.txt", "r")
		mWifiInfo_read = mWifiInfo.readlines()[0]
		mWifiInfo.close()

		os.system("adb shell dumpsys telephony.registry | grep 'mSignalStrength' > mSignalStrength.txt")
		mSignalStrength = open("mSignalStrength.txt", "r")
		mSignalStrength_read = mSignalStrength.readlines()[0]
		mSignalStrength.close()

		writer.writerow([current_foreground_package, cpuinfo_totals, diskstats_all, meminfo_RAM, battery_all, batterystats_all, wifi_info, mWifiInfo_read, mSignalStrength_read])
	file.close()