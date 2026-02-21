import logging
from .tools import Tools
from .client import Client

logging.basicConfig(level=logging.INFO)
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)

def main() -> None:
    tools = Tools()
    client = Client(tools)
    print("Welcome to Ace AI!")
    user_query = input("Ask me a question: ")
    client.send_user_query(user_query)

if __name__ == "__main__":
    main()