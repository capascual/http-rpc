import json, requests, time
from httprpccore import HTTPRPCCore

# version:		1.0
# description:	Instructions to install: apt-get install python-request, python-json
# 				This script tests Utility app 1.2
# 				https://docs.google.com/a/fon.com/document/d/1TfF0BwHM1wl8lRqx5njMW3I8bIZHK7zVJKqm2jx5xZc/edit#
#				utility_app_get = [
#					[ "anet", "status", {} ],
#					[ "anet", "ssid_scan", {"iface":"radio"} ],
#					[ "anet", "get_ssids", {} ],
#					[ "anet", "get_gramoname", {} ],
#					[ "mfgd", "get_fonmac", {} ],
#					[ "hotspotd", "get", {"section":"main", "options":["nasid"]}],
#					[ "wifid", "get_wiface", {"name":"private", "option":"key"} ],
#				]

#				utility_app_set = [
#					[ "anet", "set_gramoname", {"mdnsname" :test_gramoname} ],
#					[ "wifid", "set_wiface", {"name" :"private", "ssid": test_private_SSID , "encryption":"wpa2", "key": test_private_wpakey, "mode": "bgn"} ],
#					[ "anet", "wiclirouted", {"proto":"dhcp", "ssid":test_private_SSID} ],
#					[ "anet", "wiclone", {"ssid" :test_private_SSID, "encryption":"psk2", "key":test_private_wpakey}],
#					[ "anet", "ethrouted", {"proto":"dhcp"} ]
#				]

def get_login_sid(my_httprpc):
	#curl -i -H "Accept: application/json" -X POST  -d '{ "jsonrpc": "2.0", "id": 1, "method": "call", "params": [ "session", "login", { "username": "admin", "password": "admin" } ] }' http://192.168.10.1/api/00000000000000000000000000000000

	#login_data = [ { "jsonrpc": "2.0", "id": 1, "method": "call", "params": [ "session", "login", { "username": "admin", "password": "admin" } ] } ]
	login_data = my_httprpc.build_http_rpc_data( [ "session", "login", { "username": "admin", "password": "admin" } ])
	try:
		resp = requests.post(url=my_httprpc.build_http_rpc_url(0),
					headers={'content-type': 'application/json'},
					data=json.dumps(login_data))
		resp_data = json.loads(resp.content)
		return my_httprpc.search_key_in_json(resp_data[0], "sid")

	except requests.HTTPError, e:
		print 'HTTP ERROR %s occured' % e.code



test_private_ssid="test_priv_ssid"
test_private_wpakey="12345678"

test_master_ap_ssid="thisssiddoesnotexists"
test_master_ap_wpakey="12345678"

test_gramoname="auto_test_httrpc_gramoname"



def test_anetd_setgramofonname(sid, test_gramoname):
	data = [ "anet", "set_gramofonname", {"mdnsname" :test_gramoname, "spotifyname": test_gramoname}]
	# print data
	# print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))

def test_anetd_set_wiface(sid, ssid, wpakey):
	data = [ "wifid", "set_wiface", {"name" :"private", "ssid": ssid , "encryption":"wpa2", "key": wpakey, "mode": "bgn"} ]
	# print data
	# print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))

def test_anetd_set_ethrouted(sid):
	data = [ "anet", "ethrouted", {"proto":"dhcp"}]
	# print data
	# print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))

def test_anetd_set_wiclirouted(sid, masterssid, masterwpakey):
	data = [ "anet", "wiclirouted", {"proto":"dhcp", "ssid": "Gramofon_3e84b4", "key":masterwpakey, "encryption":"psk2"} ]
	#	"params":["anet","wclirouted",{"proto":"dhcp","ssid":"Gramofon_3e8e24","encryption":"psk2","key":"12345678","freq":"2412","mtu":1500}]}:
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))

def test_anetd_set_wicliclone(sid, masterssid, masterwpakey):
	data = [ "anet", "wiclone", {"ssid" :masterssid, "encryption":"psk2", "key":masterwpakey}]
	# print data
	# print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))

def test_anetd_status(sid):
	data = [ "anet", "status", {} ];
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))
	# Response: [{u'jsonrpc': u'2.0', u'id': 1, u'result':
	#	[0, {u'status': {u'code': 3, u'desc': u'wrongstatus'},
	#		u'netconf_status': {u'code': 0, u'desc': u'ok'},
	#		u'mode': {u'code': 0, u'desc': u'ethrouted'},
	#		u'reqmode': {u'code': 0, u'desc': u'ethrouted'}}]}]

