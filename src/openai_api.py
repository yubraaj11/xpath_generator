import base64
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class GPTVision:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.MODEL = 'gpt-4o-mini'
        self.OPENAI_API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

    def generate_test_cases(self, image_path):
        base64_image = encode_image(image_path=image_path)
        if base64_image is None:
            return "Error processing image"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model" : self.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                                Scan the given input image and from the given input image generate all possible test 
                                cases in gherkin language. While returning, stick to the test cases only.  
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64, {base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        try:
            response = requests.post(self.OPENAI_API_ENDPOINT, headers=headers, json=payload)

            # Check the response status code
            if response.status_code != 200:
                return f"API request failed with status code {response.status_code}: {response.text}"

            # Print the raw response for debugging
            print("Raw response:", response.text)

            # Attempt to parse the JSON response
            try:
                openai_response = response.json()
                # Extract the 'content' from the response
                content = openai_response['choices'][0]['message']['content']
                return content
            except json.JSONDecodeError:
                return "Error decoding JSON response. The response may not be in the expected format."

        except requests.exceptions.RequestException as e:
            return f"Error in API request: {str(e)}"


def main():
    image_path = "/home/yubraj/Documents/vertex-projects/omniglue/res/ss1.png"
    gpt_vision = GPTVision()
    response = gpt_vision.generate_test_cases(image_path=image_path)
    print(response)


if __name__=="__main__":
    main()
