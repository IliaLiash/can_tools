import time
import can
import curses

can_bus = can.interface.Bus(bustype='kvaser', channel=1, bitrate=500000)

prev_messages = {}

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

max_y, max_x = stdscr.getmaxyx()

id_data_list = []

while True:
    msg = can_bus.recv()

    if msg.arbitration_id in prev_messages:
        prev_msg = prev_messages[msg.arbitration_id]

        if msg.data != prev_msg.data:
            new_data = []

            for i in range(len(msg.data)):
                if msg.data[i] != prev_msg.data[i]:
                    new_data.append("*" + f"{msg.data[i]:02X}" + "*")
                else:
                    new_data.append(f"{msg.data[i]:02X}")

            for i, id_data in enumerate(id_data_list):
                if id_data[0] == msg.arbitration_id:
                    id_data_list[i] = (msg.arbitration_id, new_data)

        id_index = None
        for i, id_data in enumerate(id_data_list):
            if id_data[0] == msg.arbitration_id:
                id_index = i
                break

        if id_index is not None:
            id_data = id_data_list[id_index]
            data_str = ' '.join(id_data[1])
            try:
                stdscr.addstr(id_index, 0, f"ID: {msg.arbitration_id:04X} | Data: {data_str}")
            except curses.error:
                pass
    else:
        data_str = ' '.join([f"{d:02X}" for d in msg.data])
        id_data_list.append((msg.arbitration_id, data_str))

    prev_messages[msg.arbitration_id] = msg

    stdscr.refresh()
