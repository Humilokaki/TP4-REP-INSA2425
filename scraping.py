import socket
import ssl
import re
import json

HOST = 'understat.com'
PORT = 443

context = ssl.create_default_context()

paths = [
    '/league/Ligue_1',
    '/league/EPL',
    '/league/La_Liga',
    '/league/Serie_A',
    '/league/Bundesliga'
]

# json_pattern = re.compile(r'JSON\.parse\((.*?)\)') 
json_pattern = re.compile(r'var\ teamsData\ =\ JSON\.parse\((.*?)\)')

def extract_json_data_teamsData(json_data):
    extracted_data = []
    try:
        json_data = json.loads(json_data)
        for team_id, team_info in json_data.items():
            history = team_info.get('history', [])
            for match in history:
                # Modify this to extract the data you need
                match_data = {
                    'xG': match.get('xG'),
                    'xGA': match.get('xGA'),
                    'xpts': match.get('xpts'),
                    'pts': match.get('pts'),
                    'date': match.get('date'),
                    'scored': match.get('scored')
                }
                print(match_data)
                extracted_data.append(match_data)
    except json.JSONDecodeError as e:
        print("Error while extracting JSON data:", e)
    return extracted_data

for path in paths:

    client_socket = socket.create_connection((HOST, PORT))
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname=HOST)

    request_header = f'GET {path} HTTP/1.0\r\nHost: {HOST}\r\n\r\n'
    ssl_client_socket.sendall(request_header.encode('utf-8'))

    response = ''

    while True:
        recv = ssl_client_socket.recv(1024)
        if not recv:
            break
        response += recv.decode('utf-8')
    
    json_matches = json_pattern.findall(response)
    extracted_json_data = []
    
    for match in json_matches:
        try:
            match = match.strip("'").encode('utf-8').decode('unicode_escape')
            extracted_data = extract_json_data_teamsData(match)
            extracted_json_data.append(match)
        except:
            print(f'''Error while extracting json data from {path}''')

    
    # print(f"Extracted JSON data from {path}:\n", extracted_json_data)
    print("=" * 80)
    
    ssl_client_socket.close()

