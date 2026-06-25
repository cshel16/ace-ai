from .client import Client

class Manager:
    def __init__(self, client: Client):
        self.client = client
    
    def _prompt_user(self) -> str:
        return input("> ")

    def _send_to_client(self, user_input) -> str:
        return self.client.send_user_query(user_input)

    def run(self) -> None:
        print("Welcome to Ace AI! Ask me anything...")
        while True:
            user_input = self._prompt_user()
            model_response = self._send_to_client(user_input)
