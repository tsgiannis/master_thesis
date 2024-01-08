#https://hackersandslackers.com/simplify-your-python-projects-configuration/
import toml
import os
# instantiate
# Read local `config.toml` file.
def load_config():
    config = toml.load(os.path.join('resources','config.toml'))#'resources\\config.toml')
    #print(config)

    #Datasets
    datasets = config['datasets']
    #language_models
    language_models = config['language_models']
    #deep learning classifiers
    classifiers = config['Deep Learning classifier']
        #Sections
    ipcs = config['IPC level']
    single_multi = config['Single_Multi_label']
    return datasets,language_models,classifiers,ipcs,single_multi
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

def get_value_out_of_list_of_dicts(inputlist,dict_key):

        # Initialize a variable to store the 'keywords' value
        keywords_value = None

        # Iterate through each dictionary in the list
        for input_dict in inputlist:
            # Check if 'keywords' is a key in the current dictionary
            if dict_key in input_dict:
                # Retrieve the value associated with the 'keywords' key
                keywords_value = input_dict[dict_key]
                break  # Exit the loop once 'keywords' is found

        return keywords_value

def replace_dictionary_value(inputlist, dict_key,new_value):
    # Iterate through each dictionary in the list
    for input_dict in inputlist:
        # Check if 'keywords' is a key in the current dictionary
        if dict_key in input_dict:
            # Replace the value associated with the 'keywords' key
            input_dict[dict_key] = new_value
            break  # Exit the loop once 'keywords' is found
    return inputlist
if __name__ == '__main__':
    #load_config()
    a,b,c = load_config()
    print(a)