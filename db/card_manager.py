import pymongo
from typing import List, Dict, Union
import os


class CardManager:
    def __init__(self):
        url = os.getenv("MONGO_URL" , "mongodb://localhost:27017")
        self.client = pymongo.MongoClient(url)
        self.db = self.client["AutoLibrary"]
        self.cards = self.db["cards"]

    def get_or_create_card(self, tg_id: str) -> Dict:
        card = self.cards.find_one({"tg_id": tg_id})
        if not card:
            card = {"tg_id": tg_id, "books": {}, "subject": ""}
            self.cards.insert_one(card)
            card = self.cards.find_one({"tg_id": tg_id})
        return card

    def add_book_info(self, tg_id: str, subject: str, name: str, author: str):
        card = self.get_or_create_card(tg_id)
        if subject in card["books"]:
            card["books"][subject].append({"name": name, "author": author})
        else:
            card["books"][subject] = [{"name": name, "author": author}]
        self.cards.update_one({"tg_id": tg_id}, {"$set": {"books": card["books"]}})

    def get_books_by_tg_id(self, tg_id: str) -> Union[Dict[str, List[Dict[str, str]]], None]:
        card = self.get_or_create_card(tg_id)
        return card.get("books")

    def set_subject(self, tg_id: str, subject: str):
        card = self.get_or_create_card(tg_id)
        self.cards.update_one({"tg_id": tg_id}, {"$set": {"subject": subject}})

    def get_subject_by_tg_id(self, tg_id: str) -> Union[str, None]:
        card = self.get_or_create_card(tg_id)
        return card.get("subject")


if __name__ == "__main__":
    manager = CardManager()
    manager.add_book_info("123456", "Fiction", "Book Title", "Author Name")
    books = manager.get_books_by_tg_id("123456")
    print(books)
