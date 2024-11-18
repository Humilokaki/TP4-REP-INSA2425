import socket
import ssl
import re
import json
import csv

HOST = "understat.com"
PORT = 443

context = ssl.create_default_context()

paths = [
    "/league/Ligue_1",
    "/league/EPL",
    "/league/La_Liga",
    "/league/Serie_A",
    "/league/Bundesliga",
    "/league/RFPL",
]

paths_complementary = [
    "/2014",
    "/2015",
    "/2016",
    "/2017",
    "/2018",
    "/2019",
    "/2020",
]

championships = {
    "/league/Ligue_1": "Ligue 1",
    "/league/EPL": "English Premier League",
    "/league/La_Liga": "La Liga",
    "/league/Serie_A": "Serie A",
    "/league/Bundesliga": "Bundesliga",
    "/league/RFPL": "Russian Premier League",
}

json_pattern = re.compile(r"var\ teamsData\ =\ JSON\.parse\((.*?)\)")


def extract_json_data_teamsData(json_data, championship):
    extracted_data = []
    try:
        json_data = json.loads(json_data)
        for team_id, team_info in json_data.items():
            id = team_info.get("id")
            title = team_info.get("title")
            history = team_info.get("history", [])
            for match in history:
                match_data = {
                    "id": id,
                    "title": title,
                    "championship": championship,
                    "h_a": match.get("h_a"),
                    "xG": match.get("xG"),
                    "xGA": match.get("xGA"),
                    "npxG": match.get("npxG"),
                    "npxGA": match.get("npxGA"),
                    "ppda": match.get("ppda"),
                    "ppda_allowed": match.get("ppda_allowed"),
                    "deep": match.get("deep"),
                    "deep_allowed": match.get("deep_allowed"),
                    "scored": match.get("scored"),
                    "missed": match.get("missed"),
                    "xpts": match.get("xpts"),
                    "result": match.get("result"),
                    "date": match.get("date"),
                    "wins": match.get("wins"),
                    "draws": match.get("draws"),
                    "loses": match.get("loses"),
                    "pts": match.get("pts"),
                    "npxGD": match.get("npxGD"),
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

        request_header = (
            f"GET {path}{path_complementary} HTTP/1.0\r\nHost: {HOST}\r\n\r\n"
        )
        ssl_client_socket.sendall(request_header.encode("utf-8"))

        response = ""

        while True:
            recv = ssl_client_socket.recv(1024)
            if not recv:
                break
            response += recv.decode("utf-8")

        json_matches = json_pattern.findall(response)
        for match in json_matches:
            try:
                match = match.strip("'").encode("utf-8").decode("unicode_escape")
                extracted_data = extract_json_data_teamsData(match, championships[path])
                extracted_json_data.extend(
                    extracted_data
                )  # Append the structured data directly
            except Exception as e:
                print(f"Error while extracting JSON data from {path}: {e}")

        print("=" * 80)

        ssl_client_socket.close()

# Writing data to CSV
output_file = "data.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Team ID",
            "Team Name",
            "Championship",
            "h_a",
            "xG",
            "xGA",
            "npxG",
            "npxGA",
            "ppda_att",
            "ppda_def",
            "ppda_allowed_att",
            "ppda_allowed_def",
            "deep",
            "deep_allowed",
            "scored",
            "missed",
            "xpts",
            "result",
            "date",
            "wins",
            "draws",
            "loses",
            "pts",
            "npxGD",
        ]
    )

    for match_data in extracted_json_data:  # Loop over structured data
        writer.writerow(
            [
                match_data["id"],
                match_data["title"],
                match_data["championship"],
                match_data["h_a"],
                match_data["xG"],
                match_data["xGA"],
                match_data["npxG"],
                match_data["npxGA"],
                match_data["ppda"]["att"],
                match_data["ppda"]["def"],
                match_data["ppda_allowed"]["att"],
                match_data["ppda_allowed"]["def"],
                match_data["deep"],
                match_data["deep_allowed"],
                match_data["scored"],
                match_data["missed"],
                match_data["xpts"],
                match_data["result"],
                match_data["date"],
                match_data["wins"],
                match_data["draws"],
                match_data["loses"],
                match_data["pts"],
                match_data["npxGD"],
            ]
        )

print(f"Data successfully written to {output_file}")
