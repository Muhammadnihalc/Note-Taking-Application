import re
import bleach


def validate_email(email):
    email_regex = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    return bool(email_regex.match(email))

def validate_name(name):
    return re.match("^[a-zA-Z]{2,15}$", name)

def validate_password(password):
    if len(password) < 6 or len(password) > 15:
        return False
    return any(char.isupper() for char in password) and \
           any(char.islower() for char in password) and \
           any(char.isdigit() for char in password)

def validate_note_title(title):
    return len(title.strip()) > 0 and re.match("^[a-zA-Z]{1,15}$", title)

def validate_note_text(text):
    # using bleach to Sanitize input data to remove potentially malicious content or escape special characters
    sanitized_text = bleach.clean(text, strip=True)
    return len(sanitized_text.strip()) > 0

