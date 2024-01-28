import os.path
import json
from api import PetFriends
from settings import email, password

pf = PetFriends()

# Получение ключа
def test_get_api_key_for_valid_user(email=email, password=password):
    """Получаем токен и проверяем что ответ приходит с кодом 200 и держит внутри себя
ключ со значением токена авторизации"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в results
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
    print(result)


# Получение спика питомцев
def test_get_list_of_pets_with_valid_key(filter=""):
    """Используя полученный ключ запрашиваем список питомцев, и проверяем что ответ
приходит с кодом 200 и содержит в себе список с тегом 'pets' длинна которого больше 0.
Достуное значение параметра filter - 'my_pets' либо '' """
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) > 0

# Создание питомца с фото
def test_add_new_pet_and_photo_with_valid_data(name='Черныш', animal_type='Кот',
                                               age='7', pet_photo='images/cat2.jpg'):
    """ Проверяем что можно добавить питомца используя корректные данные"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Создание питомца без фото
def test_add_new_pet_without_photo_with_valid_data(name='Красныш', animal_type='Кот',
                                                   age='10'):
    """ Проверяем что можно добавить питомца без фото используя валидные данные"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Добавоение к питомцу фото
def test_add_photo_with_valid_file(pet_photo='images/cat3.jpg'):
    """ Проверяем что можно добавить к уже существующему питомцу фото """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, results = pf.add_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert results['pet_photo'] != ""

# Обновление информации о питомце
def test_update_info_pet(name="Белыш", animal_type="cat", age="3"):
    """ Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_pet(auth_key, my_pets['pets'][0]['id'],
                                            name, animal_type, age)

        # Проверяем что статус ответа равен 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")

# Удаление питомца
def test_delete_pet_with_valid_id():
    """ Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Черныш", "Кот",
                       "5", "images/cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берем id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status,_ = pf.delete_pet(auth_key, pet_id)
    # Еще раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets.values()