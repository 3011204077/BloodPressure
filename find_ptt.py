import csv
import matplotlib.pyplot as plt

def gen_time_ecg_ppg(file, wired_Y_N, start, end): #start: starting timestamp, end: ending timestamp, wired_Y_N: True of False
	file = csv.reader(open(file, 'r'))
	if wired_Y_N == True:
		start = start / 60
		end = end / 60
	time_list = []
	ecg_dict = {}
	ppg_dict = {}
	i = 0
	for row in file:
		if i == 0 or float(row[0]) <= start:#104:# 100:
			i += 1
			continue
		if float(row[0]) > end: #110:#120:
			break
		if wired_Y_N == False:
			time = float(row[0])
		else:
			time = float(row[0]) * 60
		time_list.append(time)
		ecg_dict[time] = float(row[1])
		ppg_dict[time] = float(row[2])
		i += 1
	return time_list, ecg_dict, ppg_dict

def find_ppg_peaks(ppg_dict, thresh_hight):
	ppg_peak_dict = {}
	ppg_peak_list = []
	ppg_low_peak_dict = {}
	ppg_low_peak_list = []
	ppg_change_dict = {}
	ppg_slope_dict = {}
	ppg_2nd_slope_dict = {}
	ppg_slope_filted_list = []
	for i in range(1, len(ppg_dict) - 1): ### actually for slope, it could use range(1,len(ppg_dict))
		if (((ppg_dict[time_list[i+1]] - ppg_dict[time_list[i]]) <= 0) and 
											((ppg_dict[time_list[i]] - ppg_dict[time_list[i-1]]) > 0)):
			ppg_change_dict[time_list[i]] = 1
		elif ((ppg_dict[time_list[i+1]] - ppg_dict[time_list[i]]) > 0) and ((ppg_dict[time_list[i]] - ppg_dict[time_list[i-1]]) < 0):
			ppg_change_dict[time_list[i]] = -1
		else:
			ppg_change_dict[time_list[i]] = 0
		ppg_slope_dict[time_list[i]] = (ppg_dict[time_list[i]] - ppg_dict[time_list[i-1]]) / (time_list[i+1] - time_list[i]) / 50
	
	##### generate the slope dict for high peaks, using threshould 15 here
	for (time, slope) in ppg_slope_dict.items():
		if slope > 15:
			ppg_slope_filted_list.append(time)

	##### generate the 2nd order slope, which is the slope of slope
	for i in range(2, len(ppg_slope_dict) - 1):
		ppg_2nd_slope_dict[time_list[i]] = (ppg_slope_dict[time_list[i]] - ppg_slope_dict[time_list[i-1]]) / (time_list[i+1] - time_list[i])

	for entry in ppg_change_dict.keys():
		if ppg_change_dict[entry] == 1:
			ppg_peak_dict[entry] = ppg_dict[entry]
			ppg_peak_list.append(entry)
		elif ppg_change_dict[entry] == -1:
			ppg_low_peak_dict[entry] = ppg_dict[entry]
			ppg_low_peak_list.append(entry)
		else:
			ppg_peak_dict[entry] = 0
			ppg_low_peak_dict[entry] = 0

	ppg_peak_final_dict = {}
	ppg_peak_final_dict_2 = {}
	ppg_peak_final_list = []
	ppg_peak_final_list_2 = []
	flat_group = []

	if thresh_hight > 0:
		for (time, value) in ppg_peak_dict.items():
			if value > thresh_hight:
				ppg_peak_final_dict[time] = value
				ppg_peak_final_list.append(time)
			else:
				ppg_peak_final_dict[time] = 0
	else:
		ppg_peak_final_dict = ppg_peak_dict
		ppg_peak_final_list = ppg_peak_list
	#i = 0
	'''
	##### to detect the flat area and take the middle as the peak, will cause bug in some siuation
	for i in range(len(ppg_peak_final_list) - 1):
		if ppg_peak_final_list[i+1] - ppg_peak_final_list[i] < 0.15: #define the threshould to detect the flat area, could be delete in later version
			flat_group.append(ppg_peak_final_list[i])
		else:
			if flat_group == []:
				ppg_peak_final_list_2.append(ppg_peak_final_list[i])
				continue
			else:
				flat_group.append(ppg_peak_final_list[i])
				ppg_peak_final_list_2.append(flat_group[int(len(flat_group) / 2)])
				flat_group = []

	##### to take care of the last peak
	if flat_group != []:
		flat_group.append(ppg_peak_final_list[-1])
		ppg_peak_final_list_2.append(flat_group[int(len(flat_group) / 2)])
	else:
		ppg_peak_final_list_2.append(ppg_peak_final_list[-1])

	##### create the dict for the final peaks
	for time in ppg_peak_final_dict.keys():
		if time in ppg_peak_final_list_2:
			ppg_peak_final_dict_2[time] = ppg_peak_final_dict[time]
		else:
			ppg_peak_final_dict_2[time] = 0
	'''

	ppg_peak_final_dict_2 = ppg_peak_final_dict
	ppg_peak_final_list_2 = ppg_peak_final_list	

	##### apply the filter(interval, assume heart rate < 160/min, then interval should > 0.375s; height, the 
	##### difference between neighbour peaks should smaller than a specific threshould)
	ppg_peak_final_dict_3 = {}
	ppg_peak_final_list_3 = []
	# i = 0
	# j = 0
	# print (ppg_peak_final_list_2)
	# for i in range(1, len(ppg_peak_final_list_2) - 1):
	# 	cur_time = ppg_peak_final_list_2[j]
	# 	next_time = ppg_peak_final_list_2[i]
	# 	if (next_time - cur_time) > 0.375 and abs(ppg_peak_dict[cur_time] - ppg_peak_dict[next_time]) < 0.3:
	# 		#ppg_peak_final_dict_3[ppg_peak_final_list_2[i]] = ppg_peak_dict[ppg_peak_final_list_2[i]]
	# 		ppg_peak_final_list_3.append(cur_time)
	# 		j = i
	# 	# else:
	# 	# 	ppg_peak_final_dict_3[ppg_peak_final_list_2[i]] = 0

	# for time in ppg_peak_final_dict_2.keys():
	# 	if time in ppg_peak_final_list_3:
	# 		ppg_peak_final_dict_3[time] = ppg_peak_dict[time]
	# 	else:
	# 		ppg_peak_final_dict_3[time] = 0

	##### use the 2nd derivate to filt the ppg peaks, set the threshould for real peaks to -3.5
	for time in (ppg_peak_final_list_2):
		if ppg_2nd_slope_dict[time] < -3.5:
			ppg_peak_final_list_3.append(time)
	for (time, value) in ppg_peak_final_dict_2.items():
		if time in ppg_peak_final_list_3:
			ppg_peak_final_dict_3[time] = value
		else:
			ppg_peak_final_dict_3[time] = 0

	return ppg_peak_final_dict_3, ppg_peak_final_list_3, ppg_2nd_slope_dict, ppg_low_peak_dict

