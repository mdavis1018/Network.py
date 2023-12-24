"""
File:    tactego.py
Author:  Marcus Davis
Date:    12/17/2023
Section: 58-Dis(8021)
E-mail:  marcusd2@umbc.edu
Description: creates a phone network. This is my file without the extra credit.
"""

import json


HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'


def connect_switchboards(switchboards, area_1, area_2):
    """
    Connects two switchboards by adding them to each other's connections list.
    :param switchboards: Dictionary representing the phone network.
    :param area_1: Area code of the first switchboard.
    :param area_2: Area code of the second switchboard.
    """

    # The key "connections" doesn't exist or is an empty list
    if "connections" not in switchboards[area_1] or not switchboards[area_1]["connections"]:
        switchboards[area_1]["connections"] = []

    switchboards[area_1]["connections"].append(
        area_2)  # add to connections list

    if "connections" not in switchboards[area_2] or not switchboards[area_2]["connections"]:
        switchboards[area_2]["connections"] = []

    switchboards[area_2]["connections"].append(area_1)
    print(f"{area_1} connected to {area_2}")
    pass


def add_switchboard(switchboards, area_code):
    """
    Adds a new switchboard to the network.
    :param switchboards: Dictionary representing the phone network.
    :param area_code: Area code of the new switchboard.
    """

    switchboards[area_code] = {}
    switchboards[area_code]["phone numbers"] = {}
    switchboards[area_code]["connections"] = []
    print(f"Switchboard {area_code} added")
    pass


def add_phone(switchboards, area_code, phone_number):
    """
    Adds a new phone number to a switchboard.
    :param switchboards: Dictionary representing the phone network.
    :param area_code: Area code of the switchboard.
    :param phone_number: Phone number to be added.
    """

    # Check if the area code exists in switchboards
    if area_code not in switchboards:
        print(
            f"Area code {area_code} does not exist. Add the switchboard first.")
        return

    # Convert the phone number to an integer
    phone_number = str(phone_number)

    # Initialize the dictionary for the phone number
    switchboards[area_code]["phone numbers"][phone_number] = {
        "on call": False,
        "otp": []
    }

    print(f"{area_code}-{phone_number} added to {area_code}")


def save_network(switchboards, file_name):
    """
    Saves the phone network to a JSON file.
    :param switchboards: Dictionary representing the phone network.
    :param file_name: Name of the file to save the network to.
    """

    # Convert keys back to strings before saving
    switchboards_str_keys = {
        str(key): value for key, value in switchboards.items()}

    with open(file_name, 'w') as json_file:
        json.dump(switchboards_str_keys, json_file)


def load_network(file_name):
    """
    Loads a phone network from a JSON file.
    :param file_name: Name of the file to load the network from.
    :return: Loaded phone network.
    """

    with open(file_name, 'r') as file:
        loaded_network_str_keys = json.load(file)

    # Convert keys back to integers after loading
    loaded_network = {int(key): value for key,
                      value in loaded_network_str_keys.items()}
    print("Loaded file")
    return loaded_network
    pass


def recursive_start_call(switchboards, start_area, start_number, end_area, end_number, searched=None):
    """
    Recursively checks if a call can be initiated between two phone numbers.
    :param switchboards: Dictionary representing the phone network.
    :param start_area: Area code of the starting phone.
    :param start_number: Phone number of the starting phone.
    :param end_area: Area code of the destination phone.
    :param end_number: Phone number of the destination phone.
    :param searched: List of already searched switchboards.
    :return: True if the call can be initiated, False otherwise.
    """

    if not searched:
        searched = []

    searched.append(start_area)

    if start_area == end_area: #if a path is found return true to be used in start_call function
        return True

    if "connections" in switchboards[start_area]:
        for node in switchboards[start_area]["connections"]:
            if node not in searched:
                if recursive_start_call(switchboards, node, start_number, end_area, end_number, searched):
                    return True
    return False


