import os

from dotenv import load_dotenv

def load_env():
  load_dotenv(verbose=True)

def get_env(name:str):
  return os.environ[name]
