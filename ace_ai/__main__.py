import logging
from .tools import Tools
from .client import Client
from .manager import Manager

logging.basicConfig(level=logging.INFO)
logging.disable(logging.CRITICAL)
logger = logging.getLogger(__name__)

def main() -> None:
    tools = Tools()
    client = Client(tools)
    manager = Manager(client)
    manager.run()

if __name__ == "__main__":
    main()