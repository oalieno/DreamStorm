import urllib

from lib.utils.Log import Log

def check(config,missions):
    log = Log(__name__)
    '''
    Checking Config
    '''
    config_keys = ["Connector-threads","Connector-tor","Connector-tor-password"]
    config_default = {
        "Connector-threads" : 5,
        "Connector-tor" : True
    }

    # Check whether we have that setting name
    for key,value in config.iteritems():
        if key not in (config_keys + mission_keys):
            log.error("In config.json" + key + " -> this option is not supported")


    # Set default setting
    for key,value in config_default.iteritems():
        if key not in config:
            config[key] = value

    # Check for relation
    if config["Connector-tor"] and not config.get("Connector-tor-password"):
        log.error("In config.json : " + "You didn't provide your tor password")

    '''
    Checking Missions
    '''
    mission_keys = ["url","range","requests","mutations","fuzzing","stable-query","mutable-query","stable-header","mutable-header","stable-postdata","mutable-postdata"]
    mission_default = {
        "range" : "domain",
        "requests" : 20,
        "mutation" : 10,
        "fuzzing" : False
    }
    for mission in missions:
        # Check whether we have that setting name
        for key,value in mission.iteritems():
            if key not in mission_keys:
                log.error("In missions.json : " + key + " -> this option is not supported")

        # Set default setting
        for key,value in mission_default.iteritems():
            if key not in mission:
                mission[key] = value

        # Check for relation
        if not mission.get("url"):
            log.error("In missions.json : " + "You didn't specify your target url")

        # If you don't specify http or https in front of the url we will add "http://" for you
        if re.search("^https?://",mission['url']) == None:
            mission['url'] = "http://" + mission['url']
        mission['url'] = mission['url'].rstrip('/')

        # Compute the domain
        head = missionp['url'].find("//")
        tail = mission['url'][head+2:].find("/")
        mission['domain'] = mission['url'] if tail == -1 else mission['url'][:head+2+tail]

        # Check whether the url is valid
        try:
            response = urllib.urlopen(mission['url'])
        except KeyboardInterrupt:
            log.info("You pressed Ctrl+C")
            sys.exit(0)
        except:
            log.warning("This url is not vaild : " + mission['url'])