def find_ecg_peaks(ecg_dict, thresh_hight):
	ecg_peak_dict = {}
	ecg_peak_list = []
	ecg_change_dict = {}
	ecg_slope_dict = {}

	ecg_peak_final_dict = {}
	ecg_peak_final_dict_2 = {}
	ecg_peak_final_list = []
	ecg_peak_final_list_2 = []

	for i in range(1, len(ecg_dict) - 1):
		ecg_change_dict[time_list[i]] = (((ecg_dict[time_list[i+1]] - ecg_dict[time_list[i]]) <= 0) and 
										((ecg_dict[time_list[i]] - ecg_dict[time_list[i-1]]) > 0))
		ecg_slope_dict[time_list[i]] = (ecg_dict[time_list[i]] - ecg_dict[time_list[i-1]]) / (time_list[i] - time_list[i-1])
	
	for entry in ecg_change_dict.keys():
		if ecg_change_dict[entry] == True:
			ecg_peak_dict[entry] = ecg_dict[entry]
			ecg_peak_list.append(entry)
		else:
			ecg_peak_dict[entry] = 0
	
	if thresh_hight > 0:
		for entry in ecg_peak_dict.keys():
			if ecg_peak_dict[entry] > thresh_hight: #0.0005: #and (ecg_peak_dict.keys()[i+1] - ecg_peak_dict.keys()[i]) < 0.375
				ecg_peak_final_dict[entry] = ecg_peak_dict[entry]
				ecg_peak_final_list.append(entry)
			else:
				#continue
				ecg_peak_final_dict[entry] = 0
	else:
		ecg_peak_final_dict = ecg_peak_dict

	return ecg_peak_final_dict, ecg_peak_final_list

