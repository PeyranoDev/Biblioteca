import logging
import bcrypt
from utils import Utils
from database import Database

logging.basicConfig(filename='biblioteca.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class Biblioteca:
    def __init__(self) -> None:
        self.db = Database()

    def new_book(self, libro):
        libro = Utils.sanitize_input(libro)
        result = self.db.insert_one_book({"title": libro, "status": "Available"})
        logging.info(f"Libro añadido: {libro}")
        return "Libro añadido a la biblioteca"

    def lend_book(self, libro):
        libro = Utils.sanitize_input(libro)
        result = self.db.update_one_book({"title": libro, "status": "Available"}, {"$set": {"status": "Lent"}})
        if result.modified_count > 0:
            logging.info(f"Libro prestado: {libro}")
            return "Libro prestado"
        else:
            return "El libro no está en la biblioteca o ya está prestado"

    def return_book(self, libro):
        libro = Utils.sanitize_input(libro)
        result = self.db.update_one_book({"title": libro, "status": "Lent"}, {"$set": {"status": "Available"}})
        if result.modified_count > 0:
            logging.info(f"Libro devuelto: {libro}")
            return "Libro devuelto"
        else:
            return "El libro no está prestado o no está en la biblioteca"

    def remove_book(self, libro):
        libro = Utils.sanitize_input(libro)
        result = self.db.delete_one_book({"title": libro})
        if result.deleted_count > 0:
            logging.info(f"Libro eliminado: {libro}")
            return "Libro eliminado de la biblioteca"
        else:
            return "El libro no está en la biblioteca"

    def list_books(self, status=None):
        if status:
            books = self.db.find_books({"status": status})
        else:
            books = self.db.find_books()
        return books
