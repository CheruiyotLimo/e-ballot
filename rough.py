import json

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

for _, v in user_list.items():
    user = {
            'reg_num': v[0],
            'name': v[1],
            'email': v[2],
            'password': v[3]
        }
    user_json = json.dumps(user)
    print(type(user_json))