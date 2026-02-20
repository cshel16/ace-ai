import sys

from .tools import Tools
from .client import Client

def main() -> None:
    client = Client(Tools.tools)
    print("Welcome to Ace AI!")
    user_query = input("Ask me a question: ")
    client.send_user_query(user_query)

if __name__ == "__main__":
    main()