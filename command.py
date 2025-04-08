"""Реализация паттерна Command"""
class Command:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class Light:
    def turn_on(self):
        print("Light is ON")

    def turn_off(self):
        print("Light is OFF")


class TurnOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()

class TurnOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()
        if self.command:
            self.command.execute()

    def press_undo(self):
        if self.command:
            self.command.undo()
#Задание 2
import time
import os

class NumberSet:
    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.numbers = self.load_numbers()
            self.last_modified = os.path.getmtime(filepath)
        except FileNotFoundError:
            print(f"File not found: {filepath} during initialization.  Setting last_modified to 0.")
            self.numbers = []
            self.last_modified = 0

    def load_numbers(self):
        try:
            with open(self.filepath, 'r') as f:
                return [int(num) for num in f.read().strip().split()]
        except (FileNotFoundError, ValueError):
            print("Error loading numbers from file.")
            return []

    def refresh_data(self):
        try:
            current_modified_time = os.path.getmtime(self.filepath)
            if current_modified_time > self.last_modified:
                print("Reloading data...")
                self.numbers = self.load_numbers()
                self.last_modified = current_modified_time
        except FileNotFoundError:
            print("File not found during refresh.")

    def get_numbers(self):
        self.refresh_data()
        return self.numbers

    def calculate(self, operation):
        self.refresh_data() 
        if not self.numbers:
            return None  
        if operation == "sum":
            return sum(self.numbers)
        elif operation == "max":
            return max(self.numbers)
        elif operation == "min":
            return min(self.numbers)
        else:
            return None  



class LoggingNumberSet:
    def __init__(self, number_set, log_filepath="app.log"):
        self.number_set = number_set
        self.log_filepath = log_filepath

    def _log(self, method_name, *args):  
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_message = f"[{timestamp}] {method_name}({', '.join(map(str, args))})"
        print(f"Logging: {log_message}")
        with open(self.log_filepath, 'a') as f:  
            f.write(log_message + '\n')

    def get_numbers(self):
        self._log("get_numbers")
        return self.number_set.get_numbers()

    def calculate(self, operation): 
        self._log(f"calculate", operation)
        return self.number_set.calculate(operation)

class Application:
    def __init__(self, number_set_proxy):
        self.number_set_proxy = number_set_proxy

    def run(self, command): 
        if command == "numbers":
            result = self.number_set_proxy.get_numbers()
        elif command in ("sum", "max", "min"):
            result = self.number_set_proxy.calculate(command)
        else:
            print("Unknown command.")
            return
        print(f"Result: {result}")


if __name__ == "__main__":
    test_filepath = "numbers.txt"
    with open(test_filepath, "w") as f:
        f.write("10 5 20 15\n")

    real_number_set = NumberSet(test_filepath)
    logging_number_set = LoggingNumberSet(real_number_set)
    app = Application(logging_number_set)

    app.run("sum")
    app.run("max")
    app.run("min")
    app.run("numbers")

    time.sleep(2)
    with open(test_filepath, "w") as f:
        f.write("2 4 6 8 10\n")
    time.sleep(1)

    app.run("sum")
    app.run("max")
    app.run("min")
    app.run("numbers")

    test_filepath_non_existent = "non_existent_file.txt"
    real_number_set_non_existent = NumberSet(test_filepath_non_existent)
    logging_number_set_non_existent = LoggingNumberSet(real_number_set_non_existent)
    app_non_existent = Application(logging_number_set_non_existent)
    app_non_existent.run("sum") 

#Задание 3 
import time
import json
import os
from abc import ABC, abstractmethod

# ----------------------- Сущности -----------------------
class Entity(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass

class Book(Entity):
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['author'], data['isbn'])

    def __str__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"


class Librarian(Entity):
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    def to_dict(self):
        return {"name": self.name, "employee_id": self.employee_id}

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['employee_id'])

    def __str__(self):
        return f"Librarian(name='{self.name}', employee_id='{self.employee_id}')"


