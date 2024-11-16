
import os
import argparse
import boto3
import json
import openai
from dotenv import load_dotenv
load_dotenv()
load_dotenv(os.path.expanduser('~/.credentials/.env'))
from loguru import logger
from rich.console import Console
console = Console()
print(os.getenv('OPENAI_API_KEY'))
print(os.getenv('OPENAI_BASE_URL'))
def _bedrock_anthropic(prompt:dict, model:str):
    bedrock = boto3.client(service_name="bedrock-runtime")
    completion = bedrock.invoke_model(body=prompt, modelId=model)
    return completion

def _openapi(prompt:dict, model:str):
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.base_url = os.getenv('OPENAI_BASE_URL', 'https://openai.com/v1')
    print("++", openai.base_url)
    print("##", openai.api_key)
    print("--->", prompt)
    # completion = openai.chat.completions.create(model=model, **prompt)
    completion = openai.chat.completions.create(model=model, messages=prompt['messages'])
    return completion.model_dump_json(indent=2)

def chat(api:str, model:str , prompt:str, completion:str =None, provider:str = None):
    prompt_path = prompt
    if not os.path.exists(prompt_path):
        logger.error(f"Prompt file {prompt_path} not exists")
    with open(prompt_path, 'rt', encoding='utf-8') as f:
        prompt = json.load(f)

    completion_path = completion
    if completion is None:
        filename = os.path.basename(prompt_path)
        prompt_dir = os.path.dirname(prompt_path)
        basename, ext = os.path.splitext(filename)
        if basename.endswith('-prompt'):
            basename = basename[:-len('-prompt')]
        completion_path = f'{prompt_dir}/{basename}-completion.json'
    

    completion = False
    if api == 'openai':
        if provider is None:
            completion = _openapi(prompt,model)
    elif api == 'anthropic':
        if provider == 'aws':
            completion = _bedrock_anthropic(prompt,model)
    if not completion:
        logger.error("Failed!")
    print("completion:", completion)

    with open(completion_path, 'wt', encoding='utf-8') as f:
        f.write(completion)

    console.print(f"Successfuly completion writed to {completion_path}.", style="bold green")



def main():
    parser = argparse.ArgumentParser(description='LLM Chat tool.')
    parser.add_argument('--prompt', '-p', type=str, required=True, 
                        help='Prompt JSON profile')
    parser.add_argument('--api', '-a', type=str, required=True,
                         choices=['openai', 'anthropic', 'gemini'],  
                         help='API of the model type')
    parser.add_argument('--provider', type=str, default=None, 
                        choices=['aws', 'azure', 'gcp'], 
                        help='Provider type')
    parser.add_argument('--completion', '-c', type=str, default=None, 
                        help='The file to save response content')
    parser.add_argument('--model', '-m', type=str, default=None, 
                        help='Model name')

    args = parser.parse_args()
    chat(args.api, args.model, args.prompt,args.completion, args.provider)


if __name__ == '__main__':
    main()

