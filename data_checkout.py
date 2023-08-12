import matplotlib.pyplot as plt

with open("cps_grapher.txt") as file:
    data_list= [(int(line.split()[0]), float(line.split()[1])) for line in file]

time_list = []
cps_list = []
for time, cps in data_list:
    time_list.append(time)
    cps_list.append(cps)


plt.plot(time_list, cps_list, color='b')
plt.title("CPS over time")
plt.xlabel("Seconds Passed")
plt.ylabel("CPS")
plt.show()