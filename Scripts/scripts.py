


def email_verifier(email: str):
    """ Ascertain that the email is a verified school email address. """

    return email[-21:] == "@students.uonbi.ac.ke"