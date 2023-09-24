from flask import Flask
from sqlalchemy.sql import text
from os import getenv
from flask import redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes