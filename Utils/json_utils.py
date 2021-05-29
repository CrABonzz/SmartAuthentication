import json

from Utils.common import MAX_FAILED_LOGIN_ATTEMPTS


def add_new_user(new_user):
    with open(r"assets\users.json", "r+") as users_file:
        all_users = json.load(users_file)

        all_users["users"].append(new_user)

        users_file.seek(0)
        users_file.truncate()
        json.dump(all_users, users_file)


def update_failed_login(username, email):
    failed_login_attempts = 0
    with open(r"assets\users.json", "r+") as users_file:
        all_users = json.load(users_file)

        for i, user in enumerate(all_users["users"]):
            if user['user'] == username and user['email'] == email:
                failed_login_attempts = user["count_failed_tries"] + 1
                user["count_failed_tries"] = failed_login_attempts
                all_users["users"][i] = user

                if failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
                    user["blocked"] = True
                    all_users["users"][i] = user

        users_file.seek(0)
        users_file.truncate()
        json.dump(all_users, users_file)

    return failed_login_attempts
