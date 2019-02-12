import json
import pandas as pd
import urllib.request


def open_user_data(username, offline=False):
    if offline == False:
        try:
            print("Fetching JSON data from server...")
            with urllib.request.urlopen("http://www.duolingo.com/users/" + username) as url:
                user_data = json.loads(url.read().decode())

        except Exception as exception:
            print(exception)

        return user_data
    else:
        with open("/home/owen/Documents/Computer Science/Duolingo CS/Kazutadashi.json") as offline_file:
            testing_file = json.load(offline_file)
            return testing_file


def create_word_dict(username):

    profile_data = open_user_data(username)
    language     = list(profile_data['language_data'].keys())[0]
    skills_data  = profile_data["language_data"][language]["skills"]

    word_dict = {}

    for skill_number in range(0, len(skills_data)):
        word_dict[skills_data[skill_number]["title"]] = skills_data[skill_number]["words"]

    return word_dict


def create_words_csv(dictionary):
    word_list_DataFrame = pd.DataFrame.from_dict(dictionary, orient='index')
    path_verified = False

    print(r"Please enter the path you would like to save this file. (eg. C:\Users\...)")

    while path_verified == False:
        user_path = input("Enter path: ")

        if (user_path[-1] != "\\") and (user_path[-1] != "/"):
            print(r"Invalid file path, please verify that you have a path ending with a / or a \ character.")
        else:
            path_verified = True

    try:
        desired_file_name = input("Enter the desired filename (the .csv will be added automatically): ")
        word_list_DataFrame.to_csv(user_path + desired_file_name + ".csv")
        print("Saved file to: " + user_path + desired_file_name + ".csv")

    except Exception as exception:
        print(exception)

def main():

    username = input("Please enter the username you would like to retrieve data from: ")
    create_words_csv(create_word_dict(username))

main()
