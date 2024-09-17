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
	def login_request(username, password):
		data = {
			'username': username,
			'password': password
		}
		try:
			response = requests.post(
				f'{RequestHandler.get_link()}/.netlify/functions/api/login',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()
			result = response.json()
			return True, result
		except requests.RequestException as e:
			return False, e

	@staticmethod
	def register_request(username, email, password):
		data = {
			'username': username,
			'email'   : email,
			'password': password
		}
		try:
			response = requests.post(
				f'{RequestHandler.get_link()}/.netlify/functions/api/register',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()
			result = response.json()
			return True, result
		except requests.RequestException as e:
			return False, e
