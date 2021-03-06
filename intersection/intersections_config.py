
INTER_CONFIG_OPT = {
    "0002": {
        "state_topic": "intersection/0002/state",
        "tls_id": "intersection/0002/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0003": {
        "state_topic": "intersection/0003/state",
        "tls_id": "intersection/0003/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0004": {
        "state_topic": "intersection/0004/state",
        "tls_id": "intersection/0004/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0005": {
        "state_topic": "intersection/0005/state",
        "tls_id": "intersection/0005/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0006": {
        "state_topic": "intersection/0006/state",
        "tls_id": "intersection/0006/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0007": {
        "state_topic": "intersection/0007/state",
        "tls_id": "intersection/0007/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0008": {
        "state_topic": "intersection/0008/state",
        "tls_id": "intersection/0008/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0009": {
        "state_topic": "intersection/0009/state",
        "tls_id": "intersection/0009/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")
    },
    "0010": {
        "state_topic": "intersection/0010/state",
        "tls_id": "intersection/0010/tls",
        "movements": [0, 1, 2, 3, 4, 5, 6, 7],
        "mov_phantom": [],
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
        # "m_lights": [[[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]],
        #              [[7], [12, 13, 14], [11], [0, 1, 2], [15], [4, 5, 6], [3], [8, 9, 10]]],
        # "m_lights": [[[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]],
        #              [[5], [9, 10], [8], [0, 1], [11], [3, 4], [2], [6, 7]]],
        "m_lights": [[[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]],
                     [[10, 11], [18, 19, 20, 21], [16, 17], [0, 1, 2, 3], [22, 23], [6, 7, 8, 9], [4, 5],
                      [12, 13, 14, 15]]],
        # "m_detectors": [["e02"], ["w01", "w02"], ["s02"], ["n01", "n02"], ["w02"], ["e01", "e02"], ["n02"], ["s01", "s02"]],
        "m_detectors": [["e02"], ["w01"], ["s02"], ["n01"], ["w02"], ["e01"], ["n02"], ["s01"]],
        # "lights": list("rrrrrrrrrrrrrrrr")
        # "lights": list("rrrrrrrrrrrr")
        "lights": list("rrrrrrrrrrrrrrrrrrrrrrrr")

    }
}


INTER_CONFIG_OSM = {
    "0002": {
        "state_topic": "intersection/0002/state",
        "tls_id": "intersection/0002/tls",
        "movements": [1, 2, 4, 5, 7],
        "mov_phantom": [0, 3, 6],
        # Phantom 0, 3, 6. Hecho de esta manera para solo manejar los movs que me interesan
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
        "m_max_vehicle_number": 7,  # 50meter * 1.5 cars/ 10 meter = 7.5car ~ 7car
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
        "movements": [0, 1, 3, 5, 6],
        "mov_phantom": [2, 4, 7],
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
        "m_max_vehicle_number": 6,
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
        "movements": [0, 3, 5],
        "mov_phantom": [1, 4, 6],
        "phases": [[0, 5], [3, 6], [1, 5], [0, 4]],
        "cycles": [[1, 0, 0, 0],
                   [1, 2, 1, 1],  # Problem 3
                   [1, 3, 1, 1],
                   [1, 1, 1, 1],
                   # Problem 4: There is no Transition Cxx to the same Phase / Solution: Force that it can't be a cycle with only one phase!
                   [0, 0, 0, 0]],
        "cycles_names": ["Normal", "AccSO", "AccWO", "AccEI", "AccNI"],
        "neighbors_ids": {
            "S": "",
            "E": "0005",
            "N": "",
            "W": ""
        },
        "m_max_speed": 14,
        "m_max_vehicle_number": 4,
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
        "movements": [2, 5, 7],
        "mov_phantom": [0, 3, 6],
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
        "m_max_vehicle_number": 4,
        # Configuration variables for SUMO application
        "m_lights": [[[], [], [8, 9], [], [], [0, 1, 2, 3, 4], [], [5, 6, 7]],
                     [[], [], [8, 9], [], [], [0, 1, 2, 3, 4], [], [5, 6, 7]],
                     [[], [], [8, 9], [], [], [0, 1, 2], [], [5, 6, 7]]],
        "m_detectors": [[], [], ["s03", "s04"], [], [], ["e01", "e02", "e03", "e04"], [],
                        ["s01", "s02", "s03"]],
        "lights": list("rrrrrrrrrrrr")
    },
    "0006": {
        "state_topic": "intersection/0006/state",
        "tls_id": "intersection/0006/tls",
        "movements": [0, 2, 3, 5, 7],
        "mov_phantom": [1, 4, 6],
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
        "m_max_vehicle_number": 6,
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
        "movements": [2, 5, 7],
        "mov_phantom": [0, 3, 6],
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
        "m_max_vehicle_number": 5,
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
        "movements": [0, 3, 5],
        "mov_phantom": [1, 4, 6],
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
        "m_max_vehicle_number": 7,
        # Configuration variables for SUMO application
        "m_lights": [[[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []],
                     [[2], [], [], [3, 4], [], [0, 1], [], []],
                     [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []]],
        "m_detectors": [["e02"], [], [], ["n01", "n02"], [], ["e01", "e02"], [], []],
        "lights": list("rrrrrrrrr")
    },
    "0009": {
        "state_topic": "intersection/0009/state",
        "tls_id": "intersection/0009/tls",
        "movements": [1, 4, 7],
        "mov_phantom": [0, 2, 5],
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
        "m_max_vehicle_number": 7,
        # Configuration variables for SUMO application
        "m_lights": [[[], [5, 6], [], [], [7], [], [], [0, 1, 2, 3, 4]],
                     [[], [5, 6], [], [], [7], [], [], [0, 1, 2, 3, 4]],
                     [[], [5, 6], [], [], [7], [], [], [0, 1]]],
        "m_detectors": [[], ["w01", "w02"], [], [], ["w02"], [], [], ["s01", "s02", "s03"]],
        "lights": list("rrrrrrrrrr")
    },
    "0010": {
        "state_topic": "intersection/0010/state",
        "tls_id": "intersection/0010/tls",
        "movements": [1, 4, 6],
        "mov_phantom": [0, 2, 5],
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
        "m_max_vehicle_number": 7,
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
        "movements": [1, 4, 7],
        "mov_phantom": [0, 2, 5],
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
        "m_max_vehicle_number": 7,
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
        "movements": [1, 3, 6],
        "mov_phantom": [2, 4, 7],
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
        "m_max_vehicle_number": 6,
        # Configuration variables for SUMO application
        "m_lights": [[[], [0, 1, 2], [], [3, 4], [], [], [5, 6], []],
                     [[], [0, 1, 2], [], [3, 4], [], [], [5, 6], []],
                     [[], [0], [], [3, 4], [], [], [5, 6], []]],
        "m_detectors": [[], ["w01", "w02"], [], ["n01", "n02"], [], [], ["n03", "n04"], []],
        "lights": list("rrrrrrrrr")
    }
}
