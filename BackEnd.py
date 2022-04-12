import random
import string
import math
import base64
import sqlite3
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# define password class
class Password:
    def __init__(self, size, max_size, is_num_req, is_case_req, is_symbol_req, is_low_req, include_custom_char,
                 custom_string, is_whole_word, is_space):
        # initialize password properties from front-end window
        self.include_space = is_space
        self.is_whole_word = is_whole_word
        self.include_custom_char = include_custom_char
        self.custom_string = custom_string
        self.size = size
        self.max_size = max_size
        self.is_num_req = is_num_req
        self.is_case_req = is_case_req
        self.is_symbol_req = is_symbol_req
        self.is_low_req = is_low_req
        # initialize other password properties
        self.val = None
        self.chars = None
        self.safety_color = None
        self.safety = None
        self.strength = None
        self.chars_set = None
        self.setup()

        self.max_tot_chars = 10 + 52 + 32
        self.max_strength = 150

    # password class methods

    # define all password properties
    def setup(self):
        # define available chars in checkboxes selection
        if self.is_low_req:
            if self.is_symbol_req:
                if self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.digits + string.ascii_letters + string.punctuation
                        self.chars = 10 + 52 + 32
                    elif not self.is_case_req:
                        self.chars_set = string.digits + string.ascii_lowercase + string.punctuation
                        self.chars = 10 + 26 + 32
                elif not self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.ascii_letters + string.punctuation
                        self.chars = 52 + 32
                    elif not self.is_case_req:
                        self.chars_set = string.ascii_lowercase + string.punctuation
                        self.chars = 26 + 32
            elif not self.is_symbol_req:
                if self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.digits + string.ascii_letters
                        self.chars = 10 + 52
                    elif not self.is_case_req:
                        self.chars_set = string.digits + string.ascii_lowercase
                        self.chars = 10 + 26
                elif not self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.ascii_letters
                        self.chars = 52
                    elif not self.is_case_req:
                        self.chars_set = string.ascii_lowercase
                        self.chars = 26
        elif not self.is_low_req:
            if self.is_symbol_req:
                if self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.digits + string.ascii_uppercase + string.punctuation
                        self.chars = 10 + 26 + 32
                    elif not self.is_case_req:
                        self.chars_set = string.digits + string.punctuation
                        self.chars = 10 + 26 + 32
                elif not self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.ascii_uppercase + string.punctuation
                        self.chars = 26 + 32
                    elif not self.is_case_req:
                        self.chars_set = string.punctuation
                        self.chars = 32
            elif not self.is_symbol_req:
                if self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.digits + string.ascii_uppercase
                        self.chars = 10 + 36
                    elif not self.is_case_req:
                        self.chars_set = string.digits
                        self.chars = 10
                elif not self.is_num_req:
                    if self.is_case_req:
                        self.chars_set = string.ascii_uppercase
                        self.chars = 26
                    elif not self.is_case_req:
                        self.chars_set = ""
                        self.chars = 0

        self.entropy_calc(self.chars, self.size)

    def generatepsw(self):
        if self.include_custom_char:
            if self.include_space:
                pass
            elif not self.include_space:
                self.custom_string = self.custom_string.replace(' ', '')
            char1_length = len(self.custom_string)
            rand_string = self.custom_string
            aux_string = rand_string
            final_string = ""
            it_num = self.size - char1_length
            if not self.is_whole_word:
                for i in range(it_num):
                    aux_string = aux_string + "".join(random.choice(self.chars_set))
                aux_string_list = list(aux_string)
                aux_string_list = random.sample(aux_string_list, self.size)
                final_string = "".join(aux_string_list)
            elif self.is_whole_word:
                if it_num > 0:
                    for i in range(random.randint(1, it_num)):
                        aux_string = aux_string + "".join(random.choice(self.chars_set))
                    for j in range(it_num - i - 1):
                        aux_string = "".join(random.choice(self.chars_set)) + aux_string
                else:
                    pass
                final_string = aux_string
            self.val = final_string
        elif not self.include_custom_char:
            self.val = ''.join(random.choice(self.chars_set))
            for i in range(self.size - 1):
                self.val = self.val + "".join(random.choice(self.chars_set))

    def entropy_calc(self, chars, size):
        self.strength = math.floor(size * math.log2(chars))
        if self.strength < 40:
            self.safety = "Low"
            self.safety_color = 0
        elif 40 <= self.strength <= 60:
            self.safety = "Average"
            self.safety_color = 1
        elif 60 < self.strength <= 100:
            self.safety = "High"
            self.safety_color = 2
        elif self.strength > 100:
            self.safety = "Very High"
            self.safety_color = 3


