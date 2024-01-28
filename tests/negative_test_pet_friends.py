import os.path
import json
from api import PetFriends
from settings import email, password, invalid_email, invalid_password, invalid_auth_key

pf = PetFriends()

# Получение ключа
def test_get_api_key_for_invalid_email(email=invalid_email, password=password):
    """ Проверка получения ключа авторизации с невалидным email """

    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Получение ключа
def test_get_api_key_for_invalid_password(email=email, password=invalid_password):
    """ Проверка получения ключа авторизации с невалидным password """

    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Получение ключа
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверка получения ключа авторизации с невалидным email и password """

    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Получение списка всех питомцев
def test_get_list_of_pets_with_invalid_auth_key(filter=""):
    """ Пороверка получения списка всех питомцев неавторизированным пользователем """

    status, result = pf.get_list_of_pets(auth_key={'key': invalid_auth_key}, filter=filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Создание питомца
def test_add_new_pet_with_invalid_age(name='Красныш', animal_type='Кот', age='100'):
    """ Проверка создания питомца с указанием слишком большого значения возраста """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Создание питомца
def test_add_new_pet_with_negative_age(name='Красныш', animal_type='Кот', age='-10'):
    """ Проверка создания питомца с указанием отрицательного возраста """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Создание питомца
def test_add_new_pet_with_invalid_name(name='', animal_type='Кот', age='6'):
    """ Проверка создания питомца с указанием пустого имени """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Создание питомца
def test_add_new_pet_with_invalid_type(name='Черныш', animal_type='', age='6'):
    """ Проверка создания питомца с указанием пустого типа """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Создание питомца
def test_add_new_pet_with_invalid_type(name='Черныш', animal_type='Кот', age=''):
    """ Проверка создания питомца с указанием пустого возраста """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Создание питомца
def test_add_new_pet_with_invalid_field(name='', animal_type='', age=''):
    """ Проверка создания питомца с указанием пустых параметров"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Добавление к карточке питомца файла формата txt вместо jpg
def test_add_invalid_photo_of_pet(pet_photo='images/text.txt'):
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, results = pf.add_photo(auth_key, pet_id, pet_photo)

    assert status == 500


# Изменение информации о питомце
def test_update_invalid_info(name='11223344', animal_type='44332211', age='Десять'):
    """ Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_pet(auth_key, my_pets['pets'][0]['id'],
                                            name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")

# Удаление питомца
def test_delele_pet_on_main_page():
    """ Проверяем возможность удаления чужого питомца с главной страницы """

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "")

    # Берем id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status,_ = pf.delete_pet(auth_key, pet_id)

    assert status == 403