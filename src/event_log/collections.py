from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv('DJANGO_HOST'))
db = client['django_db']


evento = db['evento']
categorias = db['categorias']