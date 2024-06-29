import logging
import os

def setup_logging(log_level=logging.INFO, script_name=os.path.basename(__file__)):
    """
    Sets up logging for the application.

    Args:
        log_level (int): The logging level. Defaults to logging.INFO.
                        [can be logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        script_name (str): The name of the script. Defaults to None, in which case it will use the name of the calling script.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    if script_name is None:
        # Get the calling script's name if not provided
        script_name = os.path.basename(__file__)
    
    logger = logging.getLogger(script_name)
    logger.setLevel(log_level)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    if not logger.handlers:
        logger.addHandler(ch)

    return logger