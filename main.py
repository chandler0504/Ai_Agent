import os
import sys
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt",type=str,help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
        temperature=0,
        tools=available_functions,
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if response.usage is None:
            raise RuntimeError("Token usage None")

        else:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            messages.append(result_message)
            if len(result_message["content"])==0:
                raise Exception("content empty")
            if args.verbose==True:
                print(f"-> {result_message['content']}")

    else:
        print(message.content)
        break
else:
    print("max number of attempts with no result")
    sys.exit(1)


def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