def generator(passw):
    passw.setup()
    passw.generatepsw()


class DataBase:
    def __init__(self, filename, encryption):
        self.connection = None
        self.encryption = encryption
        self.filename = filename

    def openconn(self):
        self.connection = sqlite3.connect(self.filename + ".db")

    def closeconn(self):
        self.connection.close()

    def createdata(self):
        self.openconn()
        data = open(self.filename + ".db", "w")
        crsr = self.connection.cursor()
        sql_command = """CREATE TABLE DATA (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT DEFAULT '',
            username TEXT DEFAULT '',
            email TEXT DEFAULT '',
            password TEXT DEFAULT '',
            category INTEGER DEFAULT 'Misc');"""
        crsr.execute(sql_command)
        sql_command2 = "INSERT INTO DATA(Id) VALUES(1)"
        crsr.execute(sql_command2)
        self.connection.commit()
        self.closeconn()
        data.close()

    def createrow(self, Id):
        self.openconn()
        crsr = self.connection.cursor()
        sql_command = "INSERT INTO DATA(Id) VALUES(" + str(Id) + ")"
        crsr.execute(sql_command)
        self.connection.commit()
        self.closeconn()

    def deleterow(self, Id):
        self.openconn()
        crsr = self.connection.cursor()
        sql_command = "DELETE FROM DATA WHERE Id=" + str(Id) + ";"
        crsr.execute(sql_command)
        self.connection.commit()
        self.closeconn()

    def updatedata(self, Id, field, value):
        self.openconn()
        crsr = self.connection.cursor()
        if field == 0:
            sql_command = "UPDATE DATA SET name ='" + value + "' WHERE Id=" + str(Id) + ";"
        elif field == 1:
            sql_command = "UPDATE DATA SET username ='" + value + "' WHERE Id=" + str(Id) + ";"
        elif field == 2:
            sql_command = "UPDATE DATA SET email ='" + value + "' WHERE Id=" + str(Id) + ";"
        elif field == 3:
            sql_command = "UPDATE DATA SET password ='" + value + "' WHERE Id=" + str(Id) + ";"
        elif field == 4:
            sql_command = "UPDATE DATA SET category ='" + value + "' WHERE Id=" + str(Id) + ";"
        crsr.execute(sql_command)
        self.connection.commit()

    def deleteallentries(self):
        self.openconn()
        crsr = self.connection.cursor()
        sql_command = "DELETE FROM DATA;"
        crsr.execute(sql_command)
        self.connection.commit()
        self.closeconn()

    def deletedata(self, keyfilename):
        self.deleteallentries()
        os.remove(self.filename + ".db")
        os.remove(keyfilename + ".key")

    def createkey(self, masterpassword, keyfilename):
        passw = masterpassword.encode()
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256, length=32, salt=salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(passw))
        keyfile = open(keyfilename + ".key", "wb")
        keyfile.write(key)
        keyfile.close()

    def encrypt(self, keyfilename):
        self.openconn()
        with open(keyfilename + ".key", "rb") as kfile:
            key = kfile.read()
        kfile.close()
        cipher = Fernet(key)
        with open(self.filename + ".db", "rb") as d1:
            encryfile = d1.read()
        d1.close()
        with open(self.filename + ".db", "wb") as d2:
            try:
                encry_data = cipher.encrypt(encryfile)
            except:
                d2.write(encryfile)
                d2.close()
            else:
                d2.write(encry_data)
                d2.close()
        self.connection.commit()
        self.closeconn()
        self.encryption = True
        return self.encryption

    def decrypt(self, keyfilename):
        self.openconn()
        with open(keyfilename + ".key", "rb") as kfile:
            key = kfile.read()
        kfile.close()
        cipher = Fernet(key)
        with open(self.filename + ".db", "rb") as d1:
            encryfile = d1.read()
        d1.close()
        with open(self.filename + ".db", "wb") as d2:
            try:
                encry_data = cipher.decrypt(encryfile)
            except:
                d2.write(encryfile)
                d2.close()
            else:
                d2.write(encry_data)
                d2.close()
        self.connection.commit()
        self.closeconn()
        self.encryption = False
        return self.encryption
