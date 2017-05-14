import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
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
UPLOAD_URL = 'https://moodle.reed.edu/repository/repository_ajax.php?action=upload'
TITLE = r"MATH 389 3-20-17.pdf"
FILENAME = r"/home/mark/classes/moodle-notetaking-uploader/MATH 389 3-20-17.pdf"

def regex_for_string(string):
    reg = re.compile(string)
    def tmp(string_to_search):
        return reg.search(str(string_to_search))
    return tmp
# repo_id 4 seems to correspond with "upload a file", look at "sortorder":4
with open(FILENAME, 'rb') as f:
    s = requests.Session()
    moodle_page_load = s.get(SUBMIT_URL)
    # Removing above breaks this, not sure why
    login_query = s.post(LOGIN_URL, data=CREDENTIALS)
    second_moodle_page_load = s.get(SUBMIT_URL)
    text = second_moodle_page_load.content.decode()
    sess_key = SESS_KEY_RE.search(text).group(1)
    sess_search = regex_for_string(sess_key)
    item_id = ITEM_ID_RE.search(text).group(1)
    author = AUTHOR_RE.search(text).group(1)
    ctx_id = CTX_RE.search(text).group(1)
    client_id = CLIENT_ID_RE.search(text).group(1)
    draft_header = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    draft_files_payload = MultipartEncoder(fields = (("sesskey", sess_key), ("client_id", client_id),
                           ("filepath", "/"), ("itemid", item_id)))
    file_payload = {"file": ("repo_upload_file", f, "application/pdf")}
    data_payload = {"sesskey": sess_key, "repo_id": "4", "itemid": item_id,
                    "author": author, "savepath": "/", "title": TITLE,
                    "ctx_id": ctx_id}
    draft_query = s.post(DRAFT_FILES_URL, data=draft_files_payload,headers = draft_header)
    upload_query = s.post(UPLOAD_URL, files=file_payload, data=data_payload)
