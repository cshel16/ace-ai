import anthropic
import logging
import json
from dotenv import load_dotenv
from .tools import Tools


logger = logging.getLogger(__name__)


class Client:

    def __init__(self, tools: Tools):
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.tools = tools
        self.conversation = []

    def add_message(self, role, content):
        message = {
            "role": role,
            "content": content,
        }
        self.conversation.append(message)

    def send_message(self):
        return self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            tools=self.tools.tools,
            messages=self.conversation
        )

    def send_user_query(self, user_query):
        self.add_message("user", user_query)
        message = self.send_message()
        logger.debug(message)
        return self.process_response(message)
    
    def build_tool_result_block(self, block, response):
        return [
            {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(response)
            }
        ]

    def process_response(self, message):
        self.add_message("assistant", message.content)
        if message.stop_reason != "tool_use":
            return message.content[0].text
        for block in message.content:
            if block.type == "tool_use":
                logger.debug(block)
                response = self.tools.tool_handlers[block.name](**block.input)
                response_block = self.build_tool_result_block(block, response)
                break
        self.add_message("user", response_block)
        response = self.send_message()
        return self.process_response(response)
