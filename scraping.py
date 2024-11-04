import socket
import ssl
import re
import json
import csv

HOST = 'understat.com'
PORT = 443

context = ssl.create_default_context()

paths = [
    '/league/Ligue_1',
    '/league/EPL',
    # '/league/La_Liga',
    # '/league/Serie_A',
    # '/league/Bundesliga'
]

paths_complementary = [
    '/2014',
    # '/2015',
    # '/2016',
    # '/2017',
    # '/2018',
    # '/2019',
    # '/2020',
    # '/2021',
    # '/2022',
    # '/2023',
    # '/2024'
]

championships = {
    '/league/Ligue_1': 'Ligue 1',
    '/league/EPL': 'English Premier League',
    # Additional championships can be added here
}

json_pattern = re.compile(r'var\ teamsData\ =\ JSON\.parse\((.*?)\)')

def extract_json_data_teamsData(json_data, championship):
    extracted_data = []
    try:
        json_data = json.loads(json_data)
        for team_id, team_info in json_data.items():
            id = team_info.get('id')
            title = team_info.get('title')
            history = team_info.get('history', [])
            for match in history:
                match_data = {
                    'id': id,
                    'title': title,
                    'championship': championship,
                    'xG': match.get('xG'),
                    'xGA': match.get('xGA'),
                    'xpts': match.get('xpts'),
                    'pts': match.get('pts'),
                    'date': match.get('date'),
                    'scored': match.get('scored')
                }
                extracted_data.append(match_data)
    except json.JSONDecodeError as e:
        print("Error while extracting JSON data:", e)
    return extracted_data

extracted_json_data = []
for path in paths:
    for path_complementary in paths_complementary:
        print(f"Requesting data from {path}{path_complementary}")

        client_socket = socket.create_connection((HOST, PORT))
        ssl_client_socket = context.wrap_socket(client_socket, server_hostname=HOST)

        request_header = f'GET {path}{path_complementary} HTTP/1.0\r\nHost: {HOST}\r\n\r\n'
        ssl_client_socket.sendall(request_header.encode('utf-8'))

        response = ''

        while True:
            recv = ssl_client_socket.recv(1024)
            if not recv:
                break
            response += recv.decode('utf-8')

        json_matches = json_pattern.findall(response)

        for match in json_matches:
            try:
                match = match.strip("'").encode('utf-8').decode('unicode_escape')
                extracted_data = extract_json_data_teamsData(match, championships[path])
                extracted_json_data.extend(extracted_data)  # Append the structured data directly
            except Exception as e:
                print(f"Error while extracting JSON data from {path}: {e}")

        print("=" * 80)

        ssl_client_socket.close()

# Writing data to CSV
output_file = 'data.csv'

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Team ID', 'Team Name', 'Championship', 'date', 'xG', 'xGA', 'xpts', 'pts', 'scored'])
    
    for match_data in extracted_json_data:  # Loop over structured data
        writer.writerow([match_data['id'], match_data['title'], match_data['championship'], 
                         match_data['date'], match_data['xG'], match_data['xGA'], 
                         match_data['xpts'], match_data['pts'], match_data['scored']])

print(f"Data successfully written to {output_file}")
