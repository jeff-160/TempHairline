import sys
sys.dont_write_bytecode = 1

from dotenv import load_dotenv
from bot import *


def main():
    load_dotenv()
    Spy.Run()

if __name__=="__main__":
    main()