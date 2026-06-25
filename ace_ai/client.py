import anthropic
import logging
import json
import sys
from dotenv import load_dotenv
from .tools import Tools

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, tools: Tools):
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.tools = tools
        self.conversation = []


    def _add_message(self, role, content) -> None:
        message = {
            "role": role,
            "content": content,
        }
        self.conversation.append(message)


    def _send_to_model(self) -> Message | None:
        response = None
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                tools=self.tools.tools,
                messages=self.conversation
            )
        except Exception:
            logger.exception("Encountered exception when talking to Claude")
            sys.exit()
        return response
    

    def _process_response(self, response) -> str | None:
        content = response["content"]
        if content["type"] == "text":
            return content["text"]
        else:
            return None


    def handle_prompt(self, prompt) -> str | None:
        # called by manager
        # takes the prompt from the user, add to convo, send to model
        # get model response, parse text, send to back to manager
        self._add_message("user", prompt)
        response = self._send_to_model()
        model_prompt = self._process_response(response)
        return model_prompt

