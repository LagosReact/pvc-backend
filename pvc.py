import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PVC_DB')

app.config['SECRET_KEY'] = os.environ.get('PVC_SECRET')
