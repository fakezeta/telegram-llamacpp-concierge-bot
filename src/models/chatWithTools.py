#import json
import os
#import time
#from datetime import datetime
#from typing import Dict

#import google.auth
#import google.oauth2.credentials
#import google_auth_oauthlib.flow
#import requests
#from google.oauth2.credentials import Credentials
#from googleapiclient.discovery import build

from langchain.agents import AgentType, load_tools, initialize_agent

from langchain.llms import OpenAI

#from langchain.chat_models import ChatOpenAI
#from langchain.memory import ConversationBufferWindowMemory
from tools.google import GoogleTool


openAIApiKey = os.environ['OPENAI_API_KEY']

params = {
  'verbose': True,
  'temperature': 1,
  'openAIApiKey': openAIApiKey,
  'modelName': os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
  'maxConcurrency': 1,
  'maxTokens': 1000,
  'maxRetries': 5,
}


class Model:
    def __init__(self):
        self.llm=OpenAI(params['modelName'])
        self.tools: load_tools([GoogleTool])

    def call(self, input: str):
        if not self.agent:
            self.executor = initialize_agent(
                self.tools,
                self.llm,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                verbose=True
            )
            self.agent.memory = ConversationBufferWindowMemory(k=2)

        response = self.agent.run(input)

        print("Model response: " + response)

        return response.output
