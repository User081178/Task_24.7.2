from random import random

from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


# Добавление питомца
def test_add_new_pet_with_valid_data(name='Дося', animal_type='безпороды',
                                     age='2', pet_photo='images/Cat_2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


# Удаление питомца
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Досинья", "кошка", "3", "images/Cat_2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


# Обновление информации питомца
def test_successful_update_self_pet_info(name='Досинья', animal_type='Кошечка', age=2):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("My pet is not there")


# Передача ключа с пустым полем email
def test_get_api_key_for_invalid_user(email=None, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


# Создание питомца с пустым полем name
def test_add_new_pet_with_invalid_data(name=None, animal_type='безпороды',
                                       age='2', pet_photo='images/Cat_2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''


# Удаление питомца с несуществующим id
def test_unsuccessful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets_before_deletion = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = str(random())
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets_after_deletion = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert my_pets_after_deletion == my_pets_before_deletion


# Создание питомца с полем name - длинная строка
def test_add_new_pet_with_long_name(animal_type='безпороды',
                                    age='2', pet_photo='images/Cat_2.jpg'):
    name = 'qwertyyaup[assssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss' \
           'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss' \
           'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss' \
           'sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


# Создание  питомца с полем age - отрицательное значение
def test_add_new_pet_with_negative_age(name='Дося', animal_type='безпороды',
                                       age='-100', pet_photo='images/Cat_2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


# Создание питома с неправильной отправкой фото
def test_add_new_pet_with_invalid_pet_photo(name='Дося', animal_type='безпороды',
                                            age='2', pet_photo='images/Cat_2.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] != pet_photo


# Обновление питомца с несуществующим id
def test_update_pet_with_not_exist_id(name='Досинья', animal_type='Кошечка', age=2):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = str(random())
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400


# Создание питомца с полем age - строка с текстом
def test_add_new_pet_age_as_string(name='Дося', animal_type='безпороды',
                                   age='mjdfj', pet_photo='images/Cat_2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


# Создание питомца с фото в формате txt
def test_add_new_pet_with_photo_as_text(name='Дося', animal_type='безпороды',
                                        age='2', pet_photo='images/123.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] == ''