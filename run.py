from app import app
from config import DEBUG

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=DEBUG
    )