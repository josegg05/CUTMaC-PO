from intersection import intersections_classes
from intersection import intersections_config
import time
import paho.mqtt.client as mqtt
import json
import datetime
import numpy as np
from skfuzzy import control as ctrl
import zmq


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("intersection/%s/e2det/n" % intersection_id)
    client.subscribe("intersection/%s/e2det/e" % intersection_id)
    client.subscribe("intersection/%s/e2det/s" % intersection_id)
    client.subscribe("intersection/%s/e2det/w" % intersection_id)
    client.subscribe("intersection/all/start")
    print("intersection/%s/e2det/n" % intersection_id)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global msg_dic
    global start_flag
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic == "intersection/all/start":
        print("Message %s" % str(msg.payload))
        if "start" in str(msg.payload):
            start_flag = True
        elif "stop" in str(msg.payload):
            start_flag = False
    else:
        msg_dic.append(json.loads(msg.payload))
        print("message arrive from topic: ", msg.topic)
        # print(msg.topic + " " + str(msg.payload))


def mqtt_conf(mqtt_broker_ip) -> mqtt.Client:
    broker_address = mqtt_broker_ip
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)  # connect to broker
    return client


def pub_zmq_config(port):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind("tcp://127.0.0.1:%s" % port)
    time.sleep(0.5)
    return sock


def sub_zmq_config(port):
    context = zmq.Context()
    print("Connecting to server on port %s" % port)
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://127.0.0.1:%s" % port)
    sock.setsockopt(zmq.SUBSCRIBE, b"super/dtm/command")
    sock.setsockopt(zmq.SUBSCRIBE, b"super/dtm/state")
    time.sleep(0.5)
    return sock


def poller_config(socket):
    poller = zmq.Poller()
    if len(socket) > 1:
        for sock in socket:
            poller.register(sock, zmq.POLLIN)
    else:
        poller.register(socket[0], zmq.POLLIN)
    return poller


def congestion_model_conf(max_speed, max_vehicle_number):
    # Antecedent/Consequent and universe definition variables
    jamLengthVehicle = ctrl.Antecedent(np.arange(0, max_vehicle_number + 2, 1), 'jamLengthVehicle')
    vehicleNumber = ctrl.Antecedent(np.arange(0, max_vehicle_number + 2, 1), 'vehicleNumber')
    occupancy = ctrl.Antecedent(np.arange(0, 101, 1), 'occupancy')
    meanSpeed = ctrl.Antecedent(np.arange(0, max_speed + 1, 1), 'meanSpeed')
    congestionLevel = ctrl.Consequent(np.arange(0, 101, 1), 'congestionLevel')

    # Membership Functions definition
    jamLengthVehicle.automf(3, 'quant')
    vehicleNumber.automf(3, 'quant')
    occupancy.automf(3, 'quant')
    meanSpeed.automf(3, 'quant')
    congestionLevel.automf(5, 'quant')

    # Graph the Membership Functions
    # jamLengthVehicle.view()
    # vehicleNumber.view()
    # occupancy.view()
    # meanSpeed.view()
    # congestionLevel.view()

    # Define the Expert Rules
    rules = [
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (jamLengthVehicle['high'] | meanSpeed['low']),
                  congestionLevel['higher']),
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (jamLengthVehicle['average'] | meanSpeed['average']),
                  congestionLevel['high']),
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (jamLengthVehicle['low'] | meanSpeed['high']),
                  congestionLevel['average']),
        ctrl.Rule((vehicleNumber['average'] | occupancy['average']) & (jamLengthVehicle['high'] | meanSpeed['low']),
                  congestionLevel['high']),
        ctrl.Rule(
            (vehicleNumber['average'] | occupancy['average']) & (jamLengthVehicle['average'] | meanSpeed['average']),
            congestionLevel['average']),
        ctrl.Rule((vehicleNumber['average'] | occupancy['average']) & (jamLengthVehicle['low'] | meanSpeed['high']),
                  congestionLevel['low']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (jamLengthVehicle['high'] | meanSpeed['low']),
                  congestionLevel['average']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (jamLengthVehicle['average'] | meanSpeed['average']),
                  congestionLevel['low']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (jamLengthVehicle['low'] | meanSpeed['high']),
                  congestionLevel['lower']),
    ]

    # Controller definition
    congestion_model = ctrl.ControlSystem(rules)
    congestion_measuring_sim = ctrl.ControlSystemSimulation(congestion_model)

    return congestion_measuring_sim, congestionLevel