class Reader(Entity):
    def __init__(self, name, reader_id):
        self.name = name
        self.reader_id = reader_id
        self.borrowed_books = []

    def to_dict(self):
        return {"name": self.name, "reader_id": self.reader_id, "borrowed_books": self.borrowed_books}

    @classmethod
    def from_dict(cls, data):
        reader = cls(data['name'], data['reader_id'])
        reader.borrowed_books = data.get('borrowed_books', [])  # Обрабатываем отсутствие borrowed_books
        return reader

    def __str__(self):
        return f"Reader(name='{self.name}', reader_id='{self.reader_id}', borrowed_books={self.borrowed_books})"

    def borrow_book(self, book):
        self.borrowed_books.append(book.isbn)

    def return_book(self, book):
        if book.isbn in self.borrowed_books:
            self.borrowed_books.remove(book.isbn)

# ----------------------- Хранение данных (Паттерн Стратегия) -----------------------
class DataStorageStrategy(ABC):
    @abstractmethod
    def load_data(self, filepath):
        pass

    @abstractmethod
    def save_data(self, filepath, data):
        pass

class JsonDataStorage(DataStorageStrategy):
    def load_data(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Ошибка загрузки данных из {filepath}. Возвращаю пустые данные.")
            return {"books": [], "librarians": [], "readers": []}

    def save_data(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)


# ----------------------- Репозиторий (Data Access Object) -----------------------
class Repository(ABC):
    @abstractmethod
    def get(self, entity_id):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass

    @abstractmethod
    def list_all(self):
        pass


class InMemoryRepository(Repository):  # Простая реализация в памяти
    def __init__(self):
        self._data = {}

    def get(self, entity_id):
        return self._data.get(entity_id)

    def add(self, entity):
        entity_id = self._generate_id(entity) # Используем уникальный ID
        self._data[entity_id] = entity
        return entity_id  # возвращаем ID

    def update(self, entity):
        entity_id = self._generate_id(entity) # Используем ID из сущности
        if entity_id in self._data:
            self._data[entity_id] = entity
        else:
            raise ValueError(f"Сущность с ID {entity_id} не найдена")

    def delete(self, entity_id):
        if entity_id in self._data:
            del self._data[entity_id]
        else:
            raise ValueError(f"Сущность с ID {entity_id} не найдена")

    def list_all(self):
        return list(self._data.values())

    def _generate_id(self, entity):
        if isinstance(entity, Book):
            return entity.isbn
        elif isinstance(entity, Librarian):
            return entity.employee_id
        elif isinstance(entity, Reader):
            return entity.reader_id
        else:
            raise ValueError("Неподдерживаемый тип сущности")

class FileRepository(Repository):
    def __init__(self, entity_type, storage_strategy, filepath):
        self.entity_type = entity_type
        self.storage_strategy = storage_strategy
        self.filepath = filepath
        self._data = self._load_data()  # Загружаем данные при инициализации

    def _load_data(self):
       data = self.storage_strategy.load_data(self.filepath)
       entity_name = self.entity_type.__name__.lower() + "s"  # "books", "librarians", "readers"

       if entity_name in data and isinstance(data[entity_name], list):  # Проверяем структуру данных
           return {self._generate_id(self.entity_type.from_dict(item)): self.entity_type.from_dict(item) for item in data[entity_name]}
       else:
           print(f"Некорректные данные {entity_name} найдены в файле.")
           return {}  # Обрабатываем отсутствие данных

    def _save_data(self):
        all_data = self.storage_strategy.load_data(self.filepath) # Загружаем все данные

        entity_name = self.entity_type.__name__.lower() + "s"  # "books", "librarians", "readers"
        entity_list = [entity.to_dict() for entity in self.list_all()]
        all_data[entity_name] = entity_list # Назначаем данные списку сущностей

        self.storage_strategy.save_data(self.filepath, all_data)


    def get(self, entity_id):
        return self._data.get(entity_id)

    def add(self, entity):
        entity_id = self._generate_id(entity)
        self._data[entity_id] = entity
        self._save_data()
        return entity_id

    def update(self, entity):
        entity_id = self._generate_id(entity)
        if entity_id in self._data:
            self._data[entity_id] = entity
            self._save_data()
        else:
            raise ValueError(f"Сущность с ID {entity_id} не найдена")

    def delete(self, entity_id):
        if entity_id in self._data:
            del self._data[entity_id]
            self._save_data()
        else:
            raise ValueError(f"Сущность с ID {entity_id} не найдена")

    def list_all(self):
        return list(self._data.values())

    def _generate_id(self, entity):
        if isinstance(entity, Book):
            return entity.isbn
        elif isinstance(entity, Librarian):
            return entity.employee_id
        elif isinstance(entity, Reader):
            return entity.reader_id
        else:
            raise ValueError("Неподдерживаемый тип сущности")

# ----------------------- Логгирование (Паттерн Прокси) -----------------------
class RepositoryLoggingProxy(Repository):
    def __init__(self, repository, log_filepath="app.log"):
        self.repository = repository
        self.log_filepath = log_filepath

    def _log(self, method_name, entity_id=None, entity=None):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message = f"[{timestamp}] {method_name}"
        if entity_id:
            message += f" (ID: {entity_id})"
        if entity:
            message += f" (Сущность: {entity})"
        print(message) # лог в консоль
        with open(self.log_filepath, 'a') as f:
            f.write(message + '\n')

    def get(self, entity_id):
        self._log("get", entity_id=entity_id)
        return self.repository.get(entity_id)

    def add(self, entity):
        self._log("add", entity=entity)
        entity_id = self.repository.add(entity)
        self._log("add - присвоен ID", entity_id=entity_id)
        return entity_id

    def update(self, entity):
        self._log("update", entity=entity)
        self.repository.update(entity)

    def delete(self, entity_id):
        self._log("delete", entity_id=entity_id)
        self.repository.delete(entity_id)

    def list_all(self):
        self._log("list_all")
        return self.repository.list_all()


# ----------------------- Поиск (Паттерн Стратегия) -----------------------
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, repository, query):
        pass

