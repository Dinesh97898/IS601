import functools
import secrets
import string

from flask import Flask, flash, redirect, url_for
from flask_apscheduler import scheduler, APScheduler
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_moment import Moment
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

moment = Moment()
scheduler = APScheduler()
security = Security()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def admin_only(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if current_user and current_user.is_authenticated and current_user.is_admin():
            return f(*args, **kwargs)
        else:
            flash("Admin only")
            return redirect(url_for('core.index'))
    return wrap


def create_app():
    print('created app')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'this_is_mine'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SCHEDULER_API_ENABLED '] = True
    #app.config['SECURITY_REGISTERABLE'] = False
    app.config['SECURITY_LOGIN_URL'] = '/auth/login'
    register_extensions(app)
    register_blueprints(app)
    setup_database(app)

    return app


def register_extensions(app):
    print("registering extensions")
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    @app.context_processor
    def inject_user():
        return dict(user=current_user)



def register_blueprints(app):
    # blueprint for auth routes in our app
    from land.models import Land
    from auth.models import Permission, User
    from core.models import Purchase, PurchaseType
    from workers.models import Worker
    from resources.models import ResourceNode, InventoryToResource, Inventory, Resource
    from smelt.models import Smelter
    from auth.models import Permission, User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    from auth.auth import auth_bp
    from core.core import core_bp
    from land.land import land_bp
    from resources.resources import resources_bp
    from workers.workers import workers_bp
    from smelt.smelt import smelters_bp
    from shop.shop import shop_bp
    app.register_blueprint(auth_bp)
    # blueprint for non-auth parts of app
    app.register_blueprint(core_bp)
    app.register_blueprint(land_bp, url_prefix='/land')
    app.register_blueprint(resources_bp, url_prefix='/resource')
    app.register_blueprint(workers_bp, url_prefix='/workers')
    app.register_blueprint(smelters_bp, url_prefix='/smelt')
    app.register_blueprint(shop_bp, url_prefix='/shop')


"""@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def test_periodic_freebieness():
    with scheduler.app.app_context():
        print ("Printing some money")
        _admins = ('matt@test.com',)
        from auth.models import Permission, User
        users = User.query.filter(User.email.in_(_admins)).all()
        for user in users:
            print('updating user')
            user.permission = Permission.ADMIN
            # user.inventory.reset_resources()
            user.inventory.update_coins(100)"""


def setup_database(app):
    with app.app_context():
        from land.models import Land
        from auth.models import Permission, User, Role
        from core.models import Purchase, PurchaseType
        from workers.models import Worker
        from resources.models import ResourceNode, InventoryToResource, Inventory, Resource
        db.create_all()
        security.init_app(app=app, datastore=SQLAlchemyUserDatastore(db, User, Role), register_blueprint=True)
        _admins = ('matt@test.com',)
        print("init db, setting up users/admins")

        user = User.query.filter_by(name="System").first()
        if user is None:
            print('Creating system user')
            res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                          for i in range(20))
            user = User(email="minelysystem@ethereallab.app", name="System",
                        password=generate_password_hash(
                            res
                            , method='sha256'),
                        permission=Permission.NONE)
            db.session.add(user)
            db.session.commit()

            print('Created system user')
        else:
            print('System user already exists ' + str(user.id))
        users = User.query.filter(User.email.in_(_admins)).all()
        for user in users:
            print('updating user')
            user.permission = Permission.ADMIN

            role = security.datastore.find_or_create_role(name="Admin", description="The one and only")
            security.datastore.add_role_to_user(user, role)
            security.datastore.activate_user(user)
            # user.inventory.reset_resources()
            if user.get_coins() < 10000:
                user.inventory.update_coins(10000)

                print('updating coins')
            # user.active = True
        db.session.commit()


if __name__ == "__main__":
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    print("Running")
    app = create_app()
    setup_database(app)

    #app.run(debug=True)y
