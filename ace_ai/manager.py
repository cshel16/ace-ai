
import logging
from .client import Client

logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, client: Client):
        self.client = client
    
    def _prompt_user(self) -> str:
        return input("> ")

    def _get_model_response(self, prompt) -> str:
        return self.client.handle_prompt(prompt)

    def run(self) -> None:
        print("\n\nWelcome to Ace AI! Ask me anything...\n\n\n")
        while True:
            prompt = self._prompt_user()
            response = self._get_model_response(prompt)
            if not response:
                logger.exception("Did not receive valid response from client")
            print(f"\n{response}\n")