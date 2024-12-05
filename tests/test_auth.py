# class TestAuthPI:

#     # Test LoginManager.require_api_key decorator

#     def test_require_api_key_no_api_key(self, client):
#         """
#         Tests that the require_api_key decorator returns a 401 response 
#         when no X-API-Key header is provided.
#         """
#         response = client.get("/api/books")
#         assert response.status_code == 401
#         assert "User API Key must be provided" in response.json["error"]

#     # Mocking successful token validation (implement actual logic)
#     def mock_compare(self, api_key, cache_id):
#         return True

#     LoginManager.toke.compare = mock_compare

#     def test_require_api_key_invalid_token(self, client):
#         """
#         Tests that the require_api_key decorator returns a 401 response 
#         when an invalid X-API-Key header is provided.
#         """
#         client.headers = {"X-API-Key": "invalid_token"}
#         response = client.get("/api/books")
#         assert response.status_code == 401
#         assert "Invalid token was specified" in response.json["error"]

#     # Test PasswordManager.generate_password_hash function

#     def test_generate_password_hash(self):
#         """
#         Tests that the generate_password_hash function produces a valid SHA512 hash 
#         from a plain text password.
#         """
#         password = "test_password"
#         hashed_password = pm.generate_password_hash(password)
#         assert len(hashed_password) == 128  # SHA512 hash length
#         assert hashed_password is not None

#     # Test PasswordManager.check_password function

#     def test_check_password_correct(self):
#         """
#         Tests that the check_password function returns True when comparing a plain text 
#         password with its corresponding hash.
#         """
#         password = "test_password"
#         hashed_password = pm.generate_password_hash(password)
#         assert pm.check_password(hashed_password, password) is True

#     def test_check_password_incorrect(self):
#         """
#         Tests that the check_password function returns False when comparing a plain text 
#         password with an incorrect hash.
#         """
#         password = "test_password"
#         hashed_password = pm.generate_password_hash(password)
#         incorrect_password = "wrong_password"
#         assert pm.check_password(hashed_password, incorrect_password) is False

#     # Test User Authentication Routes

#     def test_create_user(self, client):
#         """
#         Tests creating a new user with valid data and ensures a successful response 
#         with a token.
#         """
#         data = {"email": "[email address removed]", "fullname": "Test User", "password": "test_password123"}
#         response = client.post("/api/auth", json=data)
#         assert response.status_code == 201
#         assert "CREATED_USER_OK" in response.json
#         assert "TOKEN" in response.json

#     def test_get_access(self, client):
#         """
#         Tests authenticating a user with valid credentials and ensures a successful 
#         response with a token. (Assuming a user already exists)
#         """
#         # Assuming a user is already created with email "[email address removed]" and password "test_password123"
#         data = {"userid": "email", "pwd": "test_password123"}
#         response = client.post("/api/auth/in", json=data)
#         assert response.status_code == 200
#         assert TOKEN in response.json  # Assuming the response key for the token is 'TOKEN'
