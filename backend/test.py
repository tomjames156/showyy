import requests
import datetime
import pprint as pp
from werkzeug.security import check_password_hash

BASE = 'http://127.0.0.1:5000'

project_data = {
    'tool_id': 1,
    'name': 'Freelancr',
    'description': 'Potfolio Showcase'
}




response = requests.post(BASE + '/projects/', data=project_data)
print(response.text)