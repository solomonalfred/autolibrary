import pymongo
from typing import List, Dict, Union
import os


class LibraryManager:
    def __init__(self):
        url = os.getenv("MONGO_URL" , "mongodb://localhost:27017")
        self.client = pymongo.MongoClient(url)
        self.db = self.client.AutoLibrary
        self.library = self.db.library
        self.subjects = self.db.subjects
        self.authors = self.db.authors

    def add_record(self, name: str, author: str, subject: str, source: str):
        record = {"name": name, "author": author, "subject": subject, "source": source}
        self.library.insert_one(record)

        if self.subjects.find_one({"name": subject}) is None:
            self.subjects.insert_one({"name": subject})

        if self.authors.find_one({"name": author, "subject": subject}) is None:
            self.authors.insert_one({"name": author, "subject": subject})

    def search_library(self, name: Union[str, None] = None, subject: Union[str, None] = None,
                       author: Union[str, None] = None) -> List[Dict]:
        query = {}
        if name:
            query["name"] = name
        if subject:
            query["subject"] = subject
        if author:
            query["author"] = author

        results = self.library.find(query)
        return list(results)

    def get_all_subjects(self) -> List[str]:
        subjects = self.subjects.find()
        subjects_list = [subject["name"] for subject in subjects]
        return subjects_list

    def get_authors_by_subject(self, subject: str) -> List[str]:
        authors = self.authors.find({"subject": subject})
        authors_list = [author["name"] for author in authors]
        return authors_list

    def get_all_authors(self) -> List[str]:
        authors = self.authors.find()
        authors_list = [author["name"] for author in authors]
        return authors_list
