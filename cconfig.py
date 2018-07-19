"""
Example script for fetching the configuration of a given environment and putting it to another one.
"""
import requests, ssl, time

SRC_URL = 'YOUR_DYNATRACE_ENVIRONMENT_URL'
SRC_TOKEN = 'YOUR_DYNATRACE_CONFIG_API_TOKEN'
SRC_HEADERS = {'Authorization': 'Api-Token ' + SRC_TOKEN}

DST_URL = 'YOUR_DYNATRACE_ENVIRONMENT_URL'
DST_TOKEN = 'YOUR_DYNATRACE_CONFIG_API_TOKEN'
DST_HEADERS = {'Authorization': 'Api-Token ' + DST_TOKEN, 'Content-Type' : 'application/json; charset=utf-8'}

def copyList(list_type):
	try:
		r = requests.get(SRC_URL + '/api/config/v1/' + list_type, headers=SRC_HEADERS)
		print("%s copy list: %d" % (list_type, r.status_code))
		res = r.json()
		for entry in res['values']:
			#time.sleep(1)
			print(entry['id'])
			tr = requests.get(SRC_URL + '/api/config/v1/' + list_type + '/' + entry['id'], headers=SRC_HEADERS)
			dp = requests.put(DST_URL + '/api/config/v1/' + list_type + '/' + entry['id'], json=tr.json(), headers=DST_HEADERS)
			if dp.status_code > 204:
				print("%s put: %d" % (list_type, dp.status_code))
				print(dp.text)
	except ssl.SSLError:
		print("SSL Error")

def getListPaths():
	try:
		r = requests.get(SRC_URL + '/api/config/v1/spec2.json')
		spec = r.json()
		for path in spec['paths']:
			if path.endswith('{id}') and "validator" not in path:
				print(path)
	except ssl.SSLError:
		print("SSL Error")


# Need chcp 65001 on PowerShell 
def main():
	#getListPaths()
	copyList('applications/web')
	copyList('autoTags')
	copyList('requestAttributes')
	copyList('managementZones')
	copyList('anomalyDetection/diskEvents')


if __name__ == '__main__':
	main()



