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
                "movements": [1, 2, 4, 5, 7, 0, 3, 6],  # Phantom 0, 3, 6
                "m_lights": [[], [7], [6], [], [8], [0, 1], [], [2, 3, 4, 5]],
                "phases": [[1, 4], [1, 5], [2, 7], [0, 4], [0, 5], [2, 6], [3, 7]],
                "lights": list("rrrrrrrrrrrrr"),
                "cycles": [[1, 2, 0, 0, 0, 0, 0],
                           [2, 2, 3, 4, 2, 2, 2],
                           [1, 5, 1, 1, 1, 1, 1],
                           [6, 0, 0, 0, 0, 0, 0]],
                "cycles_names": ["Normal", "AccB", "AccC", "AccD"]
            },
            3: {
                "tlsID": "intersection/0003/tls",
                "movements": [0, 1, 3, 5, 6, 2, 4, 7],
                "m_lights": [[1], [2, 3], [], [4, 5, 6], [], [0], [7], []],
                "phases": [[0, 5], [1, 5], [3, 6], [2, 6], [3, 7], [0, 4], [1, 4]],
                "lights": list("rrrrrrrrrrrr"),
                "cycles": [[1, 2, 0, 0, 0, 0, 0],
                           [1, 3, 1, 1, 1, 1, 1],
                           [4, 0, 0, 0, 0, 0, 0],
                           [2, 2, 5, 2, 2, 6, 2]],
                "cycles_names": ["Normal", "AccA", "AccB", "AccD"]
            },
            4: {
                "tlsID": "intersection/0004/tls",
                "movements": [0, 3, 5, 1, 4, 6],
                "m_lights": [[2, 3], [], [], [5, 6], [], [0, 1], [], []],
                "phases": [[0, 5], [3, 6], [1, 5], [0, 4]],
                "lights": list("rrrrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 2, 2, 2],  # Problem 3
                           [1, 3, 1, 1]],
                "cycles_names": ["Normal", "AccA", "AccD"]
            },
            5: {
                "tlsID": "intersection/0005/tls",
                "movements": [2, 5, 7, 0, 3, 6],
                "m_lights": [[], [], [8, 9], [], [], [0, 1, 2, 3, 4], [], [5, 6, 7]],
                "phases": [[0, 5], [2, 7], [2, 6], [3, 7]],
                "lights": list("rrrrrrrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 0, 0, 0],
                           [3, 3, 3, 3]],  # Problem 3
                "cycles_names": ["Normal", "AccA", "AccB"]
            },
            6: {
                "tlsID": "intersection/0006/tls",
                "movements": [0, 2, 3, 5, 7, 1, 4, 6],
                "m_lights": [[5], [], [7], [0, 1], [], [2, 3, 4], [], [6]],
                "phases": [[0, 5], [2, 7], [3, 7], [1, 5], [2, 6], [3, 6], [0, 4]],
                "lights": list("rrrrrrrrrrrr"),
                "cycles": [[1, 2, 0, 0, 0, 0, 0],
                           [1, 3, 1, 1, 1, 1, 1],
                           [4, 0, 0, 0, 5, 0, 0],
                           [2, 2, 6, 2, 2, 2, 2]],
                "cycles_names": ["Normal", "AccA", "AccC", "AccD"]
            },
            7: {
                "tlsID": "intersection/0007/tls",
                "movements": [2, 5, 7, 3, 6],
                "m_lights": [[], [], [4], [], [], [0, 1, 2], [], [3]],
                "phases": [[0, 5], [2, 7], [2, 6], [3, 7]],
                "lights": list("rrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 0, 0, 0],
                           [3, 3, 3, 3]],  # Problem 3
                "cycles_names": ["Normal", "AccC", "AccD"]
            },
            8: {
                "tlsID": "intersection/0008/tls",
                "movements": [0, 3, 5, 1, 4, 6],
                "m_lights": [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []],
                "phases": [[0, 5], [3, 6], [1, 5], [0, 4]],
                "lights": list("rrrrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 2, 2, 2],  # Problem 3
                           [1, 3, 1, 1]],
                "cycles_names": ["Normal", "AccA", "AccD"]
            },
            9: {
                "tlsID": "intersection/0009/tls",
                "movements": [1, 4, 7, 0, 2, 5],
                "m_lights": [[], [5, 6], [], [], [7], [], [], [0, 1, 2, 3, 4]],
                "phases": [[1, 4], [2, 7], [0, 4], [1, 5]],
                "lights": list("rrrrrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [1, 2, 1, 1],
                           [3, 3, 3, 3]],  # Problem 3
                "cycles_names": ["Normal", "AccB", "AccC"]
            },
            10: {
                "tlsID": "intersection/0010/tls",
                "movements": [1, 4, 6, 0, 2, 5],
                "m_lights": [[], [1, 2], [], [], [3], [], [0], []],
                "phases": [[1, 4], [2, 6], [0, 4], [1, 5]],
                "lights": list("rrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 2, 2, 2],  # Problem 3
                           [1, 3, 1, 1]],
                "cycles_names": ["Normal", "AccB", "AccC"]
            },
            11: {
                "tlsID": "intersection/0011/tls",
                "movements": [1, 4, 7, 0, 2, 5],
                "m_lights": [[], [2, 3, 4], [], [], [5], [], [], [0, 1]],
                "phases": [[1, 4], [2, 7], [0, 4], [1, 5]],
                "lights": list("rrrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [1, 2, 1, 1],
                           [3, 3, 3, 3]],  # Problem 3
                "cycles_names": ["Normal", "AccB", "AccC"]
            },
            12: {
                "tlsID": "intersection/0002/tls",
                "movements": [1, 3, 6, 2, 4, 7],
                "m_lights": [[], [0, 1, 2], [], [3, 4], [], [5, 6], [], []],
                "phases": [[1, 4], [3, 6], [2, 6], [3, 7]],
                "lights": list("rrrrrrrrr"),
                "cycles": [[1, 0, 0, 0],
                           [2, 0, 0, 0],
                           [3, 3, 3, 3]],  # Problem 3
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
