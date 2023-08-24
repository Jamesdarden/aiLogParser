import requests
import os

api_key = os.getenv('API_KEY')
url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
prompt_message = """I want you to Identify the top 5 potential causes for the program's malfunction 
based on the provided logfile excerpt from a Windows Operating System. I want you to tell me what specifically is wrong with the component and suggest a solution. list them in order of importance to operation. 
Consider the following crucial elements, the program needs to function: active x, wmi, javascript, user internet connectivity, av3controller, ajax. but do not limit your findings to these. Also examine what would cause the operating system not to function properly provide the return output
in json format. with keys {Component,Reason, proposedSolution, numOfOccurences, whereInlog, excerpt} the numOfOccurences should be a number of how many times the item was found in the log and the whereInLog should be the index of the item in the log. excerpt should be one line of the log that made you highlight the item"""


def scan_query(logData):
    system_message = "System: You are a language model trained to analyze log data and identify failure reasons.\n"
    prompt = (
        f"{system_message}"
        f"Prompt: {prompt_message}"
        f"Log Data: {logData}"
    )
    response = requests.post(
        url,
        json={
            "prompt": prompt,
            "max_tokens": 300  # Specify the desired maximum number of tokens
        },
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )

    generated_text = response.json()["choices"][0]["text"]
    return generated_text
