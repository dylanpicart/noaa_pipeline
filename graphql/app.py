from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from schema import schema
from utils.logging_setup import setup_logging
from spark_utils.session import get_spark_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os
import traceback
import time

load_dotenv()

NOAA_TOKEN = os.getenv("NOAA_TOKEN")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

setup_logging()

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = None
SessionLocal = None
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = scoped_session(sessionmaker(bind=engine))
except Exception as e:
    print("Failed to initialize SQLAlchemy engine!")
    print(traceback.format_exc())

spark_session = None
max_retries = 10
for attempt in range(max_retries):
    try:
        print(f"Trying to initialize Spark session, attempt {attempt+1}")
        spark_session = get_spark_session(app_name="NOAA GraphQL Server")
        print("Spark session started successfully!")
        break
    except Exception as e:
        print("Failed to initialize Spark session!")
        print(traceback.format_exc())
        time.sleep(10)
if spark_session is None:
    print("Spark session unavailable after several attempts. Exiting.")
    exit(1)

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    details = {'status': 'healthy'}
    if spark_session is None:
        details['spark'] = 'unavailable'
    if SessionLocal is None:
        details['db'] = 'unavailable'
    code = 200 if spark_session and SessionLocal else 503
    return jsonify(details), code

@app.route('/')
def home():
    return jsonify(message='NOAA GraphQL API is running!'), 200

def graphql_view():
    view = GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        context={'session': SessionLocal(), 'noaa_token': NOAA_TOKEN, 'spark': spark_session}
    )
    return view

app.add_url_rule('/graphql', view_func=graphql_view())

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
