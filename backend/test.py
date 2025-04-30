import requests
import datetime
import pprint as pp
from werkzeug.security import check_password_hash

BASE = 'http://127.0.0.1:5000'

about_section_data = {
    'paragraph1': 'i am an postgrad student.',
    'paragraph2': 'i develop mobile apps.',
    'skills_intro': 'i am skilled in UI/UX design.'

}
response = requests.post(url=BASE + '/about_section/', json=about_section_data)
print(response.text)


