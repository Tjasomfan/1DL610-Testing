import json
from edit_user import edit_user

#Login as a user
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")
    #Look for user in database
    data = None
    found_user = False
    with open('users.json', "r") as file:
        data = json.load(file)
        for entry in data:
            if entry["username"] == username:
                found_user = True
                if entry["password"] == password:
                    print("Successfully logged in")
                    return {"username": entry["username"], "wallet": entry["wallet"] }
        if found_user:
            print("Either username or password were incorrect")
            return None
    
    user = None
    if not data == None:
        with open('users.json', "w") as file:
            if not found_user:
                answer = input("Do you want to create a new user with the username \"" + username + "\"?[Yes/No]")
                if answer == "Yes":
                    new_password = input("Enter the password you want to use:")
                    if valid_password(new_password):
                        new_user = {"username": username, "password": new_password, "wallet": 0}
                        data.append(new_user)
                        file.write(json.dumps(data, indent=4))
                        
                        print("New user was created!")
                        user = {"username": username, "wallet": 0}
    if user != None:
        edit_user(user)
        return user
    return None

def valid_password(password):
    if len(password) < 8:
        return False
    has_upper = any(char.isupper() for char in password)
    has_special = any(not char.isalnum() for char in password)
    return has_upper and has_special
