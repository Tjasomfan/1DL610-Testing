import json

# Edit a users information in the user file
def edit_user(login_info):
    print("Editing user information:")
    new_user = {"username": login_info["username"], "password": "", "wallet": login_info["wallet"], "address": "", "phone": "", "email": "", "cards": []}

    new_user["address"] = input("Adress: ")
    new_user["phone"] = input("Phone: ")
    new_user["email"] = input("Email: ")

    while (input("Do you want to add a card? (y/n)") == 'y'):
        card = {"number" : "", "expirationdate" : "", "name" : "", "ccv" : ""}

        card["number"] = input("Card number: ")
        card["expirationdate"] = input("Card expiration date: ")
        card["name"] = input("Card name: ")
        card["ccv"] = input("Card CCV: ")
        new_user["cards"].append(card)

    replace_user('users.json', new_user)
    print("Editing user finished!")
    return new_user

def replace_user(json_file, new_user_data):
    with open(json_file, 'r') as file:
        data = json.load(file)

    target_username = new_user_data["username"]
    # Find the index of the target user
    user_index = None
    for i, user in enumerate(data):
        if user["username"] == target_username:
            user_index = i
            break

    if user_index is not None:
        # Replace the user data
        new_user_data["password"] = data[user_index]["password"]
        data[user_index] = new_user_data

        # Write the updated data back to the JSON file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)

