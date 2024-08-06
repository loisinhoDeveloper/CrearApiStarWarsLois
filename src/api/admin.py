  
import os
from flask_admin import Admin
from api.models import db, Usuario, Favoritos, Planetas, Personajes, Vehiculos #importamos las tablas
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Añadimos las tablas para que se visualicen.
    admin.add_view(ModelView(Usuario, db.session))
    admin.add_view(ModelView(Favoritos, db.session))
    admin.add_view(ModelView(Vehiculos, db.session))
    admin.add_view(ModelView(Personajes, db.session))
    admin.add_view(ModelView(Planetas, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
    