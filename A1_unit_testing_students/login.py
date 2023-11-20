import json

#Login as a user
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")
    #Look for user in database
    with open('users.json', "rw") as file:
        data = json.load(file)
        found_user = False
        for entry in data:
            if entry["username"] == username:
                found_user = True
                if entry["password"] == password:
                    print("Successfully logged in")
                    return {"username": entry["username"], "wallet": entry["wallet"] }
        if not found_user:
            answer = input("Do you want to create a new user with the username \"" + username + "\"?[Yes/No]")
            if answer == "Yes":
                new_password = input("Enter the password you want to use:")
                if valid_password(new_password):
                    #new entry
                    new_user = {"username": username, "password": new_password, "wallet": 0}
                    data.append(new_user)
                    file.write(data)
                    
        print("Either username or password were incorrect")
        return None

def valid_password(password):
    if len(password < 8):
        return False
    has_upper = any(char.isupper() for char in password)
    has_special = any(not char.isalnum() for char in password)
    return has_upper and has_special
    