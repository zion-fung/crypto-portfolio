import requests, tkinter as tk, sys
from lxml import html
from functools import partial
def listIndex(l, element):
	for i in range(len(l)):
		if l[i] == element:
			return i
	return -1
apiTicker = "https://api.coinmarketcap.com/v1/ticker/"
file = open("info.txt", "r").read().splitlines()
coins = file[0].split("|")
quantity = file[1].split("|")
approxInvestment = file[2].split("|")
amountSpent = file[3]
# coins = ["cardano", "iota", "ark", "raiblocks", "request-network"]
# quantity = [110.889, 18.981, 11.34186, 2.53874, 134.865]
# approxInvestment = [30, 20, 61, 30, 60]
data = []
if len(coins) != len(quantity) or len(quantity) != len(approxInvestment) or len(coins) != len(approxInvestment):
	print("Length of three lists are not equal")
	sys.exit()
class apiIndex:
	id = 2
	name = 3
	symbol = 4
	rank = 5
	price_usd = 6
	price_btc = 7
	#24_volume = 8
	market_cap_usd = 9
	available_supply = 10
	total_supply = 11
	max_supply = 12
	percent_change_1h = 13
	percent_change_24h = 14
	percent_change_7d = 15
	last_updated = 16
# [1] is header ("id", "name", ...) [3] is value
def requestData():
	data.clear()
	for coin in coins:
		data.append(requests.get(apiTicker + coin).text.splitlines())
def getLine(coin, lineIndex):
	# return requests.get(apiTicker + coin).text.splitlines()[lineIndex].split("\"")
	coinIndex = listIndex(coins, coin)
	return data[coinIndex][lineIndex].split("\"")
def getPrices():
	prices = []
	for coin in coins:
		prices.append(getLine(coin, apiIndex.price_usd)[3])
	return prices
def getPercent(x):
	percent = []
	lineIndex = -1
	if x == 1: # 1 hour
		lineIndex = apiIndex.percent_change_1h
	elif x == 24: # 24 hour
		lineIndex = apiIndex.percent_change_24h
	elif x == 7: # 7 day
		lineIndex = apiIndex.percent_change_7d
	if lineIndex == -1:
		return []
	for coin in coins:
		percent.append(getLine(coin, lineIndex)[3])
	return percent
def getTotalValue():
	values = getPrices()
	total = 0
	counter = 0
	for val in values:
		total += (float(val) * quantity[counter])
		counter += 1
	return total
def getTotalInvestment():
	total = 0
	for invest in approxInvestment:
		total += int(invest)
	return total - int(amountSpent)
def getProfitPercent():
	totalValue = getTotalValue()
	totalInvestment = getTotalInvestment()
	return totalValue / totalInvestment * 100
def getProfitPercent(totalValue):
	totalInvestment = getTotalInvestment()
	return float(totalValue) / totalInvestment * 100
