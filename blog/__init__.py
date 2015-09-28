from flask import Flask
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import settings
app = Flask(__name__)
app.config.from_object('blog.settings')
import views