import json
import urllib.request

def ret_delay():
	ret = '<h1>JR山陽神戸線 白陵関係路線遅延情報</h1> <table border="1"> <tr> <th>種別</th> <th>終点</th> <th>遅れ</th> <th>場所</th> </tr>'
	try:
		url = 'https://www.train-guide.westjr.co.jp/api/v3/kobesanyo.json'
		url_st = url.replace('.json','_st.json')
		res = urllib.request.urlopen(url)
		res_st = urllib.request.urlopen(url_st)
		data = json.loads(res.read().decode('utf-8'))
		data_st = json.loads(res_st.read().decode('utf-8'))

		dictst = {}

		for station in data_st['stations']:
			dictst[station['info']['code']] = station['info']['name']

		for item in data['trains']:
			if item['delayMinutes'] > 0:
				stn = item['pos'].split('_')
				try:
					position = dictst[stn[0]] + '辺り'
				except KeyError:
					position = "どこかよくわかんない"
				#print(item['displayType'], item['dest']['text'],'行き:',item['delayMinutes'],'分遅れ',position,'辺り')
				if(item["displayType"] == "普通" or item["displayType"] == "新快速"):
					if(item["dest"]["text"] == "西明石" or item["dest"]["text"] == "野洲" or item["dest"]["text"] == "米原" or item["dest"]["text"] == "網干" or item["dest"]["text"] == "姫路"):
						ret += "<tr> <td>" + item["displayType"] + "</td> <td>" + item["dest"]["text"] + "行き" + "</td> <td>" + str(item["delayMinutes"]) + "分遅れ" + "</td> <td>" + position + "</td> </tr>" + " <br>"

	except urllib.error.HTTPError as err:
		print('HTTPError: ', err)
	except json.JSONDecodeError as err:
		print('JSONDecodeError: ', err)

	ret += "</table>"
	return ret