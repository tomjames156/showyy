from backend import create_app, create_database
from flask_restful import Api
from flask_cors import CORS

app = create_app()
CORS(app, supports_credentials=True)
api = Api(app)

if __name__ == "__main__":
    create_database(app)
    app.run(debug=True)