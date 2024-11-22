import os, json
import requests as r
from dotenv import load_dotenv

load_dotenv()

APP_PORT = os.getenv("SERVER_PORT", "")
APP_IP = os.getenv("SERVER_IP", "")
URL_PATH = "api/books"
BASE_URL = f"http://{APP_IP}:{APP_PORT}/{URL_PATH}"


class TestBookAPI:
    """
    Testing Book API
    """
    temp_book_id = ""

    def test_create_book(self):
        """
        Test creating a new book record
        """
        param_data = {
            "title": "Test Radon Book", "author": "Random Author",
            "isbn": "1230-458-3B90", "publish_date": "2023-11-19"
        }
        response = r.post(BASE_URL, json=param_data, timeout=100)
        data = json.loads(response.content.decode("utf-8"))
        self.temp_book_id = data['info']['id']
        print(data['info'])
        assert response.status_code == 201
        # assert param_data in data['info']

    def test_get_all_books(self):
        """
        Test retrieving all books from the API
        """
        response = r.get(BASE_URL + "/", timeout=100)
        assert response.status_code == 200

    def test_get_book_by_id_success(self):
        """
        Test retrieving a book by ID (success case)
        """
        test_book_id = self.temp_book_id
        response = r.get(f"{BASE_URL}/{test_book_id}", timeout=100)
        assert response.status_code == 200

    def test_get_book_by_id_not_found(self):
        """
        Test retrieving a book by ID (not found)
        """
        test_book_id = "9999"
        response = r.get(f"{BASE_URL}/{test_book_id}", timeout=100)
        assert response.status_code >= 400  # Expected not found

    def test_update_book(self):
        """
        Test updating a book record
        """
        data = {
            "title": "Updated Title", "isbn": "329K-098-2024",
            "publish_date": "2001-11-20", "author": "Desmond Tutu"
        }
        test_book_id = self.temp_book_id
        response = r.patch(url=f"{BASE_URL}/{test_book_id}", json=data, timeout=100)
        print(response.content)
        print(response.status_code)
        assert response.status_code == 200

    def test_create_book_with_invalid_data(self):
        """
        Test creating a new book record with invalid data
        """
        invalid_data = {"title": "", "isbn": "282", "author": "Silly"}
        response = r.post(BASE_URL, json=invalid_data, timeout=100)
        assert response.status_code >= 400
