"""
Example script for fetching the configuration of a given environment and store it in a directory structure. 
"""
import requests, ssl, os

SRC_URL = 'YOUR_DYNATRACE_ENVIRONMENT_URL'
SRC_TOKEN = 'YOUR_DYNATRACE_CONFIG_API_TOKEN'
SRC_HEADERS = {'Authorization': 'Api-Token ' + SRC_TOKEN}

def save(path, file, content):
	if not os.path.isdir(os.getcwd() + path): 
		os.makedirs(os.getcwd() + path)
	with open(os.getcwd() + path + "/" + file, "w") as text_file:
		text_file.write("%s" % content)

def saveList(list_type):
	try:
		r = requests.get(SRC_URL + '/api/config/v1/' + list_type, headers=SRC_HEADERS)
		print("%s save list: %d" % (list_type, r.status_code))
		res = r.json()
		for entry in res['values']:
			print(entry['id'])
			tr = requests.get(SRC_URL + '/api/config/v1/' + list_type + '/' + entry['id'], headers=SRC_HEADERS)
			# save tr.json()
			save('/api/config/v1/' + list_type + '/', entry['id'], tr.json())
	except ssl.SSLError:
		print("SSL Error")


def saveSingleton(singleton_type):
	try:
		r = requests.get(SRC_URL + '/api/config/v1/' + singleton_type, headers=SRC_HEADERS)
		print("%s save singleton: %d" % (singleton_type, r.status_code))
		save('/api/config/v1/', singleton_type, r.json())
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

def main():
	#getListPaths()	
	saveList('autoTags')
	saveList('services/requestAttributes')
	saveList('managementZones')
	saveList('anomalyDetection/diskEvents')
	saveList('applications/web')
	saveSingleton('applicationDetection')
	saveSingleton('anomalyDetection/aws')
	saveSingleton('anomalyDetection/hosts')
	saveSingleton('anomalyDetection/services')
	saveSingleton('dataPrivacy')
	
if __name__ == '__main__':
	main()



