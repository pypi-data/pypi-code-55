import requests

isDev = True
url = 'https://llamalogs.com/'
if (isDev):
	url = 'http://localhost:4000/'

class LlamaProxy:

	@staticmethod
	def send_messages(currentLogs, currentStats):
		LlamaProxy.send_logs(currentLogs)
		LlamaProxy.send_stats(currentStats)

	@staticmethod
	def send_logs(currentLogs):
		log_list = []
		for sender in currentLogs:
			for receiver in currentLogs[sender]:
				log_list.append(currentLogs[sender][receiver].toAPIFormat())

		if (isDev):
			print("log_list")
			print(log_list)
		
		if (len(log_list)):
			try:
				requests.post(url + 'api/timelogs', json = {"time_logs": log_list})
			except:
				print('LlamaLogs Error; contacting llama logs server')

	@staticmethod
	def send_stats(currentStats):
		stat_list = []
		for component in currentStats:
			for name in currentStats[component]:
				stat_list.append(currentStats[component][name].toAPIFormat())

		if (isDev):
			print(stat_list)
		
		if (len(stat_list)):
			try:
				requests.post(url + 'api/timestats', json = {"time_stats": stat_list})
			except:
				print('LlamaLogs Error; contacting llama logs server')