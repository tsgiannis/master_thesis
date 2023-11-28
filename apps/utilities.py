#https://hackersandslackers.com/simplify-your-python-projects-configuration/
import toml
# instantiate
# Read local `config.toml` file.
def load_config():
    config = toml.load('resources\\config.toml')
    #print(config)

    #Datasets
    datasets = config['datasets']
    #language_models
    language_models = config['language_models']
    #deep learning classifiers
    classifiers = config['Deep Learning classifier']
        #Sections
    return datasets,language_models,classifiers
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

if __name__ == '__main__':
    #load_config()
    a,b,c = load_config()
    print(a)