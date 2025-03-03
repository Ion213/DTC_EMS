from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from datetime import timedelta


#create database object
db=SQLAlchemy()
DB_NAME ="database.db"

#create migration so that you can migrate youre models(using cmd)
migrate = Migrate()
#create flask app
def flask_app():
    app = Flask(__name__,static_folder='templates/static')
    app.config['SECRET_KEY']= 'ion21'
    db_path = os.path.join(app.root_path, 'database', DB_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    #inheret the database and mirgration to the main app(flask app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    #implement login manager(sessions)
    # LoginManager initialization
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/'
    from .models.database_models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
        
    # Import routes/blueprints
    from .authenticator.user_auth import user_auth
    app.register_blueprint(user_auth, url_prefix='/')
#---------------------------------------
    from .routes.admin_manage_event import admin_manage_event
    app.register_blueprint(admin_manage_event, url_prefix='/')
    
    from .routes.admin_manage_activities import admin_manage_activities
    app.register_blueprint(admin_manage_activities, url_prefix='/')

#---------------------------
    from .routes.admin_manage_schedule import admin_manage_schedule
    app.register_blueprint(admin_manage_schedule, url_prefix='/')

    from .routes.admin_manage_department import admin_manage_department
    app.register_blueprint(admin_manage_department, url_prefix='/')

    from .routes.admin_manage_student_account import admin_manage_student_account
    app.register_blueprint(admin_manage_student_account, url_prefix='/')

    from .routes.admin_manage_ssg_account import admin_manage_ssg_account
    app.register_blueprint(admin_manage_ssg_account, url_prefix='/')

    from .routes.admin_manage_attendance import admin_manage_attendance
    app.register_blueprint(admin_manage_attendance, url_prefix='/')




    #add routes here

    from .routes.admin_manage_payments import admin_manage_payments
    app.register_blueprint(admin_manage_payments, url_prefix='/')




    from .routes.user_view_profile import user_view_profile
    app.register_blueprint(user_view_profile, url_prefix='/')

    from .routes.user_view_attendance import user_view_attendance
    app.register_blueprint(user_view_attendance, url_prefix='/')


    from .routes.user_view_events import user_view_events
    app.register_blueprint(user_view_events, url_prefix='/')

    

#-----------------------------------------------  
    from .routes.public_views import public_views
    app.register_blueprint(public_views, url_prefix='/')


    
    #craeate database
    create_database(app)

    
    return app

# Create database function
def create_database(app):
    if not os.path.exists(os.path.join(app.root_path,'database', DB_NAME)):
        with app.app_context():
            db.create_all()