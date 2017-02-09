import re
import urllib

from lib.utils.Log import Log

def check(config,missions):
    log = Log(__name__)
    config_keys = ["Connector-threads","Connector-tor","Connector-tor-password","mode","ip","port"]
    config_default = {
        "Connector-threads" : 5,
        "Connector-tor" : True,
        "mode" : "local"
    }
    mission_setting_keys = ["url","range","requests","mutations","fuzzing"]
    mission_data_keys = ["stable-query","mutable-query","stable-header","mutable-header","stable-postdata","mutable-postdata"]
    mission_setting_default = {
        "range" : "domain",
        "requests" : 20,
        "mutation" : 10,
        "fuzzing" : False
    }
    '''
    Checking Config
    '''
    # Check whether we have that setting name
    for key,value in config.iteritems():
        if key not in (config_keys + mission_setting_keys + mission_data_keys):
            log.error("In config.json : " + key + " -> this option is not supported")


    # Set default value
    for key,value in config_default.iteritems():
        if key not in config:
            config[key] = value

    # Check for constrain
    if config["Connector-tor"] and not config.get("Connector-tor-password"):
        log.error("In config.json : " + "You didn't provide your tor password")
    if config["mode"] not in ("local","remote"):
        log.error("In config.json : " + "we don't support this mode -> " + config["mode"])
    if config["mode"] == "remote" and not config.get("ip") or not config.get("port"):
        log.error("In config.json : " + "You didn't provide your server ip and port to listen")

    '''
    Checking Missions
    '''
    for mission in missions:
        # Check whether we have that setting name
        for key,value in mission.iteritems():
            if key not in mission_setting_keys + mission_data_keys:
                log.error("In missions.json : " + key + " -> this option is not supported")

        # Set global setting value
        for key in mission_setting_keys:
            if mission.get(key) == None and config.get(key) != None:
                mission[key] = config[key]

        # Set global data value
        for key in mission_data_keys:
            if config.get(key) != None:
                if mission.get(key) != None:
                    mission[key] = dict(config[key].items() + mission[key].items())
                else:
                    mission[key] = config[key]

        # Set default setting value
        for key,value in mission_setting_default.iteritems():
            if key not in mission:
                mission[key] = value
        
        # Guarantee we have at lest a empty dictionary
        for key in mission_data_keys:
            if mission.get(key) == None:
                mission[key] = {}

        # Check for constrain
        if not mission.get("url"):
            log.error("In missions.json : " + "You didn't specify your target url")

        # If you don't specify http or https in front of the url we will add "http://" for you
        if re.search("^https?://",mission['url']) == None:
            mission['url'] = "http://" + mission['url']
        mission['url'] = mission['url'].rstrip('/')

        # url not end with '/'
        mission["url"] = mission["url"].strip('/')

        # Compute the domain
        head = mission['url'].find("//")
        tail = mission['url'][head+2:].find("/")
        mission['domain'] = mission['url'] if tail == -1 else mission['url'][:head+2+tail]

        # Check whether the url is valid
        try:
            response = urllib.urlopen(mission['url'])
        except KeyboardInterrupt:
            log.info("You pressed Ctrl+C")
            sys.exit(0)
        except:
            log.error("This url is not vaild : " + mission['url'])
