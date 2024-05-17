import pymongo
from typing import List, Dict, Union


class CardManager:
    def __init__(self):
        # server db URL: "mongodb://mongodb:27017"
        # test db URL: "mongodb://localhost:27017"
        url = "mongodb://localhost:27017"
        self.client = pymongo.MongoClient(url)
        self.db = self.client.AutoLibrary
        self.cards = self.db.cards

    def add_book_info(self, tg_id: str, subject: str, name: str, author: str):
        card = self.cards.find_one({"tg_id": tg_id})

        if not card:
            card = {
                "tg_id": tg_id,
                "books": {subject: [{"name": name, "author": author}]}
            }
            self.cards.insert_one(card)
        else:
            if subject in card["books"]:
                card["books"][subject].append({"name": name, "author": author})
            else:
                card["books"][subject] = [{"name": name, "author": author}]
            self.cards.update_one({"tg_id": tg_id}, {"$set": {"books": card["books"]}})

    def get_books_by_tg_id(self, tg_id: str) -> Union[Dict[str, List[Dict[str, str]]], None]:
        card = self.cards.find_one({"tg_id": tg_id})
        if not card:
            card = {
                "tg_id": tg_id,
                "books": {}
            }
            self.cards.insert_one(card)
        card = self.cards.find_one({"tg_id": tg_id})
        if card:
            return card["books"]
        return None


if __name__ == "__main__":
    manager = CardManager()
    manager.add_book_info("123456", "Fiction", "Book Title", "Author Name")
    books = manager.get_books_by_tg_id("123456")
    print(books)
