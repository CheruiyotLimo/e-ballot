from app import schemas
from jose import jwt
# from db import client, session
from app.config import settings
import pytest

# @pytest.fixture()
# def test_user(client):
#     user_data = {"reg_num": "H31/2001/2015", "name": "Fraser", "email": 'fras@students.uonbi.ac.ke', 'password': '12345'}
#     res = client.post("/users/", json=user_data)
    
#     new_user = res.json()
#     print(new_user)
#     new_user['password'] = user_data['password']
#     assert res.status_code == 201
#     return new_user

# def test_root(client):
#     res = client.get("/")
#     print(res.json())
#     assert res.status_code == 200

# @pytest.mark.parametrize('reg_num, name, email, password', [
#     ("H31/200/1298", "Fraser", "q123@students.uonbi.ac.ke", "password12"),
#     (settings.admin_reg, "Mimo", "mims@students.uonbi.ac.ke", "56789"),
#     ("H31/2098/1203", "Don", "don@students.uonbi.ac.ke", "donno")
# ])
# def test_register_user(client, reg_num, name, email, password):
#     res = client.post("/users/", json={"reg_num": reg_num, "name": name, "email": email, "password": password})
#     print(res.json())
#     test_user = schemas.UserReturn(**res.json())
#     print(res.json().get('first_choice'))
#     print(res.json().get('role'))
#     # assert test_user.role == role
#     assert test_user.email == email
#     assert res.status_code == 201

# def test_user_login(client, test_user):
#     res = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
#     login_res = schemas.Token(**res.json())
#     payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
#     user_id = payload.get("user_id")
#     assert user_id == int(test_user['id'])
#     assert login_res.token_type == 'bearer'
#     assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrong@students.uonbi.ac.ke', '12345', 404),
#     ('fras@students.uonbi.ac.ke', 'wrong', 403),
#     ('fras@students.uonbi.ac.ke', None, 422),
#     (None, '12345', 422),
# ])
# def test_incorrect_login(client, test_user, email, password, status_code):
#     res = client.post('/login/', data = {'username': email, 'password': password})
#     assert res.status_code == status_code


# def test_get_all_users(authorized_client_admin, create_user_list):
#     res = authorized_client_admin.get("/users")
#     print(res.json())
#     assert res.status_code == 200

# @pytest.mark.parametrize("choice, hosp_id, status_code", [
#     ("1", 2, 201),
#     ("1", 3, 201),
#     ("1", 1, 201),
# ])
# def test_patch_user_successful(authorized_client, test_user, create_hospitals_list, choice, hosp_id, status_code):
#     """ Tests  for successful user updating of their first choice."""
#     test_user['first_choice'] = None
#     test_user['second_choice'] = None
#     res = authorized_client.patch(f'/users/choice/{choice}/', json={'first_choice': hosp_id})
#     user = schemas.UserChoice(**res.json())
#     assert user.first_choice == hosp_id
#     print(user)
#     assert res.status_code == status_code


@pytest.mark.parametrize("choice, hosp_id, status_code", [
    ("2", 2, 201),
    ("2", 3, 201),
    ("2", 4, 201),
])
def test_patch_user_successful_second(authorized_client, create_hospitals_list, test_user, choice, hosp_id, status_code):
    """ Tests  for successful user updating of their second choice."""
    # test_user['first_choice'] = '1'
    # test_user['second_choice'] = None
    authorized_client.patch(f'users/choice/1', json={'first_choice': 1})
    res = authorized_client.patch(f'/users/choice/{choice}/', json={'first_choice': hosp_id})
    print(res.json())
    # user = schemas.UserChoice(**res.json())
    # assert user.first_choice == hosp_id
    # print(user)
    assert res.status_code == status_code


# @pytest.mark.parametrize("choice, hosp_id, role, status_code", [
#     ("2", 2, None, 409),
#     ("2", 1, None, 409),
#     ('2', 3, 'admin', 403),
# ])
# def test_patch_user_failed(authorized_client, test_user, create_hospitals_list, choice, hosp_id, role, status_code):
#     """ Testing failed user updating of their 2nd choice. """
#     test_user['first_choice'] = 1
#     test_user['second_choice'] = None
#     test_user['role'] = role
#     res = authorized_client.patch(f'/users/choice/{choice}/', json={'first_choice': hosp_id})
#     print(res.json())
#     user = res.json()
#     # assert user.first_choice == hosp_id
#     # print(user.first_choice)
#     assert res.status_code == status_code
