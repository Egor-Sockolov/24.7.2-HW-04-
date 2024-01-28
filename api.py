import requests
from requests_toolbelt import MultipartEncoder
import json

class PetFriends:

    def __init__(self): # Записываем базовый URL
        self.baseURL = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод получения ключа, данные для headers используются из файла settings
        Пробуем получить от ответа результат в формате json
        иначе получаем обчный текст"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.baseURL + '/api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """ Метод получения списка питомцев совпадающего с фильтрами filter
        Достуное значение параметра filter - 'my_pets' либо '' """

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.baseURL + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """ Метод отправляет на сервер данные с фотографией добавляемого питомца и возвращает статус
        запроса на сервер и результат в формате json с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, "rb"), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.baseURL + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str,
                                  age: str) -> json:
        """ Метод отправляет на сервер данные без фотографии добовляемого питомца и возвращает статус
        запроса на сервер и результат в формате json с данными добавленного питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.baseURL + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def add_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """ Метод отправляет запрос на сервер о добавлении фото к карточке питомца по указанному ID и
        возвращает статус запроса и results в формате json"""

        headers = {'auth_key': auth_key['key']}
        photo = {'pet_photo': (pet_photo, open(pet_photo, "rb"), 'image/jpeg')}

        res = requests.post(self.baseURL + '/api/pets/set_photo/' + pet_id, headers=headers, files=photo)
        status = res.status_code
        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text
        return status, results


    def update_info_pet(self, auth_key: json, pet_id: str,
                        name: str, animal_type: str, age: str) -> json:
        """ Метод отправляет запрос на сервер о обновлении данных питомца по указанному ID и
        возвращает статус запроса и results в формате json с обновленными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.put(self.baseURL + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """ Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате json """

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.baseURL + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result