def congestion_model_conf2(max_speed, max_vehicle_number):
    # Antecedent/Consequent and universe definition variables
    vehicleNumber = ctrl.Antecedent(np.arange(0, max_vehicle_number + 2, 1), 'vehicleNumber')
    occupancy = ctrl.Antecedent(np.arange(0, 101, 1), 'occupancy')
    meanSpeed = ctrl.Antecedent(np.arange(0, max_speed + 1, 1), 'meanSpeed')
    congestionLevel = ctrl.Consequent(np.arange(0, 101, 1), 'congestionLevel')

    # Membership Functions definition
    vehicleNumber.automf(3, 'quant')
    occupancy.automf(3, 'quant')
    meanSpeed.automf(3, 'quant')
    congestionLevel.automf(5, 'quant')

    # Graph the Membership Functions
    # jamLengthVehicle.view()
    # vehicleNumber.view()
    # occupancy.view()
    # meanSpeed.view()
    # congestionLevel.view()

    # Define the Expert Rules
    rules = [
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (meanSpeed['low']),
                  congestionLevel['higher']),
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (meanSpeed['average']),
                  congestionLevel['high']),
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (meanSpeed['high']),
                  congestionLevel['average']),
        ctrl.Rule((vehicleNumber['average'] | occupancy['average']) & (meanSpeed['low']),
                  congestionLevel['high']),
        ctrl.Rule(
            (vehicleNumber['average'] | occupancy['average']) & (meanSpeed['average']),
            congestionLevel['average']),
        ctrl.Rule((vehicleNumber['average'] | occupancy['average']) & (meanSpeed['high']),
                  congestionLevel['low']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (meanSpeed['low']),
                  congestionLevel['average']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (meanSpeed['average']),
                  congestionLevel['low']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (meanSpeed['high']),
                  congestionLevel['lower']),
    ]

    # Controller definition
    congestion_model = ctrl.ControlSystem(rules)
    congestion_measuring_sim = ctrl.ControlSystemSimulation(congestion_model)

    return congestion_measuring_sim, congestionLevel


def manage_flow(msg_in, movements, moves_detectors, moves_green, previous_moves_green, time_green_changed):
    # Function that saves the detectors and neighbor congestion info
    detector_id = msg_in["id"][-3:]
    mov_ids = []
    # with open("tpn_state.txt") as f_state:
    #     tpn_state = json.loads(f_state.read())
    #
    # moves_green = [int(i) for i in tpn_state.keys() if tpn_state[i] == "G"]
    print("Detector '", detector_id, "' value changed in lane '", msg_in['laneId'], "'")
    for mov in range(8):  # 8 movements
        if detector_id in moves_detectors[mov]:
            mov_ids.append(mov)
    print("Moves affected: ", mov_ids)
    for mov in mov_ids:
        if ((mov in moves_green) and (msg_in["dateObserved"] != time_green_changed[0])) \
                or ((mov in previous_moves_green) and (msg_in["dateObserved"] == time_green_changed[1])):
            movements[mov].set_jam_length_vehicle(detector_id, [msg_in["dateObserved"], msg_in["jamLengthVehicle"]])
            # TODO: Change speed to 14 when the measure = -1
            movements[mov].set_mean_speed(detector_id, [msg_in["dateObserved"], msg_in["meanSpeed"]])
            #print("Speed of: ", mov, " = ", msg_in["meanSpeed"])
        movements[mov].set_occupancy(detector_id, [msg_in["dateObserved"], msg_in["occupancy"]])
        movements[mov].set_vehicle_number(detector_id, [msg_in["dateObserved"], msg_in["vehicleNumber"]])

    return