class BookSearchStrategy(SearchStrategy):
    def search(self, repository, query):
        results = []
        query = query.lower()
        for book in repository.list_all():
            if query in book.title.lower() or query in book.author.lower() or query == book.isbn.lower():
                results.append(book)
        return results

# ----------------------- Паттерн Команда -----------------------
class Command(ABC):
    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class AddBookCommand(Command):
    def execute(self, book):
        return self.receiver.add(book)

class UpdateBookCommand(Command):
    def execute(self, book):
        self.receiver.update(book)

class DeleteBookCommand(Command):
    def execute(self, book_id):
        self.receiver.delete(book_id)

class ListBooksCommand(Command):
    def execute(self):
        return self.receiver.list_all()

class SearchBooksCommand(Command):
    def execute(self, query):
        return self.receiver.search(query)

# ----------------------- Фасад -----------------------
class LibraryServiceFacade:
    def __init__(self, book_repository, librarian_repository, reader_repository, book_search_strategy):
        self.book_repository = book_repository
        self.librarian_repository = librarian_repository
        self.reader_repository = reader_repository
        self.book_search_strategy = book_search_strategy

    def add_book(self, book):
        add_book_command = AddBookCommand(self.book_repository)
        return add_book_command.execute(book)

    def update_book(self, book):
        update_book_command = UpdateBookCommand(self.book_repository)
        update_book_command.execute(book)

    def delete_book(self, book_id):
        delete_book_command = DeleteBookCommand(self.book_repository)
        delete_book_command.execute(book_id)

    def list_books(self):
        list_books_command = ListBooksCommand(self.book_repository)
        return list_books_command.execute()

    def search_books(self, query):
        search_books_command = SearchBooksCommand(self.book_search_strategy)
        return search_books_command.execute(self.book_repository, query)

    # Операции с читателями
    def add_reader(self, reader):
        return self.reader_repository.add(reader)

    def get_reader(self, reader_id):
        return self.reader_repository.get(reader_id)

    def update_reader(self, reader):
        self.reader_repository.update(reader)

    def delete_reader(self, reader_id):
        self.reader_repository.delete(reader_id)

    def list_readers(self):
        return self.reader_repository.list_all()

    def borrow_book(self, reader_id, book):
        reader = self.reader_repository.get(reader_id)
        if not reader:
            raise ValueError(f"Читатель с ID {reader_id} не найден")

        book_isbn = book.isbn #Предполагаем, что книги уже добавлены

        reader.borrow_book(book)
        self.reader_repository.update(reader) # Сохраняем обновленного читателя

    def return_book(self, reader_id, book):
        reader = self.reader_repository.get(reader_id)
        if not reader:
            raise ValueError(f"Читатель с ID {reader_id} не найден")

        book_isbn = book.isbn
        reader.return_book(book)
        self.reader_repository.update(reader)  # Сохраняем обновленного читателя

