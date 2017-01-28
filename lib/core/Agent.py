class Agent:
    def __init__(self,mission):
        self.mission = mission
    def run(self,tunnel):
        while True:
            if tunnel.emptyin():
                response = tunnel.getin()
