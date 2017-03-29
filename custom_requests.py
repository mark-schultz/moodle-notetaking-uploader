import requests
import http.client
from credentials import CREDENTIALS
import re
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# Regex patterns here
SESS_KEY_RE = re.compile(r"\"sesskey\":\"(\w*)\"")
ITEM_ID_RE = re.compile(r"\"itemid\":(\d*),")
AUTHOR_RE = re.compile(r"\"author\":\"([^\"]+)\"")
CTX_RE = re.compile(r";ctx_id=(\d+)&amp;")
CLIENT_ID_RE = re.compile(r"\"client_id\":\"(\w*)\"")
##

LOGIN_URL = 'https://weblogin.reed.edu/'
SUBMIT_URL = 'https://moodle.reed.edu/mod/data/edit.php?d=485'
DRAFT_FILES_URL = 'https://moodle.reed.edu/repository/draftfiles_ajax.php?action=list'
submit_url = 'https://moodle.reed.edu/repository/repository_ajax.php?action=upload'
TITLE = r"MATH 389 3-20-17.pdf"
FILENAME = r"/home/mark/classes/moodle-notetaking-uploader/MATH 389 3-20-17.pdf"


# repo_id 4 seems to correspond with "upload a file", look at "sortorder":4
with open(FILENAME, 'rb') as f:
    s = requests.Session()
    s.get(SUBMIT_URL)
    # Removing above breaks this, not sure why
    r = s.post(LOGIN_URL, data=CREDENTIALS)
    l = s.get(SUBMIT_URL)
    text = l.content.decode()
    sess_key = SESS_KEY_RE.search(text).group(1)
    item_id = ITEM_ID_RE.search(text).group(1)
    author = AUTHOR_RE.search(text).group(1)
    ctx_id = CTX_RE.search(text).group(1)
    client_id = CLIENT_ID_RE.search(text).group(1)
    draft_files_payload = {"sesskey": sess_key, "client_id": client_id,
                           "filepath": "/", "itemid": item_id}
    file_payload = {"file": ("repo_upload_file", f, "application/pdf")}
    data_payload = {"sesskey": sess_key, "repo_id": "4", "itemid": item_id,
                    "author": author, "savepath": "/", "title": TITLE,
                    "ctx_id": ctx_id}
    a = s.post(DRAFT_FILES_URL, json=draft_files_payload)
    b = s.post(submit_url, files=file_payload, data=data_payload)
