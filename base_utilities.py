import logging
import os

def setup_logging():
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'debug.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def logMessage(message_to_log):
    # Set up logging
    setup_logging()

    # Example usage
    logging.debug(message_to_log)
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')

