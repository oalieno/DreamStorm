#!/usr/bin/python
import sys
import json
import threading

from lib.core.tunnel.Internal import Internal
from lib.core.Connector import Connector
from lib.core.Agent import Agent
from lib.utils.Config import check

# Load config and missions
with open('config.json','r') as data:
    config = json.load(data)

with open("missions.json",'r') as data:
    missions = json.load(data)

check(config,mission)

# global variables
now = 0
total = config['Connector-threads']
connector_counter = 0
agent_counter = 0
table = {}

# Start Connectors
'''
Connector tunnel in : {"url" : string, "header" : dictionary, "postdata" : dictionary}
Connector tunnel out : {"url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
'''
connector = []
connector_thread = []
connector_tunnel = []
for i in xrange(total):
    connector.append(Connector(config))
    connector_tunnel.append(Internal())
    connector_thread.append(threading.Thread(target = connector[i].run, args = (connector_tunnel[i],)))
    connector_thread[i].daemon = True
    connector_thread[i].start()

# Start Agents
'''
Agent tunnel in : {"url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
Agent tunnel out : {"url" : string, "header" : dictionary, "postdata" : dictionary, "tasks" : [{"url" : string, "header" : dictionary, "postdata" : dictionary},...]}
'''
agent = []
agent_thread = []
agent_tunnel = []
for i,mission in enumerate(missions):
    table[mission["url"]] = i
    agent.append(Agent(mission))
    agent_tunnel.append(Internal())
    agent_thread.append(threading.Thread(target = agent[i].run, args = (agent_tunnel[i],)))
    agent_thread[i].daemon = True
    agent_thread[i].start()

# Put initial tasks
for mission in missions:
    connector_tunnel[now].putin({"url" : mission["url"], "header" : {}, "postdata" : {}})
    connector_counter += 1
    now = (now+1)%total

# Start running
while connector_counter and agent_counter:
    for i,tunnel in enumerate(connector_tunnel):
        if not tunnel.emptyout():
            data = tunnel.getout()
            connector_counter -= 1
            if data.get("response"):
                agent_tunnel[table[data["url"]]].putin(data)
                agent_counter += 1
    for i,tunnel in enumerate(agent_tunnel):
        if not tunnel.emptyout():
            data = tunnel.getout()
            agent_counter -= 1
            for task in data["tasks"]:
                connector_tunnel[now].putin(task)
                connector_counter += 1
                now = (now+1)%total
