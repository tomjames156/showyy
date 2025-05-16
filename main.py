from backend import create_app, create_database
from flask_restful import Api

app = create_app()
api = Api(app)

if __name__ == "__main__":
    create_database(app)
    app.run(host='0.0.0.0', port=5000, debug=True)