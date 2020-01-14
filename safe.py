#this is the modules used in the console app
import sqlite3
import base64
import imageio
import cv2
from hashlib import sha256

#here is the set username and password for login
username = "test"
password = "Datait2020!"

#this will set the input to a variable 
connect = raw_input("What is your username? ")
connectps = raw_input("What is your password? ")

#this is used to check if the connect and the connectps match the set username and password
while (connectps != password) and (connect != username):
    #this will show again if the information over dosnt match 
    connectps = raw_input("Username or password is wrong! try again: ")
    #this is used if the user wants to stop the while loop of the login with break
    if connectps == "q":
        break

#this is the function used for creating the password it will make a 15 number/letter long random encrpyted number 
def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

#this is used for the hex key for randoming the numbers
def hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

#this is used when u want to get the selected password in the database folder 
def get_password(admin_pass, service):
    secret_key = hex_key(admin_pass, service)
    cursor = connps.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

#this will insert the password into the database and will use the hex_key as a generator for the numbers
def add_password(service, admin_pass):
    secret_key = hex_key(admin_pass, service)
    #this is the sql command that will pass the pass_key into the database
    commandps = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')        
    #this is used the execute and commit all changes
    connps.execute(commandps)
    connps.commit()
    #this will then return the create random encryped password
    return create_password(secret_key, service, admin_pass)

#this check if the connect and connectps is the same as the username and password variablex
if (connect == username) and (connectps == password):
    print("\n---- Welcome to the hidden stored service ----")
    #here we create a connection to to both of the database files
    conn = sqlite3.connect('mysafe.db')
    connps = sqlite3.connect('pass_manager.db')
    try:
        #both is the sql command used for creating the db file one for files and one for passwords
        conn.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        
        connps.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        
        print("Your safe has been created!\nWhat would you like to do?")
    except:
        print("You already have a safe, what would you like to do?")
    
    #this while loop will start if everything over has been true 
    while True:
        print("\n" + "-" * 25)
        print("Commands:")
        print("o = open file")
        print("s = store file")
        print("a = available file types")
        print("gp = get password")
        print("sp = store password")
        print("q = quit program")
        print("-" * 25)
        
        #this is used to assignt the input to a variable
        input_ = raw_input(":")

        #this just break the loop if the user input q
        if input_ == "q":
            break

        #this is here if the user want to see all files available 
        if input_ == "a":
            print("\ntxt, py, jpeg, png, jpg")

        #this is used the check for files saved in the database file
        if input_ == "o":
            #these will take the file type and the file name
            file_type = raw_input("What is the filetype of the file you want to open?\n")
            file_name = raw_input("What is the name of the file you want to open?\n")
            #this added the file name and type to a variable
            FILE_ = file_name + "." + file_type

            #this will excute the sql command and search the file
            cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')

            #this is the filter foreach used for the opening of the database file 
            file_string = ""
            for row in cursor:
                file_string = row[3]
            with open(FILE_, 'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))
         
        #this is used to save the passwrod useing the add_password function
        if input_ == "sp":
            service = raw_input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password created:\n" + add_password(service, password))
        
        #this is the get password and use the get_password function 
        if input_ == "gp":
            service = raw_input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password:\n"+get_password(password, service))
         
        #this is used for the sotring of the file 
        if input_ == "s":
            PATH = raw_input("Type in the full path to the file you want to store.\nExample: /Users/mathiasvristbramstorp/Desktop/file.py\n")
             
            #this is all the files that can be used (more can be added)
            FILE_TYPES = {
                "txt": "TEXT",
                "py": "TEXT",
                "jpg": "IMAGE",
                "png": "IMAGE",
                "jpeg": "IMAGE"
            }
            
            #this will take the name set of the file and set it with the path given and then split (splits string into a list)
            file_name = PATH.split("/")
            file_name = file_name[len(file_name) - 1]
            file_string = ""
             
            #here we asign the file_name to name and take the first name in the list 
            NAME = file_name.split(".")[0]
            #and here we take the the second object in the file_name list 
            EXTENSION = file_name.split(".")[1]

            try:
                #this is just used to take the file type into the extension var
                EXTENSION = FILE_TYPES[EXTENSION] 
            except:
                Exception()

            #the extension hold the file type and will save it with path under if the file type is a picture
            if EXTENSION == "IMAGE":
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode()
             
            #this is used if the the filetype is a text form file 
            elif EXTENSION == "TEXT":
                file_string = open(PATH, "r").read()
                file_string = base64.b64encode(file_string)

            EXTENSION = file_name.split(".")[1]
            
            #this command saved every value and variable we assignt for files and uses sql commands to insert all the data intro the file
            command = 'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' %('"' + file_name +'"', '"' + NAME +'"', '"' + EXTENSION +'"', '"' + file_string +'"')
            
            #this will execute and comit everty sql comand and save it intro the database file.
            conn.execute(command)
            conn.commit()