def manage_accidents(msg_in, movements, accident_lanes):
    print("Accident status changes on street " + msg_in['laneId'])
    if msg_in["accidentOnLane"]:
        accident_lanes.append(msg_in['id'])
    else:
        accident_lanes.remove(msg_in['id'])

    acc_mov = []
    if msg_in['id'][24] == "n":
        acc_mov = [3, 6]
    elif msg_in['id'][24] == "e":
        acc_mov = [0, 5]
    elif msg_in['id'][24] == "s":
        acc_mov = [2, 7]
    elif msg_in['id'][24] == "w":
        acc_mov = [1, 4]

    date = datetime.datetime.utcnow().isoformat()
    for mov in acc_mov:
        movements[mov].accident[0] = msg_in["accidentOnLane"]
        movements[mov].accident[1] = date

    accident_msg = {
        "id": msg_in['id'],
        "type": "AccidentObserved",
        "laneId": msg_in['laneId'],
        "location": msg_in['location'],
        "dateObserved": datetime.datetime.utcnow().isoformat(),
        "accidentOnLane": msg_in["accidentOnLane"],  # It has to be configured
        "laneDirection": msg_in['laneDirection']
    }
    return accident_msg


def congestion_measure(congestion_measuring_sim, movement, time_current):
    congestion = 0.0
    mov_vehicle_num = movement.get_vehicle_number(time_current)
    mov_speed = movement.get_mean_speed(time_current)
    if mov_speed < 0:
        mov_speed = 14  # MAX_SPEED
    if mov_vehicle_num != 0:
        congestion_measuring_sim.input['jamLengthVehicle'] = movement.get_jam_length_vehicle(time_current)
        congestion_measuring_sim.input['vehicleNumber'] = mov_vehicle_num
        congestion_measuring_sim.input['occupancy'] = movement.get_occupancy(time_current)
        congestion_measuring_sim.input['meanSpeed'] = mov_speed
        # Crunch the numbers
        congestion_measuring_sim.compute()
        congestion = congestion_measuring_sim.output['congestionLevel']

    with open("log_files/dtm_%s_%d.log" % (intersection_id, run_num), "a") as f:
        f.write(str(time_current) + "; " +
                str(movement.id) + "; " +
                str(movement.get_jam_length_vehicle(time_current)) + "; " +
                str(mov_vehicle_num) + "; " +
                str(movement.get_occupancy(time_current)) + "; " +
                str(mov_speed) + "; " +
                str(congestion) + "\n")

    print("Congestion_", movement.id, " = ", congestion)
    # print("jamLengthVehicle = ", movement.get_jam_length_vehicle(time_current),
    #       "; vehicleNumber = ", mov_vehicle_num,
    #       "; occupancy = ", movement.get_occupancy(time_current),
    #       "; meanSpeed = ", mov_speed)
    # congestionLevel.view(sim=congestion_measuring_sim)

    return congestion


def congestion_measure2(congestion_measuring_sim, movement, time_current):
    congestion = 0.0
    mov_vehicle_num = movement.get_vehicle_number(time_current)
    mov_speed = movement.get_mean_speed(time_current)
    if mov_speed < 0:
        mov_speed = 14  # MAX_SPEED
    if mov_vehicle_num != 0:
        congestion_measuring_sim.input['vehicleNumber'] = mov_vehicle_num
        congestion_measuring_sim.input['occupancy'] = movement.get_occupancy(time_current)
        congestion_measuring_sim.input['meanSpeed'] = mov_speed
        # Crunch the numbers
        congestion_measuring_sim.compute()
        congestion = congestion_measuring_sim.output['congestionLevel']

    with open("log_files/dtm_%s_%d.log" % (intersection_id, run_num), "a") as f:
        f.write(str(time_current) + "; " +
                str(movement.id) + "; " +
                str(mov_vehicle_num) + "; " +
                str(movement.get_occupancy(time_current)) + "; " +
                str(mov_speed) + "; " +
                str(congestion) + "\n")

    print("Congestion_", movement.id, " = ", congestion)
    print("vehicleNumber = ", mov_vehicle_num,
          "; occupancy = ", movement.get_occupancy(time_current),
          "; meanSpeed = ", mov_speed)
    #congestionLevel.view(sim=congestion_measuring_sim)

    return congestion


