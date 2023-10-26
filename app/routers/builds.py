from fastapi import APIRouter, HTTPException, status, Depends
from ..db import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from Scripts import randomizer
from . import hosp, users, auth, final
import json, time
from typing import Literal
from sqlalchemy.sql.expression import func
import pandas as pd
import random
import numpy as np

router = APIRouter(
    prefix="/build",
    tags=["Builds"]
)


@router.post('/users/', status_code=status.HTTP_201_CREATED)
def build_users(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # verify the user is an admin
    oauth2.verify_admin(current_user)

    user_list = {
        "Caleb": ["H31/2189/1017", "Caleb Musyoki", "calmus@students.uonbi.ac.ke", "calmus103"],
        "Limo": ["H31/2700/1027", "Yony Limo", "yony@students.uonbi.ac.ke", "oakeart"],
        "Abel": ['H31/2010/1987', 'Gakuya Mwangi', 'gaks@students.uonbi.ac.ke', 'mkm'],
        'Kipsang': ['H31/2182/1192', 'Elijah Kipsang', 'kips@students.uonbi.ac.ke', 'kips137'],
        'Ogutu': ['H31/1290/1298', 'Livingstone Ogutu', 'livi@students.uonbi.ac.ke', 'rockofages'],
        'Rynah': ['H31/24664/2017', 'Rynah Aluvisi', 'rynah@students.uonbi.ac.ke', 'mumbai'],
        'Too': ['H31/1267/1098', 'Holida Too', 'holi@students.uonbi.ac.ke', 'itsaholiday'],
        'Marie': ['H31/6235/2017', 'Marie Korie', 'marie@students.uonbi.ac.ke', 'mariempoa'],
        'Panthre': ['H31/2156/4879', 'Jagavan Panthre', 'panthre@students.uonbi.ac.ke', 'kalasingha'],
        'Rama': ['H31/2015/2364', 'Rama Njoki', 'rama@students.uonbi.ac.ke', 'rampapapam']
    }

    df = pd.read_csv(r'C:\Users\limzy\Downloads\AMSUN TEXAS AGREEMENT.csv')
    count = 0
    
    rng = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    p1 = [0.15, 0.09, 0.09, 0.05, 0.1, 0.06, 0.03, 0.1, 0.02, 0.02, 0.04, 0.06, 0.04, 0.01, 0.02, 0.01, 0.05, 0.02, 0.01, 0.03]
    p2 = []
    
    for index, row in df.iterrows():
        if count < 100:
            user = {
                'reg_num': f'H31/{random.randint(2000, 3000)}/2023',
                'name': row['Name'],
                'email': row['EMAIL ADDRESSES (GMAIL)'],
                'password': f'{random.randint(100, 1000000)}',
                'first_choice': int(np.random.choice(rng, p=p1)),
                'second_choice': int(np.random.choice(rng))
            }
            # user_json = json.dumps(user)
            user = models.Users(**user)
            users.register_user(data=user, db=db)
            count += 1
        else:
            break
    
    return 'Successfully created all users!'

@router.post('/hosps/', status_code=status.HTTP_201_CREATED)
def build_hosps(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # verify the user is an admin
    oauth2.verify_admin(current_user)

    hosp_list = {
        "KNH": ["Kenyatta National Hospital", "Nairobi", "47", 9],
        "MTRH": ['Moi Teaching & Referral Hospital', 'Uasin Gishu', '27', 8],
        'NPGH': ['Nakuru Provincial General Hospital', 'Nakuru', '32', 7],
        'CGRH': ['Coast General Referral Hospital', 'Mombasa', '1', 7],
        'KRH': ['Kiambu County Referral Hospital', 'Kiambu', '22', 9],
        'Mbagathi': ['Mbagathi Hospital', 'Nairobi', '47', 6],
        'Kach': ['Kakamega County Referral Hospital', 'Kakamega', '37', 7],
        'Mama': ['Mama Lucy Kibaki Hospital', 'Nairobi', '47', 5],
        'Vih': ['Vihiga County Referral Hospital', 'Vihiga', '38', 2],
        'Chuka': ['Chuka County Hospital', 'Tharaka-Nithi', '13', 3],
        'Jara': ['Jaramogi Oginga Odinga Hospital', 'Kisumu', '42', 7],
        'Mach': ['Machakos County Referral Hospital', 'Machakos', '16', 6],
        'Mak': ['Makueni County Referral Hospital', 'Makueni', '17', 3],
        'Gar': ['Garissa County Referral Hospital', 'Garissa', '7', 3],
        'Bar': ['Baringo County Referral Hspital', 'Baringo', '30', 3],
        'Port': ['Port-Reitz Sub-County Hospital', 'Mombasa', '1', 2],
        'Kap': ['Kapsabet County Referral Hospital', 'Nandi', '29', 5],
        'Hom': ['Homa Bay County Referral Hospital', 'Homa Bay', '43', 3],
        'Mig': ['Migori County Referral Hospital', 'Migori', '44', 2],
        'Kis': ['Kisii Teaching And Referral Hospital', 'Kisii', '45', 4]
    }

    for _, v in hosp_list.items():
        hosp_data = {
            'name': v[0],
            'county_name': v[1],
            'county_num': v[2],
            'slots': v[3]
        }

        hospital = models.Hospital(**hosp_data)

        hosp.add_hospital(hosp_data=hospital, db=db, current_user=current_user)
    return 'Successfully built all hospitals!'

