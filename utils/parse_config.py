import yaml
import logging


def set_logger(file_name, level):
    logging.basicConfig(filename=file_name, filemode="w", level=logging.getLevelName(level),
                        format='%(asctime)s %(levelname)s %(message)s')
    return logging.getLogger(__name__)


def get_configurations(logger):
    config = {}
    with open("configurations.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            logger.debug(config)
        except yaml.YAMLError as exc:
            logger.exception(f"error parsing configurations file - {exc}")
    return config


def validate_configurations(cofig_data):
    return True
