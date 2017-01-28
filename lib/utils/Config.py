from lib.utils.Log import Log

def check(config,mission):
    log = Log(__name__)
    # Check whether we have that setting name
    keys = ["Connector-threads","Connector"]
    for key,value in config.iteritems():
        if key not in keys:
            log.error(key + " -> this option is not supported")
    # Check for relation

    # Set default setting
    default_value = {
        "Connector-threads" : 5
    }
    for key,value in default_value.iteritems():
        if key not in config:
            config[key] = value
