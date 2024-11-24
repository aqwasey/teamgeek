from app.settings import app
from app.routes.book_routes import book_routes
from app.routes.auth_routes import auth_routes


# add routes to the app
app.register_blueprint(auth_routes)
app.register_blueprint(book_routes)

# if __name__ == "__main__":
#     app.run(host=app.config["SERVER_IP"], port=app.config["SERVER_PORT"])
