#https://hackersandslackers.com/simplify-your-python-projects-configuration/
import toml
import os
from functools import wraps
from flask import  session
# instantiate
# Read local `config.toml` file.
ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def read_naming():
    list_of_variables = []

    filepath =os.path.join(ROOT_DIRECTORY,'resources','naming.txt')
    with open(filepath, 'r', encoding='utf-8') as file_obj:
        for line in file_obj:
            line = line.strip()
            # if not line.startswith('#') :
            #     print(line)
            if  '#' in line:
                # Take only the part left of #
                line = line.split('#')[0].strip()
            else:
                list_of_variables.append(line)
    return list_of_variables

list_of_default_variables = read_naming()

def load_config():
    config = toml.load(os.path.join('resources','config.toml'))#'resources\\config.toml')


    #Machine Learning Methods
    methods = config['methods']

    #Language Models
    languagemodels = config['languagemodels']

    #Sections
    datasets = config['datasets']

    #IPC Levels
    ipclevels = config['ipclevels']

    #noofwords
    noofwords = config['noofwords']

    #Single /  Multi Lables
    singlemulti = config['singlemulti']

    # structure
    structures = config['structure']

    # ensemble
    ensemble = config['ensemble']

    return methods,languagemodels,datasets,ipclevels,noofwords,singlemulti,structures,ensemble
    # Retrieving a value
    #config['project']['author']
    #config.get('project').get('author')


def contains_list_recursive(data):
    if isinstance(data, list):
        return any(contains_list_recursive(item) for item in data)
    elif isinstance(data, dict):
        return any(isinstance(value, list) or contains_list_recursive(value) for value in data.values())
    else:
        return False

def get_element_by_value(lst, key_name, target_value):
    for element in lst:
        if key_name in element and element[key_name] == target_value:
            return element
    return None  # Return None if key or value not found in any dictionary


def find_default_folder(directory):
    default_folder = None
    first_folder = None

    # List all directories in the specified directory
    directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    suffix = '.default'
    # Loop through the directories
    for d in directories:
        if d.endswith(suffix):
            # If a folder with ".default" suffix is found, assign it to default_folder and break the loop
            default_folder = d[:-len(suffix)]
            break
        elif first_folder is None:
            # Assign the first encountered folder to first_folder
            first_folder = d

    # Return default_folder if found, otherwise return the first encountered folder
    return default_folder if default_folder else first_folder


def get_value_at_index(string, index):
    # Split the string by underscore
    parts = string.split('_')

    # Check if the index is valid
    if index >= 0 and index < len(parts):
        return parts[index]
    else:
        return None

def get_value_out_of_list_of_dicts(inputlist,dict_key):
        found = False
        # Initialize a variable to store the 'keywords' value
        keywords_value = None

        try:
            default_folder = find_default_folder(os.path.join(ROOT_DIRECTORY,'resources'))
        except:
            print('error')
        # Iterate through each dictionary in the list
        for input_dict in inputlist:
            # Check if 'keywords' is a key in the current dictionary
            if dict_key in input_dict:
                # Retrieve the value associated with the 'keywords' key
                dict_value = input_dict[dict_key]
                found = True
                break  # Exit the loop once 'keywords' is found
        if not found :
            position = list_of_default_variables.index(dict_key)
            dict_value =get_value_at_index(default_folder,position)
        return dict_value

def replace_dictionary_value(inputlist, dict_key,new_value):
    # Iterate through each dictionary in the list
    for input_dict in inputlist:
        # Check if 'keywords' is a key in the current dictionary
        if dict_key in input_dict:
            # Replace the value associated with the 'keywords' key
            input_dict[dict_key] = new_value
            break  # Exit the loop once 'keywords' is found
    return inputlist


def custom_dict_counter(dictionary):
    elements_keys = 0

    for key, value in dictionary.items():
        elements_keys +=  1
        sub_key = bool(False)

        if isinstance(value, list):
            for value_item in  value:
                for key, value in value_item.items():
                    if isinstance(value,list):
                        if not sub_key :
                            elements_keys += 1
                            sub_key = bool(True)
    return elements_keys




# Custom decorator to read the contents of a directory
def read_directory(directory_name):
    def decorator(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            list_directories = []
            config = toml.load(os.path.join('resources', 'config.toml'))  # 'resources\\config.toml')
            elements_count  = custom_dict_counter(config)
            # Construct the directory path based on the operating system
            ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            directory_path = os.path.join(ROOT_DIRECTORY, directory_name)

            # Read the contents of the specified directory
            directory_contents = os.listdir(directory_path)
            for item in directory_contents:
                if os.path.isdir(os.path.join(directory_path,item)):
                    split_result = item.split('_')
                    if len(split_result) == elements_count :
                        list_directories.append(item)
                # Call the original view function with the directory contents
            #dismember the directory names according to the preagreed naming
            if len(list_directories) >0 :
                methods = [item.split('_')[0] for item in list_directories]
                languagemodels = [item.split('_')[1] for item in list_directories]
                datasets =  [item.split('_')[2] for item in list_directories]
                ipclevels = [item.split('_')[3] for item in list_directories]
                sections = [item.split('_')[4] for item in list_directories]
                noofwords = [int(item.split('_')[5]) for item in list_directories]
                singlemulti = [item.split('_')[6] for item in list_directories]
                structure = [item.split('_')[7] for item in list_directories]
                ensemble = [item.split('_')[8] for item in list_directories]
                #Populate session elements
                session['dynamic.methods'] = list(set(methods))
                session['dynamic.languagemodels'] =list(set(languagemodels))
                session['dynamic.datasets'] = list(set(datasets))
                session['dynamic.ipclevels'] = list(set(ipclevels))
                session['dynamic.sections'] = list(set(sections))
                session['dynamic.noofwords'] = list(set(noofwords))
                session['dynamic.singlemulti'] = list(set(singlemulti))
                session['dynamic.structures'] = list(set(structure))
                session['dynamic.ensemble'] = list(set(ensemble))

            return view_func(*args, **kwargs)

        return decorated_view

    return decorator


def get_value_for_key_in_list_of_dictionaries(list_of_dictionaries,key,target_value):
    result_dict = None
    for d in list_of_dictionaries:
        if key in d and d[key].lower() == target_value:
            result_dict = d
            break
    return d['sections']





