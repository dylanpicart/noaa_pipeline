from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from schema import schema
from utils.logging_setup import setup_logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Extract necessary variables
NOAA_TOKEN = os.getenv("NOAA_TOKEN")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Initialize logging
setup_logging()

# SQLAlchemy setup
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Flask app setup
app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/health')
def health():
    return jsonify(status='healthy'), 200

# Root endpoint
@app.route('/')
def home():
    return jsonify(message='NOAA GraphQL API is running!'), 200

# GraphQL view setup with context session injection
def graphql_view():
    view = GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        context={'session': SessionLocal(), 'noaa_token': NOAA_TOKEN}
    )
    return view

app.add_url_rule('/graphql', view_func=graphql_view())

# Application entrypoint
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)