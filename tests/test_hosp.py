from app import schemas
from jose import jwt
# from db import client, session
from app.config import settings
import pytest

def test_get_all_hospitals(authorized_client, test_user, create_hospitals_list):
    """Testing if user can get all listed hospitals."""
    res = authorized_client.get(f'/hosps/')
    hosp_list = res.json()

    assert len(hosp_list) == len(create_hospitals_list)
    assert res.status_code == 200

## Bug at endpoint, r=to be fixed then we can run this test
# @pytest.mark.parametrize('search, status_code, num', [
#     ('R', 200, 2),
#     ('KNH', 200, 1),
#     ('Z', 404, 0)
# ])
# def test_get_all_hospitals_searched(authorized_client, test_user, create_hospitals_list, search="R"):
#     """Testing that endpoint filters through list with searched element"""
#     res = authorized_client.get(f'/hosps?search={search}/')
    # print(res.json())

def test_unauthorized_user_get_one_hosp(authorized_client, test_user, create_hospitals_list):
    """Testing whether an unauthorized user can retrieve one post."""
    res = authorized_client.get(f'/hosps/{create_hospitals_list[0].id}')
    print(res.json())
    assert res.status_code == 401
    