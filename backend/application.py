from app import create_app
from flask_cors import CORS

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
