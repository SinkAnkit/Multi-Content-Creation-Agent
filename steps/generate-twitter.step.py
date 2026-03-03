import os
import json
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from dotenv import load_dotenv
import ollama

load_dotenv()

OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'deepseek-r1')

class GenerateInput(BaseModel):
    requestId: str
    url: HttpUrl
    title: str
    content: str
    timestamp: int

config = {
    'type': 'event',
    'name': 'TwitterGenerate',
    'description': 'Generates Twitter content using Ollama Deepseek-R1',
    'subscribes': ['generate-content'],
    'emits': ['twitter-schedule'],
    'input': GenerateInput.model_json_schema(),
    'flows': ['content-generation']
}

async def handler(input, context):
    try:
        with open("prompts/twitter-prompt.txt", "r", encoding='utf-8') as f:
            twitterPromptTemplate = f.read()
        
        twitterPrompt = twitterPromptTemplate.replace('{{title}}', input['title']).replace('{{content}}', input['content'])

        context.logger.info("🔄 Twitter content generation started using Ollama (Deepseek-R1)...")

        # Use Ollama instead of OpenAI for local LLM inference
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{'role': 'user', 'content': twitterPrompt}],
            format='json',
            options={
                'temperature': 0.7,
                'num_predict': 2000
            }
        )

        try:
            twitter_content = json.loads(response['message']['content'])
        except Exception:
            twitter_content = {'thread': [{'tweetNumber': 1, 'content': response['message']['content']}], 'totalTweets': 1}

        context.logger.info(f"🎉 Twitter content generated successfully!")

        await context.emit({
            'topic': 'twitter-schedule',
            'data': {
                'requestId': input['requestId'],
                'url': input['url'],
                'title': input['title'],
                'content': twitter_content,
                'generatedAt': datetime.now().isoformat(),
                'originalUrl': input['url']
            }
        })
    except Exception as e:
        context.logger.error(f"❌ Twitter content generation failed: {e}")
        raise e