def makeGUI():
	def saveInfo():
		file = open("info.txt", "w")
		length = len(coins)
		for i in range(length):
			file.write(coins[i])
			if i < length - 1:
				file.write("|")
		file.write("\r\n")
		for i in range(length):
			file.write(quantityEntries[i].get())
			if i < length - 1:
				file.write("|")
		file.write("\r\n")
		for i in range(length):
			file.write(approxInvestment[i])
			if i < length - 1:
				file.write("|")
		# for coin in coins:
		# 	file.write(coin)
		# 	file.write("|")
		# file.write("\r\n")
		# for quan in quantityEntries:
		# 	file.write(quan.get())
		# 	file.write("|")
		# file.write("\r\n")
		# for ai in approxInvestment:
		# 	file.write(ai)
		# 	file.write("|")
		file.close()
	def reloadGUI():
		gui.destroy()
		file = open("info.txt", "r").read().splitlines()
		coins = file[0].split("|")
		quantity = file[1].split("|")
		approxInvestment = file[2].split("|")
		print(coins, quantity, aprroxInvestment)
		makeGUI()
	def calculateTotal():
		total = 0
		for val in values:
			total += float(val.get())
		return total
	def refreshValues():
		requestData()
		new_one_hour = getPercent(1)
		new_twentyfour_hour = getPercent(24)
		new_seven_day = getPercent(7)
		newPrices = getPrices()
		for i in range(len(coins)):
			priceLabels[i].set(str("%.3f" % float(newPrices[i])))
			s = float(quantityEntries[i].get()) * float(newPrices[i])
			# values[i].set(str("%.3f" % float(s)))
			values[i].set(str("{:.3f}".format(s)))
			# one_hour[i].set(str("%.3f" % float(new_one_hour[i])))
			one_hour[i].set(str("{:.3f}".format(float(new_one_hour[i]))))
			# twentyfour_hour[i].set(str(".3f" % float(new_twentyfour_hour[i])))
			twentyfour_hour[i].set("{:.3f}".format(float(new_twentyfour_hour[i])))
			# seven_day[i].set(str("%.3f" % float(new_seven_day[i])))
			seven_day[i].set(str("{:.3f}".format(float(new_seven_day[i]))))
		totalValue.set(str("%.3f" % calculateTotal()))
		percentChange.set(str("%.3f" % getProfitPercent(totalValue.get())))
	requestData()
	gui = tk.Tk()
	gui.title("Crypto Portfolio")
	# Column Labels
	tk.Label(gui, text = "Coin").grid(row = 0, column = 0)
	tk.Label(gui, text = "Quantity").grid(row = 0, column = 1)
	tk.Label(gui, text = "Price").grid(row = 0, column = 2)
	tk.Label(gui, text = "Value").grid(row = 0, column = 3)
	tk.Label(gui, text = "1 day").grid(row = 0, column = 4)
	tk.Label(gui, text = "24 hour").grid(row = 0, column = 5)
	tk.Label(gui, text = "7 day").grid(row = 0, column = 6)
	# Some buttons on the end
	# tk.Button(gui, text = "Reload", command = reloadGUI).grid(row = 0, column = 7)
	tk.Button(gui, text = "Refresh", command = refreshValues).grid(row = 1, column = 7)
	tk.Button(gui, text = "Save", command = saveInfo).grid(row = 2, column = 7)
	# First Column (names of coins)
	for i in range(len(coins)):
		tk.Label(gui, text="%s"%(coins[i])).grid(row = i + 1, column = 0)
	# Second Column (quantity of coins)
	quantityEntries = []
	for i in range(len(quantity)):
		var = tk.StringVar()
		var.set(quantity[i])
		quantityEntries.append(var)
		tk.Entry(gui, textvariable = var).grid(row = i + 1, column = 1)
	# Third Column (prices of coins)
	prices = getPrices()
	priceLabels = []
	for i in range(len(prices)):
		var = tk.StringVar()
		var.set(str("%.3f" % float(prices[i])))
		priceLabels.append(var)
		tk.Label(gui, textvariable = var).grid(row = i + 1, column = 2)
	# Fourth Column (values of each holding)
	values = []
	for i in range(len(coins)):
		var = tk.StringVar()
		quan = quantityEntries[i].get()
		s = float(quan) * float(prices[i])
		var.set(str("%.3f" % s))
		values.append(var)
		tk.Label(gui, textvariable = var).grid(row = i + 1, column = 3)
	# Fifth Column (% change 1h)
	one_hour = []
	for i in range(len(coins)):
		var = tk.StringVar()
		change = getPercent(1)
		var.set(str("%.3f" % float(change[i])))
		one_hour.append(var)
		tk.Label(gui, textvariable = var).grid(row = i + 1, column = 4)
	# Sixth Column (% change 24h)
	twentyfour_hour = []
	for i in range(len(coins)):
		var = tk.StringVar()
		change = getPercent(24)
		var.set(str("%.3f" % float(change[i])))
		twentyfour_hour.append(var)
		tk.Label(gui, textvariable = var).grid(row = i + 1, column = 5)
	# Seventh Column (% change 7d)
	seven_day = []
	for i in range(len(coins)):
		var = tk.StringVar()
		change = getPercent(7)
		var.set(str("%.3f" % float(change[i])))
		seven_day.append(var)
		tk.Label(gui, textvariable = var).grid(row = i + 1, column = 6)
	# End information
	tk.Label(gui, text = "Total value:").grid(row = len(coins) + 1, column = 6)
	totalValue = tk.StringVar()
	totalValue.set(str("%.3f" % calculateTotal()))
	tk.Label(gui, textvariable = totalValue).grid(row = len(coins) + 1, column = 7)
	tk.Label(gui, text = "% change: ").grid(row = len(coins) + 2, column = 6)
	percentChange = tk.StringVar()
	percentChange.set(str("%.3f" % getProfitPercent(totalValue.get())))
	tk.Label(gui, textvariable = percentChange).grid(row = len(coins) + 2, column = 7)
	gui.mainloop()
makeGUI()
# requestData()
# print(getPrices())
# print(coins)
# print(getLine("cardano", apiIndex.price_usd))
# print(getLine("iota", apiIndex.price_usd))
# print(getLine("ark", apiIndex.price_usd))