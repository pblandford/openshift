import httplib
import jsonpickle

url = "android.googleapis.com"
apiKey = "AIzaSyBHKZHknfNzOxsr51VW7jqKMY9kMUpE2mA"

def sendMessage(registration_ids):
	headers = { "Content-type" : "application/json", "Authorization", "key=" + apiKey }

	params = { "registration_ids" : registration_ids, "data" : "test_data" }
	data = jsonpickle.encode(params, unpickleable=False)

	connection = httplib.HTTPSConnection(url)
	connection.request("POST", "gcm/send", data, headers) 

	response = connection.getresponse()

	print response

	
