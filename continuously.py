import can
from colorama import Fore, Style, init

init()

can_bus = can.interface.Bus(bustype='kvaser', channel=1, bitrate=500000)

prev_messages = {}

while True:
    msg = can_bus.recv()

    if msg.arbitration_id in prev_messages:
        prev_msg = prev_messages[msg.arbitration_id]

        if msg.data != prev_msg.data:
            new_data = []

            for i in range(len(msg.data)):
                if msg.data[i] != prev_msg.data[i]:
                    new_data.append(Fore.RED + f"{msg.data[i]:02X}" + Style.RESET_ALL)
                else:
                    new_data.append(f"{msg.data[i]:02X}")

            print(f"ID: {msg.arbitration_id:04X} | Data: {' '.join(new_data)}")
    else:
        data_str = ' '.join([f"{d:02X}" for d in msg.data])
        print(f"ID: {msg.arbitration_id:04X} | Data: {data_str}")

    prev_messages[msg.arbitration_id] = msg