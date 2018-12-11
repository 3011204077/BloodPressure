import csv
import matplotlib.pyplot as plt


ptt_file = csv.reader(open('1ppg and ecg.csv', 'r'))
i = 0
freq_list = []

for row in ptt_file:
	if i == 0:
		i += 1
		continue
	elif i == 1:
		prev = float(row[0])
		i += 1
		continue
	else:
		cur = float(row[0])
		freq = 1 / (cur - prev)
		freq_list.append(freq)
		print (freq)
		prev = cur
		i += 1

print (freq_list)
plt.plot(freq_list)
plt.show()