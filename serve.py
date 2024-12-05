from flask import jsonify as jr
from app.settings import app
from app.misc.messages import SERVICE_INFO
from app.routes.book_routes import book_routes
from app.routes.user_routes import auth_routes


@app.route("/", methods=["GET"])
def index():
    """
    This is the default home page
    """
    return jr({"info": SERVICE_INFO}), 200


# add routes to the app
app.register_blueprint(auth_routes)
app.register_blueprint(book_routes)

# if __name__ == "__main__":
#     app.run(host=app.config["SERVER_IP"], port=app.config["SERVER_PORT"])
