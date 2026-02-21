import anthropic
import logging
from dotenv import load_dotenv
from .tools import Tools


logger = logging.getLogger(__name__)


class Client:

    def __init__(self, tools: Tools):
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.tools = tools

    def send_message(self, content):
        return self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            tools=self.tools.tools,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        )

    def send_user_query(self, user_query):
        message = self.send_message(user_query)
        logging.debug(message)
        return self.process_response(message)

    def process_response(self, message):
        response = None
        for block in message.content:
            if block.type == "text":
                print(block.text)
            if block.type == "tool_use":
                if block.name == "get_player_id":
                    logging.debug(block)
                    response = self.call_get_player_id(block.input)
        return response

    def call_get_player_id(self, input):
        response = self.tools.get_player_id(input["last_name"], input["first_name"])
        return response