#def find rrs(ecg_peak_dict, ecg_peak_list):

def gen_ptt(ecg_peak_dict, ecg_peak_list, ppg_peak_dict, ppg_peak_list):
	min_length = min(len(ecg_peak_list), len(ppg_peak_list))
	i = 0
	j = 0
	ppg_peak_ecgtime = {}
	ptt = {}
	while i < min_length and j < min_length:
		diff = ppg_peak_times_final[j] - ecg_peak_times_final[i] #### create a ppg/ecg peak time mapping dict: {ecg_peak_time, ppg_peak_time}
		if 0.12 < diff <= 0.25:
			ppg_peak_ecgtime[ecg_peak_times_final[i]] = ppg_peak_times_final[j]
			ptt[ecg_peak_times_final[i]] = diff
			i += 1
			j += 1
		elif diff < 0:
			j += 1
		elif diff > 0.3:
			i += 1
	return ptt, ppg_peak_ecgtime


time_list, ecg_dict, ppg_dict = gen_time_ecg_ppg('BIOPAC_RAVI_ECG_PPG_SIT.csv', True, 15, 300)
ppg_peak_final_dict, ppg_peak_final_list, ppg_slope_dict, ppg_low_peak_dict = find_ppg_peaks(ppg_dict, 0)
ecg_peak_final_dict, ecg_peak_final_list = find_ecg_peaks(ecg_dict, 0.45)
print (len(ppg_peak_final_list))
print (len(ecg_peak_final_list))

#print (len(ppg_peak_final_dict)) 
#print (len(ecg_peak_final_dict))
#ptt, ppg_peak_ecgtime = gen_ptt(ecg_peak_final_dict, ecg_peak_list, ppg_peak_final_dict, ecg_peak_final_list)
#file = csv.reader(open('BIOPAC_RAVI_ECG_PPG_SIT.csv', 'r'))
#file = csv.reader(open('11-26/wireless_RAVI_ECG_PPG_LOW_STIM.csv', 'r'))
#file = csv.reader(open('11-27/wireless-Fei-Lead I-PPG-siiting.csv', 'r'))

# time_list = []
# ecg_dict = {}
# ppg_dict = {}
# #ecg_list = []
# #ppg_list = []
# ppg_slope_dict = {}
# ppg_change_dict = {}
# ecg_slope_dict = {}
# ecg_change_dict = {}
# ppg_peak_dict = {}
# #ppg_peak_final_dict = {}
# ecg_peak_dict = {}
# ecg_peak_final_dict = {}
# ecg_peak_final_dict_2 = {}

# i = 0

# for row in file:
# 	if i == 0 or float(row[0]) <= 104:# 100:
# 		i += 1
# 		continue
# 	if float(row[0]) > 110:#120:
# 		break
# 	time_list.append(float(row[0]))
# 	ecg_dict[float(row[0])] = float(row[2])
# 	ppg_dict[float(row[0])] = float(row[1])
# 	i += 1

# for i in range(1, len(ecg_dict) - 1):
# 	ppg_change_dict[time_list[i]] = (((ppg_dict[time_list[i+1]] - ppg_dict[time_list[i]]) <= 0) and 
# 										((ppg_dict[time_list[i]] - ppg_dict[time_list[i-1]]) > 0))
# 	ppg_slope_dict[time_list[i]] = (ppg_dict[time_list[i]] - ppg_dict[time_list[i-1]]) / (time_list[i+1] - time_list[i])
# #print (ppg_change_dict)
# for i in range(1, len(ecg_dict) - 1):
# 	ecg_change_dict[time_list[i]] = (((ecg_dict[time_list[i+1]] - ecg_dict[time_list[i]]) <= 0) and 
# 									((ecg_dict[time_list[i]] - ecg_dict[time_list[i-1]]) > 0))
# 	ecg_slope_dict[time_list[i]] = (ecg_dict[time_list[i]] - ecg_dict[time_list[i-1]]) / (time_list[i] - time_list[i-1])

