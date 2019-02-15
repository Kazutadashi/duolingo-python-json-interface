import json
import pandas as pd
import urllib.request
import os


def open_user_data_from_web(username, offline=False):
    """
    Opens user data based on their username.

    Opens up a request to http://www.duolingo.com/users/USERNAME
    where the USERNAME is entered by the user.

    Parameters
    ----------
    username : username
       Case sensitve and symbol sensitive username used to request JSON file.

    Returns
    -------
    dict
       Returns the JSON file decoded as a python dictionary for data manipulation.

    """
    try:
        print("Fetching JSON data from server...")
        with urllib.request.urlopen("http://www.duolingo.com/users/" + username) as url:
            user_data = json.loads(url.read().decode())

    except Exception as exception:
        print(exception)

    return user_data


def create_word_dict(online=True, path=None, username=None):
    """
    Creates a dictionary of words.

    Creates a dictionary with all of the words as values, and their respective
    lessons as keys

    Parameters
    ----------
    online
        Used to determine if we are going to load a file, or download one from the internet

    Returns
    -------
    word_dict
        A dictionary with lesson titles as keys and words as values

    """
    if online == True:
        profile_data = open_user_data_from_web(username)

    else:
        profile_data_raw = open(path).read()
        profile_data = json.loads(profile_data_raw)

    # Gathers the language code to move through the dictionary based off the username
    language = list(profile_data['language_data'].keys())[0]

    # Loads all lessons and their values
    skills_data = profile_data["language_data"][language]["skills"]

    word_dict = {}

    # Creates the key, and fills the values
    for skill_number in range(0, len(skills_data)):
        word_dict[skills_data[skill_number]["title"]] = skills_data[skill_number]["words"]

    return word_dict


def create_words_csv(dictionary):
    """
    Exports a csv file with titles and words

    Uses a dictionary of words and titles to export a nicely formatted csv file for use with other
    software

    Parameters
    ----------
    dictionary
        A dictionary containing titles as keys and words as values

    Returns
    -------
    None
        Does not return a value, only saves a csv file to disk

    """
    word_list_DataFrame = pd.DataFrame.from_dict(dictionary, orient='index')
    path_verified = False

    print(r"Please enter the path you would like to save this file. (eg. C:\Users\...)")

    while path_verified == False:
        user_path = input("Enter path: ")

        # If the user does not end with a slash or backspace, it will be located somewhere unexpected.
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
    """
    Gets the language code for user's current language

    Parameters
    ----------
    json_file
        Takes a JSON file for the Duolingo JSON file of the user

    Returns
    -------
    string
        Returns the language code as a 2 character string

    """
    return list(json_file['language_data'].keys())[0]


def get_language_name(json_file):
    """
    Gets the full name of the language the user is currently studying

    Parameters
    ----------
    json_file
        Takes a JSON file for the Duolingo JSON file of the user

    Returns
    -------
    string
        Returns the full name of the language

    """
    return json_file['language_data'][get_language_code(json_file)]['language_string']


def get_number_of_skills(json_file):
    """
    Gets the number of skills in the tree the user is currently in

    Parameters
    ----------
    json_file
        Takes a JSON file for the Duolingo JSON file of the user

    Returns
    -------
    int
        Returns an integer with the number of skills

    """
    return len(json_file['language_data'][get_language_code(json_file)]['skills'])


def get_number_of_lessons(json_file):
    """
    Gets the number of lessons in the tree the user is currently in

    Parameters
    ----------
    json_file
        Takes a JSON file for the Duolingo JSON file of the user

    Returns
    -------
    int
        Returns an integer with the number of lessons

    """
    total_lessons = 0

    for i in range(0, get_number_of_skills(json_file)):
        total_lessons += json_file['language_data'][get_language_code(json_file)]['skills'][i]['num_lessons']

    return total_lessons


def get_number_of_lexemes(json_file):
    """
    Gets the total number of lexemes in the tree the user is currently in

    Parameters
    ----------
    json_file
        Takes a JSON file for the Duolingo JSON file of the user

    Returns
    -------
    int
        Returns the number of lexemes

    """
    total_lexemes = 0

    for i in range(0, get_number_of_skills(json_file)):
        total_lexemes += json_file['language_data'][get_language_code(json_file)]['skills'][i]['num_lexemes']

    return total_lexemes


def load_data(language, path):
    """
    Loads the JSON file of the current language

    Loads the JSOn file of the current tree the user is studying, using
    the path provided and the title of the language for naming conventions
    of the new JSON file

    Parameters
    ----------
    language
        The title of the language

    Returns
    -------
    JSON File
        Returns the loaded JSON file

    """
    with open(path + language + ".json") as offline_file:
        current_file = json.load(offline_file)
        return current_file


def get_language_list(path):
    """
    Gets the list of titles from a directory

    Gets the list of titles from a directory, assuming that all files in the directory
    are only the JSON files that were created. This should only be used if the JSON file
    directory is clean and has correct formatting

    Parameters
    ----------
    path
        Path to the JSON file list directory

    Returns
    -------
    list
        A list of all of the languages found in the directory

    """
    language_list = []

    for language in os.listdir(path):

        # Removes the JSON file extension
        language_list.append(language[0:len(language)-5])

    return language_list

def make_dict_all_lessons(list_of_languages, path):
    """
    Makes a dictionary of all lessons

    Makes a dictionary for every language, showing the language as the key,
    and the number of lessons for that language as the value

    Parameters
    ----------
    list_of_languages
        The list of all the language names

    path
        The path to the local language JSON files

    Returns
    -------
    language_lesson_dict
        The dictionary of languages to lessons


    """
    language_lesson_dict = {}

    for lang in list_of_languages:

        # Sets the current language to the language in the list
        language = lang

        language_file = load_data(language, path)
        language_lesson_dict[lang] = get_number_of_lessons(language_file)

    return language_lesson_dict

def make_dict_all_skills(list_of_languages, path):
    """
    Makes a dictionary of all skills

    Makes a dictionary for every language, showing the language as the key,
    and the number of skills for that language as the value

    Parameters
    ----------
    list_of_languages
        The list of all the language names

    path
        The path to the local language JSON files

    Returns
    -------
    language_skills_dict
        The dictionary of languages to skills


    """
    language_skills_dict = {}

    for lang in list_of_languages:

        # Sets the current language to the language in the list
        language = lang

        language_file = load_data(language, path)
        language_skills_dict[lang] = get_number_of_skills(language_file)

    return language_skills_dict


def get_word_count_dict(path):
    """
    Makes a dictionary of the number of words in each tree

    Makes a dictionary of the number of words in each tree. It uses the language name
    as the key, and the number of words in each language as the value

    Parameters
    ----------
    path
        The path to the local language JSON files. This is used to loop through
        all json files in a directory, to generate a key and value for each

    Returns
    -------
    languages_and_word_count
        The dictionary of all languages and their word count


    """

    languages_and_word_count = {}
    languages = get_language_list(path)

    # For each language, create a key with the title and then loops over each json file to
    # extract the number of words per tree

    for i in range(0, len(languages)):
        language = languages[i]
        word_dict = create_word_dict(online=False, path=path + language + ".json")

        sum = 0
        for values in word_dict.values():
            sum += len(values)

        languages_and_word_count[language] = sum

    return languages_and_word_count



