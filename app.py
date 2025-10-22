from flask import Flask
from flask_mail import Mail
from config.config import Config

mail = Mail()  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)  

    # Blueprints
    from blueprints.usuario_bp import user_bp
    from blueprints.main_bp import main_bp
    from blueprints.filme_bp import filme_bp
    from blueprints.comentario_bp import comentario_bp
    from blueprints.canais_bp import canais_bp

    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(filme_bp, url_prefix="/filme")
    app.register_blueprint(comentario_bp, url_prefix="/comentario")
    app.register_blueprint(canais_bp, url_prefix="/canais")

    return app

app = create_app()
