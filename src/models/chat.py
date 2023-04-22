from typing import List, Any
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import openai

openAIApiKey = os.environ['OPENAI_API_KEY']

params = {
    'verbose': True,
    'temperature': 1,
    'openAIApiKey': openAIApiKey,
    'modelName': os.environ['OPENAI_MODEL'] if 'OPENAI_MODEL' in os.environ else "gpt-3.5-turbo",
    'maxConcurrency': 1,
    'maxTokens': 1000,
    'maxRetries': 5,
}

class Model:
    def __init__(self):
        self.tools = []
        self.chain = ConversationChain
        self.openai = openai
        self.openai.apikey = openAIApiKey
        
        model = ChatOpenAI(params, configuration)

        chatPrompt = ChatPromptTemplate.fromPromptMessages([
            SystemMessagePromptTemplate.fromTemplate(
                "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."
            ),
            MessagesPlaceholder("history"),
            HumanMessagePromptTemplate.fromTemplate("{input}"),
        ])

        self.chain = ConversationChain({
            memory: ConversationBufferMemory(),
            prompt: chatPrompt,
            llm: model,
        })

    def call(self, input):
        output = self.chain.call({ input })
        return output.output

