# File that contains the Intersection class


class IntersectionOpt:
    def __init__(self, intersection_id, auto_configuration=True):
        self.id = intersection_id
        self.state_topic = []
        self.tls_id = []
        self.movements = []
        self.phases = []
        self.cycles = []
        self.cycles_names = []
        self.neighbors_ids = {}
        self.m_max_speed = 0
        self.m_max_vehicle_number = 0
        self.m_lights = []  # Lights associated with every movement
        self.m_detectors = []  # detectors associated with every movement
        self.lights = []

        if auto_configuration:
            inter_config = {
                "0002": {
                    "state_topic": "intersection/0002/state",
                    "tls_id": "intersection/0002/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0005",
                        "E": "0003",
                        "N": "",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0003": {
                    "state_topic": "intersection/0003/state",
                    "tls_id": "intersection/0003/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0006",
                        "E": "0004",
                        "N": "",
                        "W": "0002"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0004": {
                    "state_topic": "intersection/0004/state",
                    "tls_id": "intersection/0004/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0007",
                        "E": "",
                        "N": "",
                        "W": "0003"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0005": {
                    "state_topic": "intersection/0005/state",
                    "tls_id": "intersection/0005/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0008",
                        "E": "0006",
                        "N": "0002",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0006": {
                    "state_topic": "intersection/0006/state",
                    "tls_id": "intersection/0006/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0009",
                        "E": "0007",
                        "N": "0003",
                        "W": "0005"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0007": {
                    "state_topic": "intersection/0007/state",
                    "tls_id": "intersection/0007/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0010",
                        "E": "",
                        "N": "0004",
                        "W": "0006"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0008": {
                    "state_topic": "intersection/0008/state",
                    "tls_id": "intersection/0008/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "0009",
                        "N": "0005",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0009": {
                    "state_topic": "intersection/0009/state",
                    "tls_id": "intersection/0009/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "0010",
                        "N": "0006",
                        "W": "0008"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                },
                "0010": {
                    "state_topic": "intersection/0010/state",
                    "tls_id": "intersection/0010/tls",
                    "movements": [0, 1, 2, 3, 4, 5, 6, 7],
                    "phases": [[0, 4], [1, 5], [2, 6], [3, 7], [1, 4], [2, 7], [0, 5], [3, 6]],
                    "cycles": [[1, 2, 3, 0, 0, 0, 0, 0],
                               [1, 2, 5, 1, 1, 4, 1, 1],
                               [6, 0, 0, 5, 0, 0, 3, 0],
                               [1, 6, 7, 1, 1, 1, 2, 1],
                               [4, 0, 0, 7, 3, 0, 0, 0],
                               [1, 7, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2, 2],
                               [1, 5, 0, 0, 0, 0, 0, 0],
                               [2, 2, 3, 6, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "",
                        "N": "0007",
                        "W": "0009"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
                                 [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
                    "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"],
                                    ["s01", "s02"]],
                    "lights": list("rrrrrrrrrrrrrrrr")
                }
            }

            self.state_topic = inter_config[self.id]["state_topic"]
            self.tls_id = inter_config[self.id]["tls_id"]
            self.movements = inter_config[self.id]["movements"]
            self.phases = inter_config[self.id]["phases"]
            self.cycles = inter_config[self.id]["cycles"]
            self.cycles_names = inter_config[self.id]["cycles_names"]
            self.neighbors_ids = inter_config[self.id]["neighbors_ids"]
            self.m_max_speed = inter_config[self.id]["m_max_speed"]
            self.m_max_vehicle_number = inter_config[self.id]["m_max_vehicle_number"]
            self.m_lights = inter_config[self.id]["m_lights"]
            self.m_detectors = inter_config[self.id]["m_detectors"]
            self.lights = inter_config[self.id]["lights"]


class Intersection:
    def __init__(self, intersection_id, auto_configuration=True):
        self.id = intersection_id
        self.state_topic = []
        self.tls_id = []
        self.movements = []
        self.phases = []
        self.cycles = []
        self.cycles_names = []
        self.neighbors_ids = {}
        self.m_max_speed = 0
        self.m_max_vehicle_number = 0
        self.m_lights = []  # Lights associated with every movement
        self.m_detectors = []  # detectors associated with every movement
        self.lights = []

        if auto_configuration:
            inter_config = {
                "0002": {
                    "state_topic": "intersection/0002/state",
                    "tls_id": "intersection/0002/tls",
                    "movements": [1, 2, 4, 5, 7, 0, 3, 6],  # Phantom 0, 3, 6
                    "phases": [[1, 4], [1, 5], [2, 7], [0, 4], [0, 5], [2, 6], [3, 7]],
                    "cycles": [[1, 2, 0, 0, 0, 0, 0],
                               [2, 2, 3, 4, 2, 2, 2],
                               [1, 5, 1, 1, 1, 1, 1],
                               [6, 0, 0, 0, 0, 0, 0],
                               [1, 0, 0, 0, 0, 0, 0],
                               [2, 0, 0, 0, 0, 0, 0],
                               [2, 2, 4, 2, 2, 2, 2]],
                    "cycles_names": ["Normal", "AccEO", "AccNO", "AccWO", "AccSI", "AccEI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0005",
                        "E": "",
                        "N": "",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [7], [6], [], [8], [0, 1], [], [2, 3, 4, 5]],
                                 [[], [7], [6], [], [8], [0, 1], [], [2, 3, 4, 5]],
                                 [[], [7], [6], [], [8], [0, 1], [], [2, 3, 4, 5]],
                                 [[], [7], [6], [], [8], [0, 1], [], [2, 3, 4, 5]]],
                    "m_detectors": [[], ["w01"], ["s03"], [], ["w01"], ["e01"], [], ["s01", "s02", "s03"]],
                    "lights": list("rrrrrrrrrrrrr")
                },
                "0003": {
                    "state_topic": "intersection/0003/state",
                    "tls_id": "intersection/0003/tls",
                    "movements": [0, 1, 3, 5, 6, 2, 4, 7],
                    "phases": [[0, 5], [1, 5], [3, 6], [2, 6], [3, 7], [0, 4], [1, 4]],
                    "cycles": [[1, 2, 0, 0, 0, 0, 0],
                               [1, 3, 1, 1, 1, 1, 1],
                               [4, 0, 0, 0, 0, 0, 0],
                               [2, 2, 5, 2, 2, 6, 2],
                               [2, 2, 6, 2, 2, 2, 2],
                               [1, 0, 0, 0, 0, 0, 0],
                               [2, 0, 0, 0, 0, 0, 0]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccWO", "AccEI", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "0008",
                        "E": "",
                        "N": "",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[1], [2, 3], [], [4, 5, 6], [], [0], [7], []],
                                 [[1], [2, 3], [], [4, 5, 6], [], [0], [7], []],
                                 [[1], [2, 3], [], [4, 5, 6], [], [0], [7], []],
                                 [[1], [2, 3], [], [4, 5, 6], [], [0], [7], []]],
                    "m_detectors": [["e01"], ["w01"], [], ["n01", "n02"], [], ["e01"], ["n02"], []],
                    "lights": list("rrrrrrrrrrrr")
                },
                "0004": {
                    "state_topic": "intersection/0004/state",
                    "tls_id": "intersection/0004/tls",
                    "movements": [0, 3, 5, 1, 4, 6],
                    "phases": [[0, 5], [3, 6], [1, 5], [0, 4]],
                    "cycles": [[1, 0, 0, 0],
                               [1, 2, 1, 1],  # Problem 3
                               [1, 3, 1, 1],
                               [1, 1, 1, 1],  # Problem 4: There is no Transition Cxx to the same Phase
                               [0, 0, 0, 0]],
                    "cycles_names": ["Normal", "AccSO", "AccWO", "AccEI", "AccNI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "0005",
                        "N": "",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[2, 3], [], [], [4, 5, 6], [], [0, 1], [], []],
                                 [[2, 3], [], [], [4], [], [0, 1], [], []],
                                 [[2, 3], [], [], [4, 5, 6], [], [0, 1], [], []]],
                    "m_detectors": [["e03", "e04"], [], [], ["n01", "n02"], [], ["e01", "e02"], [], []],
                    "lights": list("rrrrrrrrr")
                },
                "0005": {
                    "state_topic": "intersection/0005/state",
                    "tls_id": "intersection/0005/tls",
                    "movements": [2, 5, 7, 0, 3, 6],
                    "phases": [[0, 5], [2, 7], [2, 6], [3, 7]],
                    "cycles": [[1, 0, 0, 0],
                               [2, 0, 0, 0],
                               [3, 0, 0, 0],  # Problem 3
                               [0, 0, 0, 0],  # Problem 4:
                               [1, 1, 1, 1]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccSI", "AccEI"],
                    "neighbors_ids": {
                        "S": "0009",
                        "E": "0006",
                        "N": "0002",
                        "W": "0004"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [], [8, 9], [], [], [0, 1, 2, 3, 4], [], [5, 6, 7]],
                                 [[], [], [8, 9], [], [], [0, 1, 2, 3, 4], [], [5, 6, 7]],
                                 [[], [], [8, 9], [], [], [0, 1, 2], [], [5, 6, 7]]],
                    "m_detectors": [[], [], ["s03", "s04"], [], [], ["e01", "e02", "e03", "e04"], [], ["s01", "s02", "s03"]],
                    "lights": list("rrrrrrrrrrrr")
                },
                "0006": {
                    "state_topic": "intersection/0006/state",
                    "tls_id": "intersection/0006/tls",
                    "movements": [0, 2, 3, 5, 7, 1, 4, 6],
                    "phases": [[0, 5], [2, 7], [3, 7], [1, 5], [2, 6], [3, 6], [0, 4]],
                    "cycles": [[1, 2, 0, 0, 0, 0, 0],
                               [1, 3, 1, 1, 1, 1, 1],
                               [4, 0, 0, 0, 5, 0, 0],
                               [2, 2, 6, 2, 2, 2, 2],
                               [5, 0, 0, 0, 0, 0, 0],
                               [1, 2, 1, 1, 1, 1, 1],
                               [1, 0, 0, 0, 0, 0, 0]],
                    "cycles_names": ["Normal", "AccSO", "AccNO", "AccWO", "AccSI", "AccEI", "AccNI"],
                    "neighbors_ids": {
                        "S": "0010",
                        "E": "0007",
                        "N": "",
                        "W": "0005"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[5], [], [7], [0, 1], [], [2, 3, 4], [], [6]],
                                 [[5], [], [7], [0, 1], [], [2, 3, 4], [], [6]],
                                 [[5], [], [7], [0, 1], [], [2, 3, 4], [], [6]],
                                 [[5], [], [7], [0, 1], [], [2, 3, 4], [], [6]]],
                    "m_detectors": [["e02"], [], ["s01"], ["n01"], [], ["e01", "e02"], [], ["s01"]],
                    "lights": list("rrrrrrrrrrrr")
                },
                "0007": {
                    "state_topic": "intersection/0007/state",
                    "tls_id": "intersection/0007/tls",
                    "movements": [2, 5, 7, 0, 3, 6],
                    "phases": [[0, 5], [2, 7], [2, 6], [3, 7]],
                    "cycles": [[1, 0, 0, 0],
                               [2, 0, 0, 0],
                               [3, 0, 0, 0],  # Problem 3
                               [0, 0, 0, 0],  # Problem 4:
                               [1, 1, 1, 1]],
                    "cycles_names": ["Normal", "AccSO", "AccWO", "AccSI", "AccEI"],
                    "neighbors_ids": {
                        "S": "0011",
                        "E": "0008",
                        "N": "",
                        "W": "0006"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [], [4], [], [], [0, 1, 2], [], [3]],
                                 [[], [], [4], [], [], [0, 1, 2], [], [3]],
                                 [[], [], [4], [], [], [0], [], [3]]],
                    "m_detectors": [[], [], ["s01"], [], [], ["e01", "e02"], [], ["s01"]],
                    "lights": list("rrrrrrr")
                },
                "0008": {
                    "state_topic": "intersection/0008/state",
                    "tls_id": "intersection/0008/tls",
                    "movements": [0, 3, 5, 1, 4, 6],
                    "phases": [[0, 5], [3, 6], [1, 5], [0, 4]],
                    "cycles": [[1, 0, 0, 0],
                               [1, 2, 1, 1],  # Problem 3
                               [1, 3, 1, 1],
                               [1, 1, 1, 1],  # Problem 4:
                               [0, 0, 0, 0]],
                    "cycles_names": ["Normal", "AccSO", "AccWO", "AccEI", "AccNI"],
                    "neighbors_ids": {
                        "S": "0002",
                        "E": "",
                        "N": "0003",
                        "W": "0007"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []],
                                 [[2], [], [], [3, 4], [], [0, 1], [], []],
                                 [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []]],
                    "m_detectors": [["e02"], [], [], ["n01", "n02", "n03", "n04"], [], ["e01", "e02"], [], []],
                    "lights": list("rrrrrrrrr")
                },
                "0009": {
                    "state_topic": "intersection/0009/state",
                    "tls_id": "intersection/0009/tls",
                    "movements": [1, 4, 7, 0, 2, 5],
                    "phases": [[1, 4], [2, 7], [0, 4], [1, 5]],
                    "cycles": [[1, 0, 0, 0],
                               [1, 2, 1, 1],
                               [1, 3, 1, 1],  # Problem 3
                               [0, 0, 0, 0],  # Problem 4:
                               [1, 1, 1, 1]],
                    "cycles_names": ["Normal", "AccEO", "AccNO", "AccSI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "0010",
                        "N": "0005",
                        "W": ""
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [5, 6], [], [], [7], [], [], [0, 1, 2, 3, 4]],
                                 [[], [5, 6], [], [], [7], [], [], [0, 1, 2, 3, 4]],
                                 [[], [5, 6], [], [], [7], [], [], [0, 1]]],
                    "m_detectors": [[], ["w01", "w02"], [], [], ["w02"], [], [], ["s01", "s02", "s03", "s04"]],
                    "lights": list("rrrrrrrrrr")
                },
                "0010": {
                    "state_topic": "intersection/0010/state",
                    "tls_id": "intersection/0010/tls",
                    "movements": [1, 4, 6, 0, 2, 5],
                    "phases": [[1, 4], [2, 6], [0, 4], [1, 5]],
                    "cycles": [[1, 0, 0, 0],
                               [2, 2, 2, 2],  # Problem 3
                               [1, 3, 1, 1],
                               [0, 0, 0, 0],  # Problem 4:
                               [1, 1, 1, 1]],
                    "cycles_names": ["Normal", "AccEO", "AccNO", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "0011",
                        "N": "0006",
                        "W": "0009"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [1, 2], [], [], [3], [], [0], []],
                                 [[], [1, 2], [], [], [3], [], [0], []],
                                 [[], [1, 2], [], [], [3], [], [0], []]],
                    "m_detectors": [[], ["w01", "w02"], [], [], ["w02"], [], ["n01"], []],
                    "lights": list("rrrrrrr")
                },
                "0011": {
                    "state_topic": "intersection/0011/state",
                    "tls_id": "intersection/0011/tls",
                    "movements": [1, 4, 7, 0, 2, 5],
                    "phases": [[1, 4], [2, 7], [0, 4], [1, 5]],
                    "cycles": [[1, 0, 0, 0],
                               [1, 2, 1, 1],
                               [1, 3, 1, 1],  # Problem 3
                               [0, 0, 0, 0],  # Problem 4:
                               [1, 1, 1, 1]],
                    "cycles_names": ["Normal", "AccEO", "AccNO", "AccSI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "0012",
                        "N": "0007",
                        "W": "0010"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [2, 3, 4], [], [], [5], [], [], [0, 1]],
                                 [[], [2, 3, 4], [], [], [5], [], [], [0, 1]],
                                 [[], [2, 3, 4], [], [], [5], [], [], [0]]],
                    "m_detectors": [[], ["w01", "w02"], [], [], ["w02"], [], [], ["s01"]],
                    "lights": list("rrrrrrrr")
                },
                "0012": {
                    "state_topic": "intersection/0012/state",
                    "tls_id": "intersection/0012/tls",
                    "movements": [1, 3, 6, 2, 4, 7],
                    "phases": [[1, 4], [3, 6], [2, 6], [3, 7]],
                    "cycles": [[1, 0, 0, 0],
                               [2, 0, 0, 0],
                               [3, 0, 0, 0],  # Problem 3
                               [0, 0, 0, 0],  # Problem 4:
                               [1, 1, 1, 1]],
                    "cycles_names": ["Normal", "AccSO", "AccEO", "AccNI", "AccWI"],
                    "neighbors_ids": {
                        "S": "",
                        "E": "",
                        "N": "0008",
                        "W": "0011"
                    },
                    "m_max_speed": 14,
                    "m_max_vehicle_number": 9,
                    # Configuration variables for SUMO application
                    "m_lights": [[[], [0, 1, 2], [], [3, 4], [], [], [5, 6], []],
                                 [[], [0, 1, 2], [], [3, 4], [], [], [5, 6], []],
                                 [[], [0], [], [3, 4], [], [], [5, 6], []]],
                    "m_detectors": [[], ["w01", "w02"], [], ["n01", "n02"], [], [], ["n03", "n04"], []],
                    "lights": list("rrrrrrrrr")
                }
            }

            self.state_topic = inter_config[self.id]["state_topic"]
            self.tls_id = inter_config[self.id]["tls_id"]
            self.movements = inter_config[self.id]["movements"]
            self.phases = inter_config[self.id]["phases"]
            self.cycles = inter_config[self.id]["cycles"]
            self.cycles_names = inter_config[self.id]["cycles_names"]
            self.neighbors_ids = inter_config[self.id]["neighbors_ids"]
            self.m_max_speed = inter_config[self.id]["m_max_speed"]
            self.m_max_vehicle_number = inter_config[self.id]["m_max_vehicle_number"]
            self.m_lights = inter_config[self.id]["m_lights"]
            self.m_detectors = inter_config[self.id]["m_detectors"]
            self.lights = inter_config[self.id]["lights"]


