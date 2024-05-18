import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.library_manager import LibraryManager

class TestLibraryManager(unittest.TestCase):

    @patch('pymongo.MongoClient')
    def setUp(self, mock_mongo_client):
        
        self.mock_client = MagicMock()
        mock_mongo_client.return_value = self.mock_client
        self.mock_db = self.mock_client.AutoLibrary
        self.mock_library = self.mock_db.library
        self.mock_subjects = self.mock_db.subjects
        self.mock_authors = self.mock_db.authors

        
        self.library_manager = LibraryManager()

    def test_add_record(self):
        
        self.mock_subjects.find_one.return_value = None
        self.mock_authors.find_one.return_value = None

        
        self.library_manager.add_record("Test Book", "Test Author", "Test Subject", "Test Source")

        
        self.mock_library.insert_one.assert_called_once_with({
            "name": "Test Book",
            "author": "Test Author",
            "subject": "Test Subject",
            "source": "Test Source"
        })
        self.mock_subjects.insert_one.assert_called_once_with({"name": "Test Subject"})
        self.mock_authors.insert_one.assert_called_once_with({"name": "Test Author", "subject": "Test Subject"})

    def test_search_library(self):
        
        self.mock_library.find.return_value = [{"name": "Test Book"}]

        
        result = self.library_manager.search_library(name="Test Book")

        
        self.assertEqual(result, [{"name": "Test Book"}])
        self.mock_library.find.assert_called_once_with({"name": "Test Book"})

    def test_get_all_subjects(self):
        
        self.mock_subjects.find.return_value = [{"name": "Test Subject 1"}, {"name": "Test Subject 2"}]

        
        result = self.library_manager.get_all_subjects()

        
        self.assertEqual(result, ["Test Subject 1", "Test Subject 2"])
        self.mock_subjects.find.assert_called_once()

    def test_get_authors_by_subject(self):
       
        self.mock_authors.find.return_value = [{"name": "Test Author"}]

        
        result = self.library_manager.get_authors_by_subject("Test Subject")

        
        self.assertEqual(result, ["Test Author"])
        self.mock_authors.find.assert_called_once_with({"subject": "Test Subject"})

    def test_get_all_authors(self):
  
        self.mock_authors.find.return_value = [{"name": "Test Author 1"}, {"name": "Test Author 2"}]


        result = self.library_manager.get_all_authors()


        self.assertEqual(result, ["Test Author 1", "Test Author 2"])
        self.mock_authors.find.assert_called_once()

if __name__ == "__main__":
    unittest.main()
