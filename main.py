import datetime
import sys, json
import discord_msg

fleet_doctrines = {}
clean_discord_messages = []
year_month = []


def get_ship_doctrine_name(msg, index, ship_doctrine_descriptor="None") -> str:
    """
    Gets ship doctrine name: clean
    :param msg: the discord message content in question
    :param index: index where we start extracting the str
    :return: name of doctrine detected
    """
    doctrine_name_string = ""
    combined_index_start = index + len(ship_doctrine_descriptor) + 2
    counter = 0 + combined_index_start
    for character in msg[combined_index_start:]:
        if character is not '\n':
            doctrine_name_string += str(character)
        else:
            break

    return doctrine_name_string


def parse_discord_msg(fleet_doctrine_list: dict, discord_msg: dict, clean_message_descriptor= ["Ship Doctrine"]) -> dict:
    """
    Parses The Discord message
    :param fleet_doctrine_list:
    :param discord_msg:
    :return:
    """

    # state case - we find it in generic fleet ping
    for clean_message_filter in clean_message_descriptor:

        if clean_message_filter in discord_msg['content'] and discord_msg['id'] not in clean_discord_messages:
            if clean_message_filter == "Ship Doctrine":
                clean_discord_messages.append(discord_msg['id'])
                ship_doctrine_name = get_ship_doctrine_name(discord_msg['content'], discord_msg['content'].find("Ship Doctrine"),
                                       ship_doctrine_descriptor=clean_message_filter)
                # datetime.datetime.strptime(discord_msg['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
            else:
                ship_doctrine_name = clean_message_filter
            # Check dict
            try:
                discord_msg_timestamp = datetime.datetime.strptime(discord_msg['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                discord_msg_timestamp = datetime.datetime.strptime(discord_msg['timestamp'], '%Y-%m-%dT%H:%M:%S%z')
            timestamp_str = datetime.datetime.strftime(discord_msg_timestamp, '%Y_%m')
            if ship_doctrine_name in fleet_doctrine_list.keys() and (ship_doctrine_name is not "" or ship_doctrine_name is not " "):
                if timestamp_str not in fleet_doctrine_list[ship_doctrine_name]:
                    fleet_doctrine_list[ship_doctrine_name][timestamp_str] = 1
                else:
                    fleet_doctrine_list[ship_doctrine_name][timestamp_str] += 1
            else:
                fleet_doctrine_list[ship_doctrine_name] = {}
                fleet_doctrine_list[ship_doctrine_name][timestamp_str] = 1

            if timestamp_str not in year_month:
                year_month.append(timestamp_str)

        else:
            pass
    return fleet_doctrine_list


if __name__ == '__main__':
    """
    usage is python3 main.py "name_of_discord_file_to_check_TEST_Alliance_Pings"
    """
    with open(sys.argv[1], 'r') as file_to_be_read:
        asdf = json.load(file_to_be_read)
        for msg in asdf['messages']:
            parse_discord_msg(fleet_doctrines, discord_msg=msg)

        #For dirty messages
        for msg in asdf['messages']:
            parse_discord_msg(fleet_doctrines, discord_msg=msg,
                              clean_message_descriptor=[*fleet_doctrines.keys()])
    for yearmonth_tocheck in year_month:
        with open('doctrine_list_count_{}.csv'.format(yearmonth_tocheck),'w') as write_file:
            for k, v in sorted(fleet_doctrines.items()):
                if yearmonth_tocheck in v.keys():
                    msg_str = "{} \t {}\n".format(k, v[yearmonth_tocheck])
                    print(msg_str)
                    write_file.write(msg_str)
    pass

