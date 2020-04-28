# File that contains the Intersection class


class Intersection:
    def __init__(self, intersection_id, inter_config={}):
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

        if inter_config:
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
        self.mov_congestion = [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0]


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
        self.split = 16  # Same as "tAct_" in inter_tpn
        self.accident = [0, ""]
        self.light_state = "r"

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
            jam_length_vehicle = jam_length_vehicle / len(self._detectors)
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
            occupancy = occupancy / len(self._detectors)
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
            mean_speed = mean_speed / len(self._detectors)
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
            vehicle_number = vehicle_number / len(self._detectors)
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
