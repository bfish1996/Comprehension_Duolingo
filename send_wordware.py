import json
import requests
import os
import get_body

my_secret = os.environ['WORDWARE_KEY']
consumer_key = "YOUR_CONSUMER_KEY"
access_token = os.environ['POCKET_CONSUMER_TOKEN']

def retrieve_pocket_data(consumer_key, access_token, count=10, detail_type="complete"):
      url = "https://getpocket.com/v3/get"
      headers = {"Content-Type": "application/json"}
      payload = {
          "consumer_key": consumer_key,
          "access_token": access_token,
          "count": count,
          "detailType": detail_type
      }

      response = requests.post(url, headers=headers, data=json.dumps(payload))

      if response.status_code == 200:
          return response.json()
      else:
          return {"error": "Failed to retrieve data", "status_code": response.status_code}

pocket_data = retrieve_pocket_data(consumer_key, access_token)
print(json.dumps(pocket_data, indent=4))

def main():
    prompt_id = "4db40616-771d-41cd-861c-8b5fca200420"
    api_key = os.environ['WORDWARE_KEY']

    url = 'https://paulgraham.com/nft.html'
    body = store_url_body(url)
    print(body)

    # Describe the prompt (shows just the inputs for now)
    r1 = requests.get(f"https://app.wordware.ai/api/prompt/{prompt_id}/describe",
                      headers={"Authorization": f"Bearer {api_key}"})
    print(json.dumps(r1.json(), indent=4))

    # Execute the prompt
    r = requests.post(f"https://app.wordware.ai/api/prompt/{prompt_id}/run",
    json={
        "inputs": {
            "content": body
        }
    },
    headers={"Authorization": f"Bearer {api_key}"},
    stream=True
   )


    # Ensure the request was successful
    if r.status_code != 200:
        print("Request failed with status code", r.status_code)
        print(json.dumps(r.json(), indent=4))
    else:
        for line in r.iter_lines():
            if line:
                content = json.loads(line.decode('utf-8'))
                value = content['value']
                # We can print values as they're generated
                if value['type'] == 'generation':
                    if value['state'] == "start":
                        print("\nNEW GENERATION -", value['label'])
                    else:
                        print("\nEND GENERATION -", value['label'])
                elif value['type'] == "chunk":
                    print(value['value'], end="")
                elif value['type'] == "outputs":
                    # Or we can read from the outputs at the end
                    # Currently we include everything by ID and by label - this will likely change in future in a breaking
                    # change but with ample warning
                    print("\nFINAL OUTPUTS:")
                    print(json.dumps(value, indent=4))

if __name__ == '__main__':
    main()