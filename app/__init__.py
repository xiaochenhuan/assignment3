from flask import Flask, render_template
from app.db_models import db, migrate, login
from app.routes import api_bp

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('../instance/config.py')
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
app.register_blueprint(api_bp, url_prefix='/')
app.config['UPLOAD_FOLDER'] = 'static/img/products'    # need Chang's review here

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from app import routes