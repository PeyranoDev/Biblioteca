import tkinter as tk
from tkinter import simpledialog, messagebox
import customtkinter as ctk
from biblioteca import Biblioteca
from database import Database

class LibraryApp(ctk.CTk):
    def __init__(self, library, db):
        super().__init__()

        self.library = library
        self.db = db
        self.title("Biblioteca")
        self.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.main_frame, text="Bienvenido a la biblioteca Gonzales", font=("Arial", 20))
        self.label.pack(pady=20)

        self.view_books_button = ctk.CTkButton(self.main_frame, text="Ver libros", command=self.show_books)
        self.view_books_button.pack(pady=10)

        self.admin_button = ctk.CTkButton(self.main_frame, text="Admin", command=self.admin_login)
        self.admin_button.pack(pady=10)

    def show_books(self):
        books_window = ctk.CTkToplevel(self)
        books_window.title("Libros")
        books_window.geometry("400x300")

        status_label = ctk.CTkLabel(books_window, text="Mostrar libros:")
        status_label.pack(pady=10)

        self.status_var = tk.StringVar(value="Todos")
        all_books_radio = ctk.CTkRadioButton(books_window, text="Todos", variable=self.status_var, value="Todos")
        available_books_radio = ctk.CTkRadioButton(books_window, text="Disponibles", variable=self.status_var, value="Available")
        lent_books_radio = ctk.CTkRadioButton(books_window, text="Prestados", variable=self.status_var, value="Lent")

        all_books_radio.pack()
        available_books_radio.pack()
        lent_books_radio.pack()

        show_button = ctk.CTkButton(books_window, text="Mostrar", command=self.display_books)
        show_button.pack(pady=10)

        self.books_listbox = tk.Listbox(books_window)
        self.books_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def display_books(self):
        status = self.status_var.get()
        if status == "Todos":
            books = self.library.list_books()
        else:
            books = self.library.list_books(status=status)

        self.books_listbox.delete(0, tk.END)
        for book in books:
            self.books_listbox.insert(tk.END, f"{book['title']}: {book['status']}")

    def admin_login(self):
        username = simpledialog.askstring("Admin Login", "Ingrese el nombre de usuario del administrador:")
        password = simpledialog.askstring("Admin Login", "Ingrese la contraseña del administrador:", show='*')
        if self.db.check_admin_credentials(username, password):
            messagebox.showinfo("Login Exitoso", "Inicio de sesión como administrador exitoso.")
            self.show_admin_menu()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Acceso denegado.")

    def show_admin_menu(self):
        admin_window = ctk.CTkToplevel(self)
        admin_window.title("Admin Menu")
        admin_window.geometry("400x400")

        add_book_button = ctk.CTkButton(admin_window, text="Agregar libro", command=self.add_book)
        add_book_button.pack(pady=10)

        lend_book_button = ctk.CTkButton(admin_window, text="Prestar libro", command=self.lend_book)
        lend_book_button.pack(pady=10)

        return_book_button = ctk.CTkButton(admin_window, text="Devolver libro", command=self.return_book)
        return_book_button.pack(pady=10)

        remove_book_button = ctk.CTkButton(admin_window, text="Eliminar libro", command=self.remove_book)
        remove_book_button.pack(pady=10)

    def add_book(self):
        book_name = simpledialog.askstring("Agregar libro", "Ingrese el nombre del libro:")
        if book_name:
            result = self.library.new_book(book_name)
            messagebox.showinfo("Resultado", result)

    def lend_book(self):
        book_name = simpledialog.askstring("Prestar libro", "Ingrese el nombre del libro:")
        if book_name:
            result = self.library.lend_book(book_name)
            messagebox.showinfo("Resultado", result)

    def return_book(self):
        book_name = simpledialog.askstring("Devolver libro", "Ingrese el nombre del libro:")
        if book_name:
            result = self.library.return_book(book_name)
            messagebox.showinfo("Resultado", result)

    def remove_book(self):
        book_name = simpledialog.askstring("Eliminar libro", "Ingrese el nombre del libro:")
        if book_name:
            result = self.library.remove_book(book_name)
            messagebox.showinfo("Resultado", result)

if __name__ == "__main__":
    library = Biblioteca()
    db = Database()
    app = LibraryApp(library, db)
    app.mainloop()
