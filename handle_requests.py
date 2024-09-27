import json
import requests

class RequestHandler:

	development = False
	url_link = "https://test888.netlify.app"
	dev_link = "http://localhost:8888"


	@staticmethod
	def get_link():
		if RequestHandler.development:
			return RequestHandler.dev_link
		return RequestHandler.url_link



	@staticmethod
	def create_request(link, data={}):
		try:
			response = requests.post(
				f'{RequestHandler.get_link()}/.netlify/functions/api/{link}',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()
			result = response.json()
			return True, result
		except requests.RequestException as e:
			return False, e
