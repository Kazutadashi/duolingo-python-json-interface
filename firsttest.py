import json
import pandas as pd
import urllib.request
import os

def open_user_data(username):
    try:
        print("Fetching JSON data from server...")
        with urllib.request.urlopen("http://www.duolingo.com/users/" + username) as url:
            user_data = json.loads(url.read().decode())

    except Exception as exception:
        print(exception)

    return user_data



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


def get_language_code(json_file):
    return list(json_file['language_data'].keys())[0]


def get_language_name(json_file):
    return json_file['language_data'][get_language_code(json_file)]['language_string']


def get_number_of_skills(json_file):
    return len(json_file['language_data'][get_language_code(json_file)]['skills'])


def get_number_of_lessons(json_file):
    total_lessons = 0

    for i in range(0, get_number_of_skills(json_file)):
        total_lessons += json_file['language_data'][get_language_code(json_file)]['skills'][i]['num_lessons']

    return total_lessons


def get_number_of_lexemes(json_file):
    total_lexemes = 0

    for i in range(0, get_number_of_skills(json_file)):
        total_lexemes += json_file['language_data'][get_language_code(json_file)]['skills'][i]['num_lexemes']

    return total_lexemes


def load_data(language, path):
    with open(path + language + ".json") as offline_file:
        current_file = json.load(offline_file)
        return current_file


def get_language_list(path):
    language_list = []

    for language in os.listdir(path):
        language_list.append(language[0:len(language)-5])

    return language_list




def main():

    path = "/home/owen/Documents/Computer Science/Duolingo CS/All Language Json Files/"

    language = "French"
    language_file = load_data(language, path)

    print((["French"], get_number_of_lessons(language_file)))

main()
