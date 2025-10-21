import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# 1) add_new_book - книга добавляется
def test_add_new_book_adds_book(collector):
    collector.add_new_book('Три товарища')
    assert 'Три товарища' in collector.books_genre


# 2) add_new_book - некорректные имена не добавляются
@pytest.mark.parametrize('bad_name', ['', 'A' * 41])
def test_add_new_book_rejects_invalid_names(collector, bad_name):
    collector.add_new_book(bad_name)
    assert bad_name not in collector.books_genre


# 3) add_new_book - дубль игнорируется
def test_add_new_book_duplicate_is_ignored(collector):
    collector.add_new_book('Мастер и Маргарита')
    collector.add_new_book('Мастер и Маргарита')
    assert len(collector.books_genre) == 1


# 4) set_book_genre - валидный жанр устанавливается
def test_set_book_genre_valid(collector):
    collector.books_genre['Дюна'] = ''
    collector.set_book_genre('Дюна', 'Фантастика')
    assert collector.books_genre['Дюна'] == 'Фантастика'


# 5) set_book_genre - невалидный жанр игнорируется
def test_set_book_genre_invalid_ignored(collector):
    collector.books_genre['Собачье сердце'] = ''
    collector.set_book_genre('Собачье сердце', 'Поэзия')
    assert collector.books_genre['Собачье сердце'] == ''


# 6) get_book_genre - возвращает жанр
def test_get_book_genre_returns_value(collector):
    collector.books_genre = {'Дюна': 'Фантастика'}
    assert collector.get_book_genre('Дюна') == 'Фантастика'


# 7) get_book_genre - возвращает None для неизвестной книги
def test_get_book_genre_returns_none_for_unknown(collector):
    assert collector.get_book_genre('Неизвестная книга') is None


# 8) get_books_with_specific_genre - возвращает нужные книги
def test_get_books_with_specific_genre_returns_expected(collector):
    collector.books_genre = {'Оно': 'Ужасы', 'Незнайка': 'Мультфильмы'}
    assert collector.get_books_with_specific_genre('Ужасы') == ['Оно']


# 9) get_books_genre - возвращает текущий словарь
def test_get_books_genre_returns_mapping(collector):
    collector.books_genre = {'Оно': 'Ужасы', 'Незнайка': 'Мультфильмы'}
    assert collector.get_books_genre() == {'Оно': 'Ужасы', 'Незнайка': 'Мультфильмы'}


# 10) get_books_for_children - исключает возрастные жанры
def test_get_books_for_children_filters_age_rating(collector):
    collector.books_genre = {
        'Оно': 'Ужасы',
        'Иван Васильевич меняет профессию': 'Комедии',
    }
    assert collector.get_books_for_children() == ['Иван Васильевич меняет профессию']


# 11) add_book_in_favorites - добавляет существующую книгу
def test_add_book_in_favorites_adds_existing(collector):
    collector.books_genre = {'Дюна': 'Фантастика'}
    collector.add_book_in_favorites('Дюна')
    assert collector.favorites == ['Дюна']


# 12) add_book_in_favorites - не добавляет дубликаты
def test_add_book_in_favorites_no_duplicates(collector):
    collector.books_genre = {'Три товарища': ''}
    collector.favorites = ['Три товарища']
    collector.add_book_in_favorites('Три товарища')
    assert collector.favorites == ['Три товарища']


# 13) delete_book_from_favorites - удаляет книгу
def test_delete_book_from_favorites_removes_book(collector):
    collector.favorites = ['Дюна']
    collector.delete_book_from_favorites('Дюна')
    assert collector.favorites == []


# 14) get_list_of_favorites_books - возвращает список избранных
def test_get_list_of_favorites_books_returns_all(collector):
    collector.favorites = ['Три товарища', 'Дюна']
    assert collector.get_list_of_favorites_books() == ['Три товарища', 'Дюна']
                                                                                                                        