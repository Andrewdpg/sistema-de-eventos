from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
client = MongoClient(os.getenv('DJANGO_HOST'))
db = client['django_db']

evento = db['evento']
categorias = db['categorias']

universitydb = psycopg2.connect(
    dbname=os.getenv('UNIVERSITY_DB'),
    user=os.getenv('UNIVERSITY_USER'),
    password=os.getenv('UNIVERSITY_PASSWORD'),
    host=os.getenv('UNIVERSITY_HOST')
)
