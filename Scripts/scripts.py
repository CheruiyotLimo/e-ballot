import re


def email_verifier(email: str):
    """ Ascertain that the email is a verified school email address. """

    pattern = r'@students\.uonbi\.ac\.ke$'
    
    if re.search(pattern, email):
        return True
    