# for entry in ppg_change_dict.keys():
# 	if ppg_change_dict[entry] == True:
# 		ppg_peak_dict[entry] = ppg_dict[entry]
# 	else:
# 		ppg_peak_dict[entry] = 0
# for entry in ecg_change_dict.keys():
# 	if ecg_change_dict[entry] == True:
# 		ecg_peak_dict[entry] = ecg_dict[entry]
# 	else:
# 		ecg_peak_dict[entry] = 0

# ####### apply the filter(value(hight) threshould)

# for entry in ecg_peak_dict.keys():
# 	if ecg_peak_dict[entry] > 0.0005: #and (ecg_peak_dict.keys()[i+1] - ecg_peak_dict.keys()[i]) < 0.375
# 		ecg_peak_final_dict[entry] = ecg_peak_dict[entry]
# 	else:
# 		#continue
# 		ecg_peak_final_dict[entry] = 0

# ####### apply the filter(time interval, no shorter than the interval of 160 beats/min) compare to ppg, set the ptt to (150-250)ms

# ecg_peak_list = []
# temp = []

# for entry in ecg_peak_final_dict.keys():
# 	if ecg_peak_final_dict[entry] != 0:
# 		ecg_peak_list.append(entry)
# print (ecg_peak_list)
# temp.append(ecg_peak_list[0])
# for entry in ecg_peak_list:
# 	if (entry - temp[-1]) < 0.375:
# 		continue
# 	else:
# 		temp.append(entry)
# for entry in ecg_peak_final_dict.keys():
# 	if entry in temp:
# 		ecg_peak_final_dict_2[entry] = ecg_peak_dict[entry]
# 	else:
# 		ecg_peak_final_dict_2[entry] = 0

# ppg_peak_final_dict_2, ppg_peak_final_list_2 = find_ppg_peaks(ppg_peak_dict, 2.5)

# '''
# ppg_temp_list = []
# ppg_temp_list.append(0)
# for entry in ppg_change_dict.keys():
# 	if ppg_change_dict[entry] == True:
# 		ppg_temp_list.append(ppg_dict[entry])
# 	else:
# 		ppg_temp_list.append(0)
# ppg_temp_list.append(0)
# '''

# '''
# ecg_temp_list = []
# ecg_temp_list.append(0)
# for entry in ecg_change_dict.keys():
# 	if ecg_change_dict[entry] == True:
# 		ecg_temp_list.append(ecg_dict[entry])
# 	else:
# 		ecg_temp_list.append(0)
# ecg_temp_list.append(0)
# '''
# ampli_ecg = []
# for entry in ecg_dict.values():
# 	ampli_ecg.append(entry* 100)

#plt.plot(time_list, ampli_ecg)
plt.plot(time_list, ecg_dict.values())
#plt.plot(time_list, ppg_dict.values())
#plt.plot(ecg_peak_dict.keys(), ecg_peak_dict.values())
plt.plot(ecg_peak_final_dict.keys(), ecg_peak_final_dict.values())
#plt.plot(time_list, ppg_temp_list)
#plt.plot(ecg_slope_dict.keys(), ecg_slope_dict.values())
#plt.plot(ppg_peak_dict.keys(), ppg_peak_dict.values())
#plt.plot(ppg_peak_final_dict.keys(), ppg_peak_final_dict.values())
#plt.plot(ppg_low_peak_dict.keys(), ppg_low_peak_dict.values())
#plt.plot(ppg_slope_dict.keys(), ppg_slope_dict.values())
# plt.plot(time_list, ecg_dict.values())
# plt.plot(time_list, ecg_temp_list)
plt.show()