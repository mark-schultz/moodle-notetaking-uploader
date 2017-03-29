import requests
import http.client
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

AUTHOR = "Mark Schultz"
CREDENTIALS = {'login': 'schultzm', 'password': '0ZsRPH0K7mEo'}
LOGIN_URL = 'https://weblogin.reed.edu/'
SUBMIT_URL = 'https://moodle.reed.edu/mod/data/edit.php?d=485'
submit_url = 'https://moodle.reed.edu/repository/repository_ajax.php?action=upload'
TITLE = r"MATH 389 3-20-17.pdf"
FILENAME = r"/home/mark/classes/moodle-notetaking-uploader/MATH 389 3-20-17.pdf"


with open(FILENAME, 'rb') as f:
    file_payload = {"file": ("repo_upload_file", f, "application/pdf")}
    data_payload = {"repo_id": "4", "author": AUTHOR,
                    "title": TITLE, "ctx_id": "69355", 'savepath': '/'}
    s = requests.Session()
    s.get(SUBMIT_URL)
    r = s.post(LOGIN_URL, data=CREDENTIALS)
    l = s.get(submit_url)
    q = s.post(submit_url, files=file_payload, data=data_payload)
