class Intersection:
    def __init__(self, intersection_id):
        self.intersection_id = intersection_id
        self.tlsID = []
        self.movements = []
        self.m_lights = []  # Lights associated with every movement
        self.phases = []
        self.lights = []
        self.cycles = []
        self.cycles_names = []

    def config(self):
        inter_config = {
            2: {
                "tlsID": "intersection/0002/tls",
                "movements": [0, 1, 3, 4, 5, 7],
                "m_lights": [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []],
                "phases": [[3, 7], [0, 5], [0, 4], [1, 5]],
                "lights": list("rrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 0, 0, 0],
                           [3, 0, 0, 0]],
                "cycles_names": ["Normal", "AccA", "AccB"]
            },
            3: {
                "tlsID": "intersection/0002/tls",
                "movements": [0, 1, 3, 4, 5, 7],
                "m_lights": [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []],
                "phases": [[3, 7], [0, 5], [0, 4], [1, 5]],
                "lights": list("rrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 0, 0, 0],
                           [3, 0, 0, 0]],
                "cycles_names": ["Normal", "AccA", "AccB"]
            },
            4: {
                "tlsID": "intersection/0002/tls",
                "movements": [0, 1, 3, 4, 5, 7],
                "m_lights": [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []],
                "phases": [[3, 7], [0, 5], [0, 4], [1, 5]],
                "lights": list("rrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 0, 0, 0],
                           [3, 0, 0, 0]],
                "cycles_names": ["Normal", "AccA", "AccB"]
            }
        }

        self.tlsID = inter_config[self.intersection_id]["tlsID"]
        self.movements = inter_config[self.intersection_id]["movements"]
        self.m_lights = inter_config[self.intersection_id]["m_lights"]
        self.phases = inter_config[self.intersection_id]["phases"]
        self.lights = inter_config[self.intersection_id]["lights"]
        self.cycles = inter_config[self.intersection_id]["cycles"]
        self.cycles_names = inter_config[self.intersection_id]["cycles_names"]
