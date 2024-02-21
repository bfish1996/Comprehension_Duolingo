import requests

def store_url_body(url, array):
  response = requests.get(url)
  if response.status_code == 200:
      array.append(response.text)
  else:
      print(f"Failed to retrieve URL: {url}")

# Usage example:
url = 'https://paulgraham.com/greatwork.html'
body_array = []
store_url_body(url, body_array)

def get_body():
  print(body_array)