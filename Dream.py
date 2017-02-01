#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import threading

from lib.core.tunnel.Internal import Internal
from lib.core.Connector import Connector
from lib.core.Agent import Agent
from lib.utils.Config import check
from lib.utils.Log import Log

log = Log(__name__)

# Load config and missions
with open('config.json','r') as data:
    try:
        config = json.load(data)
    except ValueError as error:
        log.error("In config.json : " + str(error))

with open("missions.json",'r') as data:
    try:
        missions = json.load(data)
    except ValueError as error:
        log.error("In missions.json : " + str(error))

check(config,missions)

# global variables
now = 0
total = config['Connector-threads']
connector_counter = 0
agent_counter = 0

# Start Connectors
'''
Connector tunnel in : {"index" : integer, "url" : string, "header" : dictionary, "postdata" : dictionary}
Connector tunnel out : {"index" : integet, "url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
'''
connectors = []
connector_threads = []
connector_tunnels = []
for i in xrange(total):
    connectors.append(Connector(config))
    connector_tunnels.append(Internal())
    connector_threads.append(threading.Thread(target = connectors[i].run, args = (connector_tunnels[i],)))
    connector_threads[i].daemon = True
    connector_threads[i].start()

# Start Agents
'''
Agent tunnel in : {"url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
Agent tunnel out : [{"url" : string, "header" : dictionary, "postdata" : dictionary},...]
'''
agents = []
agent_threads = []
agent_tunnels = []
for i,mission in enumerate(missions):
    agents.append(Agent(mission))
    agent_tunnels.append(Internal())
    agent_threads.append(threading.Thread(target = agents[i].run, args = (agent_tunnels[i],)))
    agent_threads[i].daemon = True
    agent_threads[i].start()

# Put initial tasks
for i,mission in enumerate(missions):
    connector_tunnels[now].putin({"index" : i, "url" : mission["url"], "header" : {}, "postdata" : {}})
    connector_counter += 1
    now = (now+1)%total

# Start running
while connector_counter or agent_counter:
    # Get response from Connector
    for i,tunnel in enumerate(connector_tunnels):
        if not tunnel.emptyout():
            data = tunnel.getout()
            connector_counter -= 1
            if data.get("response"):
                agent_tunnels[data["index"]].putin(data)
                agent_counter += 1
    # Get tasks from Agent
    for i,tunnel in enumerate(agent_tunnels):
        if not tunnel.emptyout():
            data = tunnel.getout()
            agent_counter -= 1
            for task in data:
                connector_tunnels[now].putin(dict({"index" : i}.items() + task.items()))
                connector_counter += 1
                now = (now+1)%total

# Get the analyze result
for agent in agents:
    agent.report()
