import json, requests

class HTTPRPCCore:
	"""HTTP RPC core function"""
	def __init__(self, fonera_ip):
		self.fonera_ip = fonera_ip
		

	def build_http_rpc_url(self, sid):
		if sid == 0:
			return 'http://' + self.fonera_ip +'/api/00000000000000000000000000000000'
		else:
			return 'http://' + self.fonera_ip +'/api/' + str(sid)

	def build_http_rpc_data(self, data):
		return [ { "jsonrpc": "2.0", "id": 1, "method": "call", "params": data } ]

	def run_httprpc_call(self, data, sid):
		headers = {'content-type': 'application/json'}
		full_data = self.build_http_rpc_data(data)
		try:
			resp = requests.post(url=self.build_http_rpc_url(sid),
						headers={'content-type': 'application/json'},
						data=json.dumps(full_data))
			resp_data = json.loads(resp.content)
			return resp_data

		except requests.HTTPError, e:
			print 'HTTP ERROR %s occured' % e.code

	def print_json(json):
		print "0) " + str(json) + " - " + type(json).__name__
		for key, val in json.iteritems():
			print "1) " + key + " - " + str(val) + " - " + type(val).__name__

			# list
			if type(val).__name__ in ('list'):
				for subkey in val:
					print "2) " + str(subkey) + " - " + type(subkey).__name__
					if type(subkey).__name__ in ('dict'):
						print_json(subkey)
			# tuple
			elif type(val).__name__ in ('tuple'):
				print_json(val)

		return

'''
	def search_key_in_json(self, json, searchkey):
		for key, val in json.iteritems():
			print "1) " + str(key) + " - " + str(val)
			if searchkey == key:
				return val

			# list
			if type(val).__name__ in ('list', 'dict'):
				for item in val:
					if searchkey == item:
						return val
					else:
						if type(item).__name__ in ('dict', 'list'):
							return self.search_key_in_json(item, searchkey)
'''

