import anthropic
from dotenv import load_dotenv


class Client:

    def __init__(self, tools):
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.tools = tools

    def send_user_query(self, user_query):
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            tools=self.tools,
            messages=[
                {
                    "role": "user",
                    "content": user_query,
                }
            ],
        )
        print(message.content)