def start_call(switchboards, start_area, start_number, end_area, end_number):
    """
    Initiates a call between two phone numbers.
    :param switchboards: Dictionary representing the phone network.
    :param start_area: Area code of the starting phone.
    :param start_number: Phone number of the starting phone.
    :param end_area: Area code of the destination phone.
    :param end_number: Phone number of the destination phone.
    """
    start_number = str(start_number)
    end_number = str(end_number)

    # conditions for a call to be a fail
    if switchboards[start_area]["phone numbers"][start_number]["on call"]:
        print(f"Error: {start_area}{start_number} is already on call.")
        return
    elif switchboards[end_area]["phone numbers"][end_number]["on call"]:
        print(f"Error: {end_area}{end_number} is already on call.")
        return

    if recursive_start_call(switchboards, start_area, start_number, end_area, end_number): #if my recusive call returns true (finds a path)
        switchboards[start_area]["phone numbers"][start_number]["on call"] = True
        switchboards[end_area]["phone numbers"][end_number]["on call"] = True
        print(
            f"{start_area}{start_number} and {end_area}{end_number} are now connected.")
        start_otp_list = [
            int(f"{start_area}{start_number}"),
            int(f"{end_area}{end_number}")
        ]
        end_otp_list = [
            int(f"{end_area}{end_number}"),
            int(f"{start_area}{start_number}")
        ]

        # add the two phone numbers into their respective otp lists
        switchboards[start_area]["phone numbers"][start_number]["otp"].append(
            start_otp_list)
        switchboards[end_area]["phone numbers"][end_number]["otp"].append(
            end_otp_list)
        print(
            f"... Call Connected Succesfully between {start_area}{start_number} and {end_area}{end_number} ")
    else:
        print(
            f"{start_area}{start_number} and {end_area}{end_number} could not connect.")


def end_call(switchboards, start_area, start_number):
    """
    Ends an ongoing call for a phone number.
    :param switchboards: Dictionary representing the phone network.
    :param start_area: Area code of the phone ending the call.
    :param start_number: Phone number ending the call.
    """

    start_number = str(start_number)
    for i in range(len(switchboards[start_area]["phone numbers"][start_number]["otp"])):
        # updating switchboard to get rid of information related to connected call
        connected_full_number = str(
            switchboards[start_area]["phone numbers"][start_number]["otp"][i][1])
        connected_area = int(connected_full_number[:3])
        connected_number = str(connected_full_number[3:10])
        switchboards[connected_area]["phone numbers"][connected_number]["on call"] = False
        del switchboards[connected_area]["phone numbers"][connected_number]["otp"][i]
        switchboards[start_area]["phone numbers"][start_number]["on call"] = False
        del switchboards[start_area]["phone numbers"][start_number]["otp"][i]
        print("Hanging up...Connection Terminated.")

    pass


def display(switchboards):
    """
    Displays the current state of the phone network, including switchboard connections and phone status.
    :param switchboards: Dictionary representing the phone network.
    """

    for area_code, info in switchboards.items():
        print(f"Switchboard with area code: {area_code}")

        # Display trunk lines
        trunk_lines = info.get('connections', [])
        print("    Trunk lines are:")
        if trunk_lines:
            for trunk_line in trunk_lines:
                print(f"      Trunk line connection to: {trunk_line}")
        else:
            print("      None")

        print("    Local phone numbers are:")
        for phone_number, phone_info in info.get('phone numbers', {}).items():
            if phone_info.get('on call', False):
                connected_numbers = [
                    f"{connected_area}-{connected_number}"
                    for connected_area, connected_number in phone_info.get('otp', [])
                ]
                if connected_numbers:
                    connected_info = f"connected to {connected_numbers[0][11:14]}-{connected_numbers[0][14:]}"
                    print(
                        f"      Phone with number: {phone_number} is in use, {connected_info}.")
                else:
                    print(
                        f"      Phone with number: {phone_number} is in use, not connected.")
            else:
                print(
                    f"      Phone with number: {phone_number} is not in use.")
        print()


if __name__ == '__main__':
    switchboards = {}
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            connect_switchboards(switchboards, area_1, area_2)
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            add_switchboard(switchboards, int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))
            add_phone(switchboards, area_code, phone_number)
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            save_network(switchboards, split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            switchboards = load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))
            start_call(switchboards, src_area_code,
                       src_number, dest_area_code, dest_number)

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))
            end_call(switchboards, area_code, number)

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            display(switchboards)

        s = input('Enter command: ')
