# File that contains the Intersection class


class Intersection:
    def __init__(self, intersection_id, inter_config={}):
        self.id = intersection_id
        self.state_topic = []
        self.tls_id = []
        self.movements = []
        self.mov_phantom = []
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
            self.mov_phantom = inter_config[self.id]["mov_phantom"]
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
        self.vehicleNumber = [[0, 0], [0, 0]]
        self.occupancy = [[0, 0], [0, 0]]
        self.jamLengthVehicle = [[0, 0]]
        self.meanSpeed = [[0, 0]]


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

    def get_vehicle_number(self, time, detector="ALL"):
        vehicle_number = 0
        if detector in self.detectors_name:
            if self._detectors[detector].vehicleNumber[0][0] < time:
                vehicle_number = self._detectors[detector].vehicleNumber[0][1]
            else:
                vehicle_number = self._detectors[detector].vehicleNumber[1][1]
        elif detector == "ALL":
            for det in self._detectors:
                if self._detectors[det].vehicleNumber[0][0] < time:
                    vehicle_number += self._detectors[det].vehicleNumber[0][1]
                else:
                    vehicle_number += self._detectors[det].vehicleNumber[1][1]
            vehicle_number = vehicle_number / len(self._detectors)
        else:
            vehicle_number = "NA"
        return vehicle_number

    def get_occupancy(self, time, detector="ALL"):
        occupancy = 0
        if detector in self.detectors_name:
            if self._detectors[detector].occupancy[0][0] < time:
                occupancy = self._detectors[detector].occupancy[0][1]
            else:
                occupancy = self._detectors[detector].occupancy[1][1]
        elif detector == "ALL":
            for det in self._detectors:
                if self._detectors[det].occupancy[0][0] < time:
                    occupancy += self._detectors[det].occupancy[0][1]
                else:
                    occupancy += self._detectors[det].occupancy[1][1]
            occupancy = occupancy / len(self._detectors)
        else:
            occupancy = "NA"
        return occupancy

    def get_jam_length_vehicle(self, time, detector="ALL"):  # "time" variable is irrelevant in the current control ...
        jam_length_vehicle = 0
        future_val = 0
        if detector in self.detectors_name:
            for jam in self._detectors[detector].jamLengthVehicle:
                if jam[0] < time:
                    jam_length_vehicle += jam[1]
                else:
                    future_val += 1
            jam_length_vehicle = jam_length_vehicle / len(self._detectors[detector].jamLengthVehicle) - future_val
        elif detector == "ALL":
            jam_length_vehicle_list = []
            for det in self._detectors:
                jam_length_vehicle_list.append(0)
                if self._detectors[det].jamLengthVehicle:
                    future_val = 0
                    for jam in self._detectors[det].jamLengthVehicle:
                        if jam[0] < time:
                            jam_length_vehicle_list[-1] += jam[1]
                        else:
                            future_val += 1
                    jam_length_vehicle_list[-1] = jam_length_vehicle_list[-1] / len(self._detectors[det].jamLengthVehicle) - future_val
            jam_length_vehicle = sum(jam_length_vehicle_list) / len(jam_length_vehicle_list)
        else:
            jam_length_vehicle = "NA"
        return jam_length_vehicle

    def get_mean_speed(self, time, detector="ALL"):  # "time" variable is irrelevant in the current control strategy (speed values are used in the phase transition process, much later its recollection)
        mean_speed = 0
        future_val = 0
        if detector in self.detectors_name:
            for msp in self._detectors[detector].meanSpeed:
                if msp[0] < time:
                    mean_speed += msp[1]
                else:
                    future_val += 1
            mean_speed = mean_speed / len(self._detectors[detector].meanSpeed) - future_val
        elif detector == "ALL":
            mean_speed_list = []
            for det in self._detectors:
                mean_speed_list.append(0)
                if self._detectors[det].meanSpeed:
                    future_val = 0
                    for msp in self._detectors[det].meanSpeed:
                        if msp[0] < time:
                            mean_speed_list[-1] += msp[1]
                        else:
                            future_val += 1
                    mean_speed_list[-1] = mean_speed_list[-1] / len(self._detectors[det].meanSpeed) - future_val
            mean_speed = sum(mean_speed_list) / len(mean_speed_list)
        else:
            mean_speed = "NA"
        return mean_speed

    def set_vehicle_number(self, detector, vehicle_number):
        self._detectors[detector].vehicleNumber.insert(0, vehicle_number)
        self._detectors[detector].vehicleNumber.pop(-1)
        return

    def set_occupancy(self, detector, occupancy):
        self._detectors[detector].occupancy.insert(0, occupancy)
        self._detectors[detector].occupancy.pop(-1)
        return

    def set_jam_length_vehicle(self, detector, jam_length_vehicle):
        self._detectors[detector].jamLengthVehicle.insert(0, jam_length_vehicle)
        return

    def set_mean_speed(self, detector, mean_speed):
        self._detectors[detector].meanSpeed.insert(0, mean_speed)
        return

    def reset_jam_length_vehicle(self, detector="ALL"):
        if detector in self.detectors_name:
            self._detectors[detector].jamLengthVehicle = []
        elif detector == "ALL":
            for det in self._detectors:
                self._detectors[det].jamLengthVehicle = []
        return

    def reset_mean_speed(self, detector="ALL"):
        if detector in self.detectors_name:
            self._detectors[detector].meanSpeed = []
        elif detector == "ALL":
            for det in self._detectors:
                self._detectors[det].meanSpeed = []
        return
