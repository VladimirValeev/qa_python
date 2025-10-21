import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# 1) add_new_book - позитивный сценарий
def test_add_new_book_adds_book(collector):
    collector.add_new_book('Три товарища')
    assert 'Три товарища' in collector.get_books_genre()


# 2) add_new_book - некорректные имена не добавляются
@pytest.mark.parametrize('bad_name', ['', 'A' * 41])
def test_add_new_book_rejects_invalid_names(collector, bad_name):
    collector.add_new_book(bad_name)
    assert bad_name not in collector.get_books_genre()


# 3) add_new_book - дубли не создаются
def test_add_new_book_duplicate_is_ignored(collector):
    collector.add_new_book('Мастер и Маргарита')
    collector.add_new_book('Мастер и Маргарита')
    assert list(collector.get_books_genre().keys()).count('Мастер и Маргарита') == 1


# 4) add_new_book - у добавленной книги жанр пустой
def test_added_book_has_no_genre_initially(collector):
    collector.add_new_book('Пикник на обочине')
    assert collector.get_book_genre('Пикник на обочине') == ''


# 5) set_book_genre - валидный жанр устанавливается
def test_set_book_genre_valid(collector):
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')
    assert collector.get_book_genre('Дюна') == 'Фантастика'


# 6) set_book_genre - невалидный жанр игнорируется
def test_set_book_genre_invalid_ignored(collector):
    collector.add_new_book('Собачье сердце')
    collector.set_book_genre('Собачье сердце', 'Поэзия')  # такого жанра нет в списке genre
    assert collector.get_book_genre('Собачье сердце') == ''


# 7) get_books_with_specific_genre - возвращает корректный список
def test_get_books_with_specific_genre_returns_expected(collector):
    collector.add_new_book('Оно')
    collector.add_new_book('Незнайка')
    collector.set_book_genre('Оно', 'Ужасы')
    collector.set_book_genre('Незнайка', 'Мультфильмы')

    assert collector.get_books_with_specific_genre('Ужасы') == ['Оно']


# 8) get_books_for_children - книги с возрастным рейтингом исключаются
def test_get_books_for_children_filters_age_rating(collector):
    collector.add_new_book('Оно')
    collector.add_new_book('Иван Васильевич меняет профессию')
    collector.set_book_genre('Оно', 'Ужасы')  # есть возрастной рейтинг
    collector.set_book_genre('Иван Васильевич меняет профессию', 'Комедии')  # для детей ок

    assert collector.get_books_for_children() == ['Иван Васильевич меняет профессию']


# 9) add_book_in_favorites - добавляет только если книга есть в словаре и без дублей
def test_add_book_in_favorites_only_existing_and_no_duplicates(collector):
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    collector.add_book_in_favorites('Дюна')  # повторно
    collector.add_book_in_favorites('Несуществующая')  # нет в словаре - игнор

    assert collector.get_list_of_favorites_books() == ['Дюна']


# 10) delete_book_from_favorites + get_list_of_favorites_books - удаление работает
def test_delete_book_from_favorites_updates_list(collector):
    collector.add_new_book('Трудно быть богом')
    collector.add_book_in_favorites('Трудно быть богом')
    collector.delete_book_from_favorites('Трудно быть богом')

    assert collector.get_list_of_favorites_books() == []