def test_anetd_ssidscan(sid):
	data = [ "anet", "ssid_scan", {"iface":"radio"} ]
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))
	# Response: [{u'jsonrpc': u'2.0', u'id': 1, u'result': [0]}

def test_anetd_get_ssids(sid):
	data = [ "anet", "get_ssids", {} ]
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))
	# [{u'jsonrpc': u'2.0', u'id': 1, u'result':
	# [0, {u'results': [
	# 				{u'ssid': u'BTHub3-56F7', u'bssid': u'00:FE:F4:0E:95:D8', u'encryption': {u'authentication': [u'psk'], u'ciphers': [u'tkip', u'ccmp'], u'enabled': True, u'wpa': [1, 2]}, u'signal': -53, u'quality_max': 70, u'mode': u'Master', u'quality': 57, u'channel': 2},
	# 				{u'ssid': u'Fon WiFi', u'bssid': u'C6:71:30:34:C7:DD', u'encryption': {u'enabled': False}, u'signal': -55, u'quality_max': 70, u'mode': u'Master', u'quality': 55, u'channel': 1},
	# 				{u'ssid': u'MyPlace_0B30A0', u'bssid': u'18:AA:45:0B:30:B0', u'encryption': {u'authentication': [u'psk'], u'ciphers': [u'ccmp'], u'enabled': True, u'wpa': [2]}, u'signal': -53, u'quality_max': 70, u'mode': u'Master', u'quality': 57, u'channel': 11}]}]}]

def test_anetd_get_gramoname(sid):
	data = [ "anet", "get_gramofonname", {} ]
	print data
	print '\t Response' + str(my_httprpc.run_httprpc_call(data, sid))
	# Response: [{u'jsonrpc': u'2.0', u'id': 1, u'result': [0, {u'spotifyname': u'Gramofon_3e84b4', u'mdnsname': u'Gramofon MPD server'}]}]

def test_anetd_get_fonmac(sid):
	data = [ "mfgd", "get_fonmac", {} ]
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))
	# Response: [{u'jsonrpc': u'2.0', u'id': 1, u'result': [0, {u'fonmac': u'c4-71-30-3e-84-b4'}]}]

def test_anetd_get_hotspotdmac(sid):
	data = [ "hotspotd", "get", {"section":"main", "options":["nasid"]}]
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))
	# Response: [{u'jsonrpc': u'2.0', u'id': 1, u'result': [0, {u'main': {u'nasid': u'c4-71-30-3e-84-b4'}}]}]

def test_anetd_get_wifaceprivate(sid):
	data = [ "wifid", "get_wiface", {"name":"private", "option":["key", "ssid"]} ]
	print data
	print '\t Response: ' + str(my_httprpc.run_httprpc_call(data, sid))
	# Response: [{u'jsonrpc': u'2.0', u'id': 1, u'result': [0, {u'key': u'cqscsrgbtd'}]}]


# get login sid
my_httprpc = HTTPRPCCore("192.168.10.1")
sid = get_login_sid(my_httprpc)

# get API
test_anetd_status(sid)
time.sleep(1)
test_anetd_ssidscan(sid)
time.sleep(5)
test_anetd_get_ssids(sid)
time.sleep(1)
test_anetd_get_gramoname(sid)
time.sleep(1)
test_anetd_get_fonmac(sid)
time.sleep(1)
test_anetd_get_hotspotdmac(sid)
time.sleep(1)
test_anetd_get_wifaceprivate(sid)
time.sleep(1)

'''
# set API
test_anetd_setgramofonname(sid, test_gramoname)
test_anetd_get_gramoname(sid)
time.sleep(1)
test_anetd_set_wiface(sid, test_private_ssid, test_private_wpakey)
test_anetd_get_wifaceprivate(sid)
time.sleep(1)
test_anetd_set_ethrouted(sid)
test_anetd_status(sid)
time.sleep(1)
test_anetd_set_wiclirouted(sid, test_master_ap_ssid, test_master_ap_wpakey)
test_anetd_status(sid)
time.sleep(1)
test_anetd_set_wicliclone(sid, test_master_ap_ssid, test_master_ap_wpakey)
test_anetd_status(sid)
'''
