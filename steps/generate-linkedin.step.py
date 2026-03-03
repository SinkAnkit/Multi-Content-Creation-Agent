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
    'name': 'LinkedinGenerate',
    'description': 'Generates LinkedIn content using Ollama Deepseek-R1',
    'subscribes': ['generate-content'],
    'emits': ['linkedin-schedule'],
    'input': GenerateInput.model_json_schema(),
    'flows': ['content-generation']
}

async def handler(input, context):
    try:
        with open("prompts/linkedin-prompt.txt", "r", encoding='utf-8') as f:
            linkedinPromptTemplate = f.read()
        
        linkedinPrompt = linkedinPromptTemplate.replace('{{title}}', input['title']).replace('{{content}}', input['content'])

        context.logger.info("🔄 LinkedIn content generation started using Ollama (Deepseek-R1)...")

        # Use Ollama instead of OpenAI for local LLM inference
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{'role': 'user', 'content': linkedinPrompt}],
            format='json',
            options={
                'temperature': 0.7,
                'num_predict': 2000
            }
        )

        try:
            linkedin_content = json.loads(response['message']['content'])
        except Exception:
            linkedin_content = {'post': response['message']['content'], 'characterCount': len(response['message']['content'])}

        context.logger.info(f"🎉 LinkedIn content generated successfully!")

        await context.emit({
            'topic': 'linkedin-schedule',
            'data': {
                'requestId': input['requestId'],
                'url': input['url'],
                'title': input['title'],
                'content': linkedin_content,
                'generatedAt': datetime.now().isoformat(),
                'originalUrl': input['url']
            }
        })
    except Exception as e:
        context.logger.error(f"❌ LinkedIn content generation failed: {e}")
        raise e
