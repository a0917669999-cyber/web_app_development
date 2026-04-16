from flask import Flask
from app.routes.recipe import bp as recipe_bp
import os
import sqlite3

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'app', 'templates'),
                static_folder=os.path.join(base_dir, 'app', 'static'))
                
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret_key')
    
    app.register_blueprint(recipe_bp)

    return app

app = create_app()

def init_db():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'instance', 'database.db')
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully at:", db_path)

if __name__ == '__main__':
    app.run(debug=True)