def congestion_msg_set(msg_in, mov_cong):
    msg_sup = {
        "id": msg_in["id"],
        "type": "stateResult",
        "category": msg_in["category"],
        "state": {
            "value": mov_cong
        }
    }
    return msg_sup


def accident_msg_set(msg_in, mov_acc):
    msg_sup = {
        "id": msg_in["id"],
        "type": "stateChange",
        "category": {
            "value": ["mov_accident"]
        },
        "state": {
            "value": mov_acc
        }
    }
    return msg_sup


def run():
    # Set or Reset of run variables
    accident_lanes = []
    movements = {}  # dictionary of movements
    moves_green = []
    previous_moves_green = []

    # Create intersection Movements
    for i in inter_info.movements:
        movements[i] = intersections_classes.Movement(i, inter_info)
    print("Intersection Movements: ", movements)

    # Begging the run() log
    with open("log_files/dtm_%s_%d.log" % (intersection_id, run_num), "w") as f:
        f.write("time; movement_id; jam; vehicle_number; occupancy; mean_speed; my_congestion_level\n")
    with open("log_files/detect_%s_%d.log" % (intersection_id, run_num), "w") as f:
        f.write("time; time_det; detect_id; cars_number; occupancy; jam; mean_speed\n")
    with open("log_files/mg_%s_%d.log" % (intersection_id, run_num), "w") as f:
        f.write("time; state\n")

    # ----------------------------------------- DTM ready tu start -----------------------------------------
    print("DTM '%s' READY:" % intersection_id)
    while not start_flag:
        pass  # Do nothing waiting for the start signal

    # Set Petri Net Time, delay and step variables initial values to start
    time_0 = time.perf_counter()
    time_current = 0.0
    time_green_changed = [-1, -1]  # [change_to_green, change_to_NOT_green]

    # -------- Start the DTM --------
    print("\n\nStart the Intersection Petri Net:")
    while start_flag:
        # # Add accident in B at t = 30
        # if time_current == 30:
        #     my_accident_change = True
        #     msg_dic.append({
        #         "id": "intersection/0002/e2det/s03",
        #         "type": "AccidentObserved",
        #         "laneId": "436291016#3_3",
        #         "location": "here",
        #         "dateObserved": datetime.datetime.utcnow().isoformat(),
        #         "accidentOnLane": True,
        #         "laneDirection": "s-_wn_"
        #     })
        # # Remove accident in B at t = 300
        # if time_current == 300:
        #     my_accident_change = True
        #     msg_dic.append({
        #         "id": "intersection/0002/e2det/s03",
        #         "type": "AccidentObserved",
        #         "laneId": "436291016#3_3",
        #         "location": "here",
        #         "dateObserved": datetime.datetime.utcnow().isoformat(),
        #         "accidentOnLane": False,
        #         "laneDirection": "s-_wn_"
        #     })

        # ---- Manage SUMO-Detectors mqtt msgs received
        while msg_dic:
            msg_mqtt = msg_dic.pop(0)
            msg_id = msg_mqtt['id']
            msg_type = msg_mqtt['type']
            if "e2det" in msg_id:
                if msg_type == "TrafficFlowObserved":
                    manage_flow(msg_mqtt, movements, inter_info.m_detectors, moves_green, previous_moves_green, time_green_changed)
                    with open("log_files/detect_%s_%d.log" % (intersection_id, run_num), "a") as f:
                        f.write(str(time_current) + "; " +
                                str(msg_mqtt["dateObserved"]) + "; " +
                                str(msg_id) + "; " +
                                str(msg_mqtt["vehicleNumber"]) + "; " +
                                str(msg_mqtt["occupancy"]) + "; " +
                                str(msg_mqtt["jamLengthVehicle"]) + "; " +
                                str(msg_mqtt["meanSpeed"]) + "\n")
                elif msg_type == "AccidentObserved":
                    # TODO: Create the accident_msg
                    accident_msg = manage_accidents(msg_mqtt, movements, accident_lanes)
                    pub_socket.send_multipart([super_topic_accident, json.dump(accident_msg).encode()])

        # ---- Manage supervisor ZeroMQ msgs received
        poll = dict(poller.poll(2))
        if sub_socket in poll and poll[sub_socket] == zmq.POLLIN:
            [top, contents] = sub_socket.recv_multipart()
            msg_zmq = json.loads(contents.decode())
            print(msg_zmq)
            # Manage supervisor COMMANDS
            if b"command" in top:
                # Manage Congestion measure command
                if "mov_congestion" in msg_zmq["category"]["value"]:
                    msg_movements = list(msg_zmq["value"]["value"])
                    mov_cong = {}
                    print(time_current, "*** Measure congestion of movements: ", msg_movements, " ***")
                    for mov in msg_movements:
                        if mov in movements:  # Está de  más pues ya lo verificó el supervisor antes de enviar el msg
                            movements[mov].congestionLevel = congestion_measure2(congestion_measuring_sim, movements[mov], time_current)
                            mov_cong[mov] = movements[mov].congestionLevel
                    cong_data_msg = congestion_msg_set(msg_zmq, mov_cong)
                    print(cong_data_msg)
                    pub_socket.send_multipart([super_topic_congestion, json.dumps(cong_data_msg).encode()])

            # Manage Display Change
            elif b"state" in top:
                if "display" in msg_zmq["category"]["value"]:
                    msg_display = dict(msg_zmq["state"]["value"])  # dic -> {mov: "display"}. Ej: {2: "y", 7: "y"}
                    if moves_green:  # Display is going to change to a NOT green light
                        previous_moves_green = moves_green[:]
                        time_green_changed[1] = time_current
                    else:
                        previous_moves_green = []
                        time_green_changed[1] = -1
                    moves_green = []
                    for mov in msg_display:
                        mov_int = int(mov)
                        if msg_display[mov] == "G":
                            moves_green.append(mov_int)
                            movements[mov_int].reset_jam_length_vehicle()
                            movements[mov_int].reset_mean_speed()
                    if moves_green:  # Display changed to green light
                        time_green_changed[0] = time_current
                    else:
                        time_green_changed[0] = -1
                    with open("log_files/mg_%s_%d.log" % (intersection_id, run_num), "a") as f:
                        f.write(str(time_current) + "; " + str(moves_green) + "\n")
                    print("Moves Green : ", moves_green)

        # Update time_current
        if time.perf_counter() >= time_0 + time_current + 1:
            time_current += 1.0


