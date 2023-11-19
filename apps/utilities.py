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

if __name__ == '__main__':
    #load_config()
    a,b,c = load_config()
    print(a)