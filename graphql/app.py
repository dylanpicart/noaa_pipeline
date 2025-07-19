from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from schema import schema
from utils.logging_setup import setup_logging
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

NOAA_TOKEN = os.getenv("NOAA_TOKEN")


# Initialize logging
setup_logging()

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify(status='healthy'), 200

@app.route('/')
def home():
    return jsonify(message='NOAA GraphQL API is running!'), 200

# GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