if __name__ == '__main__':
    # Define the Global Variables
    start_flag = False
    run_num = 0
    with open("intersection/inter_id.txt", "r") as f:
        intersection_id = f.read().rstrip()
    with open("intersection/broker_ip.txt", "r") as f:
        mqtt_broker_ip = f.read().rstrip()  # PC Office: "192.168.0.196"; PC Lab: "192.168.5.95"; PC Home: "192.168.1.86"
    print("Intersection_ID: ", intersection_id)

    # Setup of the intersection
    inter_info = intersections_classes.Intersection(intersection_id, intersections_config.INTER_CONFIG_OPT)

    # Start mqtt connection
    client_intersection = mqtt_conf(mqtt_broker_ip)
    client_intersection.loop_start()  # Necessary to maintain connection

    # Define ZeroMQ topics
    super_topic_congestion = b"dtm/state"
    super_topic_accident = b"dtm/state"
    # Configure ZeroMQ sockets
    pub_socket = pub_zmq_config("5556")
    sub_socket = sub_zmq_config("5558")
    poller = poller_config([sub_socket])

    # Setup the congestion model
    congestion_measuring_sim, congestionLevel = congestion_model_conf2(inter_info.m_max_speed,
                                                                      inter_info.m_max_vehicle_number)
    # Reset Loop
    while True:
        msg_dic = []
        run()
        run_num += 1
        time.sleep(10)
        # Empty the zmq pipe
        poll = dict(poller.poll(20))
        while sub_socket in poll and poll[sub_socket] == zmq.POLLIN:
            [top, contents] = sub_socket.recv_multipart()
            poll = dict(poller.poll(20))
        time.sleep(20)