# ----------------------- Главное приложение -----------------------
class LibraryApp:
    def __init__(self, library_service):
        self.library_service = library_service

    def add_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        isbn = input("Введите ISBN книги: ")
        book = Book(title, author, isbn)
        book_id = self.library_service.add_book(book)
        print(f"Книга добавлена с ID: {book_id}")

    def update_book(self):
        isbn = input("Введите ISBN книги для обновления: ")
        book = self.library_service.book_repository.get(isbn)
        if not book:
            print("Книга не найдена.")
            return

        new_title = input(f"Введите новое название (текущее: {book.title}): ") or book.title
        new_author = input(f"Введите нового автора (текущий: {book.author}): ") or book.author
        book.title = new_title
        book.author = new_author

        self.library_service.update_book(book)
        print("Книга обновлена.")

    def delete_book(self):
        isbn = input("Введите ISBN книги для удаления: ")
        try:
            self.library_service.delete_book(isbn)
            print("Книга удалена.")
        except ValueError as e:
            print(e)

    def list_books(self):
        books = self.library_service.list_books()
        for book in books:
            print(book)

    def search_books(self):
        query = input("Введите поисковый запрос: ")
        results = self.library_service.search_books(query)
        if results:
            for book in results:
                print(book)
        else:
            print("Книги, соответствующие запросу, не найдены.")

    def add_reader(self):
        name = input("Введите имя читателя: ")
        reader_id = input("Введите ID читателя: ")
        reader = Reader(name, reader_id)
        reader_id = self.library_service.add_reader(reader)
        print(f"Читатель добавлен с ID: {reader_id}")

    def borrow_book(self):
        reader_id = input("Введите ID читателя: ")
        book_isbn = input("Введите ISBN книги для выдачи: ")

        book = self.library_service.book_repository.get(book_isbn)
        if not book:
            print("Книга не найдена")
            return

        try:
            self.library_service.borrow_book(reader_id, book)
            print(f"Книга {book.title} выдана читателю {reader_id}")
        except ValueError as e:
            print(e)

    def return_book(self):
        reader_id = input("Введите ID читателя: ")
        book_isbn = input("Введите ISBN книги для возврата: ")

        book = self.library_service.book_repository.get(book_isbn)
        if not book:
            print("Книга не найдена")
            return

        try:
            self.library_service.return_book(reader_id, book)
            print(f"Книга {book.title} возвращена читателем {reader_id}")
        except ValueError as e:
            print(e)

    def run(self):
        while True:
            print("\nМеню приложения Библиотека:")
            print("1. Добавить книгу")
            print("2. Обновить книгу")
            print("3. Удалить книгу")
            print("4. Список книг")
            print("5. Поиск книг")
            print("6. Добавить читателя")
            print("7. Выдать книгу")
            print("8. Вернуть книгу")
            print("9. Выход")

            choice = input("Введите ваш выбор: ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.update_book()
            elif choice == '3':
                self.delete_book()
            elif choice == '4':
                self.list_books()
            elif choice == '5':
                self.search_books()
            elif choice == '6':
                self.add_reader()
            elif choice == '7':
                self.borrow_book()
            elif choice == '8':
                self.return_book()
            elif choice == '9':
                print("Выход...")
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

# ----------------------- Главное исполнение -----------------------
if __name__ == "__main__":
    # Конфигурация
    DATA_FILE = "library_data.json"
    LOG_FILE = "library_app.log"

    # Инициализация компонентов
    json_storage = JsonDataStorage()

    book_repository = RepositoryLoggingProxy(
        FileRepository(Book, json_storage, DATA_FILE), LOG_FILE
    )

    librarian_repository = RepositoryLoggingProxy(
        FileRepository(Librarian, json_storage, DATA_FILE), LOG_FILE
    )

    reader_repository = RepositoryLoggingProxy(
        FileRepository(Reader, json_storage, DATA_FILE), LOG_FILE
    )

    book_search_strategy = BookSearchStrategy()

    library_service = LibraryServiceFacade(
        book_repository, librarian_repository, reader_repository, book_search_strategy
    )

    app = LibraryApp(library_service)
    app.run()