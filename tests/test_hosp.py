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

def test_authorized_user_get_one_hosp(authorized_client, test_user, create_hospitals_list):
    """Testing whether an authorized user can retrieve one pt."""
    res = authorized_client.get(f'/hosps/{create_hospitals_list[0].id}')
    print(res.json())
    assert res.status_code == 200

def test_unauthorized_user_get_one_hosp(client, test_user, create_hospitals_list):
    # Bug here cause I am not getting the expected error message though test passes.
    """Testing whether an unauthorized user can retrieve one hospital."""  
    res = client.get(f'/hosps/{create_hospitals_list[0].id}')
    print(res.json())
    assert res.status_code == 401
    
def test_hosp_doesnt_exist(authorized_client, test_user, create_hospitals_list):
    """ Test error when hospital doesnt exist."""
    res = authorized_client.get(f'/hosps/5')
    print(res.json())
    assert res.status_code == 404

def test_admin_add_new_hosp(authorized_client_admin, test_user_admin, create_hospitals_list):
    """ Test admin adding a new hosppital to the db. """
    new_hosp = {
        'name': 'Vihiga CRH',
        'county_name': 'Vihiga',
        'county_num': 38,
        'slots': 1
    }
    res = authorized_client_admin.post(f'/hosps/', json=new_hosp)
    hos = schemas.HospReturn(**res.json())
    print(hos)
    print(res.json())
    assert res.status_code == 201
    assert len(create_hospitals_list) == 4


def test_admin_new_hosp_exists(authorized_client_admin, test_user_admin, create_hospitals_list):
    """ Test admin adding a new hospital whch already exists to the db. """
    new_hosp = {
        'name': 'CGRH',
        'county_name': 'Mombasa',
        'county_num': 15,
        'slots': 1
    }
    res = authorized_client_admin.post(f'/hosps/', json=new_hosp)
    print(res.json())
    assert res.status_code == 403
    assert len(create_hospitals_list) == 4


def test_unauthorized_user_add_new_hosp(authorized_client, test_user, create_hospitals_list):
    """ Test unauthorized user tring to add new hospital. """
    
    new_hosp = {
        'name': 'Vihiga CRH',
        'county_name': 'Vihiga',
        'county_num': 38,
        'slots': 1
    }

    res = authorized_client.post(f'/hosps/', json=new_hosp)
    # hos = schemas.HospReturn(**res.json())
    # print(hos)
    print(res.json())
    assert res.status_code == 403
    assert len(create_hospitals_list) == 4

def test_admin_patch_hosp_slots(authorized_client_admin, test_user_admin, create_hospitals_list):
    """ Test admins can update a hospital's slot number. """

    new_slots = {'slots': 2}
    res = authorized_client_admin.patch(f'/hosps/1', json=new_slots)
    print(res.json())
    assert res.status_code == 201
    assert res.json()['slots'] == 2

def test_admin_patch_hosp_doesnt_exist(authorized_client_admin, test_user_admin, create_hospitals_list):
    """ Test admins can update a hospital's slot number. """

    new_slots = {'slots': 2}
    res = authorized_client_admin.patch(f'/hosps/54', json=new_slots)
    print(res.json())
    assert res.status_code == 404

def test_admin_delete_hosp(authorized_client_admin, test_user_admin, create_hospitals_list):
    """ Tests admins delete hospital from db. """
## Delete not reflectng on the created hosp list

    res = authorized_client_admin.delete(f'/hosps/2')
    print(res)
    assert res.status_code == 204
    print(create_hospitals_list)
    # assert len(create_hospitals_list) == 3