class Neighbor:
    def __init__(self, neighbor_id, neighbor_dir):
        self.id = neighbor_id
        self.direction = neighbor_dir
        self.mov_accident = [False, False, False, False, False, False, False, False]
        self.mov_congestion = [0, 0, 0, 0, 0, 0, 0, 0]


class Detector:
    def __init__(self, detect_id):
        self.id = detect_id
        self.jamLengthVehicle = 0
        self.vehicleNumber = 0
        self.occupancy = 0
        self.meanSpeed = 0



class Movement:
    def __init__(self, mov_id, intersection):
        self.id = mov_id
        self.phases = []
        self.m_lights = []  # Lights associated with every movement
        self.detectors_name = []  # Detectors associated with the movement
        self._detectors = {}
        self.in_neighbors = []
        self.out_neighbors = []
        self.congestionLevel = 0
        self.split = 0
        self.light_state = "RED"

        for i in range(len(intersection.phases)):
            if self.id in intersection.phases[i]:
                self.phases.append(i)

        self.m_lights = intersection.m_lights[0][self.id]
        self.detectors_name = intersection.m_detectors[self.id]
        for i in self.detectors_name:
            self._detectors[i] = Detector(i)

        if self.id == 0:
            self.in_neighbors = [[2, 5], "E"]
            self.out_neighbors = [[3, 6], "S"]
        elif self.id == 1:
            self.in_neighbors = [[1, 6], "W"]
            self.out_neighbors = [[1, 4], "E"]
        elif self.id == 2:
            self.in_neighbors = [[4, 7], "S"]
            self.out_neighbors = [[0, 5], "W"]
        elif self.id == 3:
            self.in_neighbors = [[0, 3], "N"]
            self.out_neighbors = [[3, 6], "S"]
        elif self.id == 4:
            self.in_neighbors = [[1, 6], "W"]
            self.out_neighbors = [[2, 7], "N"]
        elif self.id == 5:
            self.in_neighbors = [[2, 5], "E"]
            self.out_neighbors = [[0, 5], "W"]
        elif self.id == 6:
            self.in_neighbors = [[0, 3], "N"]
            self.out_neighbors = [[1, 4], "E"]
        elif self.id == 7:
            self.in_neighbors = [[4, 7], "S"]
            self.out_neighbors = [[2, 7], "N"]
        else:
            self.in_neighbors = ["ERROR"]
            self.out_neighbors = ["ERROR"]

    def get_jam_length_vehicle(self, det="ALL"):
        jam_length_vehicle = 0
        if det in self.detectors_name:
            jam_length_vehicle = self._detectors[det].jamLengthVehicle
        elif det == "ALL":
            for i in self._detectors:
                jam_length_vehicle += self._detectors[i].jamLengthVehicle
        else:
            jam_length_vehicle = "NA"
        return jam_length_vehicle

    def get_occupancy(self, det="ALL"):
        occupancy = 0
        if det in self.detectors_name:
            occupancy = self._detectors[det].occupancy
        elif det == "ALL":
            for i in self._detectors:
                occupancy += self._detectors[i].occupancy
        else:
            occupancy = "NA"
        return occupancy

    def get_mean_speed(self, det="ALL"):
        mean_speed = 0
        if det in self.detectors_name:
            mean_speed = self._detectors[det].meanSpeed
        elif det == "ALL":
            for i in self._detectors:
                mean_speed += self._detectors[i].meanSpeed
        else:
            mean_speed = "NA"
        return mean_speed

    def get_vehicle_number(self, det="ALL"):
        vehicle_number = 0
        if det in self.detectors_name:
            vehicle_number = self._detectors[det].vehicleNumber
        elif det == "ALL":
            for i in self._detectors:
                vehicle_number += self._detectors[i].vehicleNumber
        else:
            vehicle_number = "NA"
        return vehicle_number

    def set_jam_length_vehicle(self, detector_id, jam_length_vehicle):
        self._detectors[detector_id].jamLengthVehicle = jam_length_vehicle
        return

    def set_occupancy(self, detector_id, occupancy):
        self._detectors[detector_id].occupancy = occupancy
        return

    def set_mean_speed(self, detector_id, mean_speed):
        self._detectors[detector_id].meanSpeed = mean_speed
        return

    def set_vehicle_number(self, detector_id, vehicle_number):
        self._detectors[detector_id].vehicleNumber = vehicle_number
        return


