import json

schedule = json.loads(open("schedule.json").read())["Schedule"]
matches = json.loads(open("matches.json").read())["MatchScores"]

matches_with_robots = {}

for match in schedule:
    match_number = match["matchNumber"]
    matches_with_robots[match_number] = {
        "match_info": match,
        "match_results": matches[match_number - 1],
    }
"""
netAlgaeCount = how many algae the alliance picked out of processor and scored in net
wallAlgaeCount =
    how many algae the other alliance missed net or kept in processor
    OR how many algae the alliance scored in processor with the other team not interacting with
algaePoints = netAlgaeCount * 4 + wallAlgaeCount * 6
"""

total_wall_algae = 0
total_net_algae = 0
match_algae = {}

for match_number, match in matches_with_robots.items():
    match_results = match["match_results"]
    blue = match_results["alliances"][0]
    red = match_results["alliances"][1]

    blue_net_algae = blue["netAlgaeCount"]
    blue_wall_algae = blue["wallAlgaeCount"]
    red_net_algae = red["netAlgaeCount"]
    red_wall_algae = red["wallAlgaeCount"]

    total_net_algae += blue_net_algae + red_net_algae
    total_wall_algae += blue_wall_algae + red_wall_algae

    match_algae[match_number] = {
        "blue": {
            "net": blue_net_algae,
            "processor": blue_wall_algae,
        },
        "red": {
            "net": red_net_algae,
            "processor": red_wall_algae,
        },
    }

print(f"Total net algae: {total_net_algae}")
print(f"Total procsesor algae: {total_wall_algae}")

# find match with highest net algae
max_net_algae = 0
max_net_match = None

for match_number, match in match_algae.items():
    blue_net = match["blue"]["net"]
    red_net = match["red"]["net"]

    if blue_net > max_net_algae:
        max_net_algae = blue_net
        max_net_match = match_number

    if red_net > max_net_algae:
        max_net_algae = red_net
        max_net_match = match_number

print(f"Match with highest net algae: {max_net_match} with {max_net_algae} algae")

hp_accuracy = {}

for match_number, match in match_algae.items():
    blue = match["blue"]
    red = match["red"]
    print("red", red["processor"], "match", match_number)
    print("ne 0", red["processor"] != 0)
    print("blue accuracy", red["processor"] - blue["net"])
    blue_accuracy = "Not attempted"
    if red["processor"] != 0:
        blue_accuracy = 1 - (red["processor"] - blue["net"]) / red["processor"]
    red_accuracy = "Not attempted"
    if blue["processor"] != 0:
        red_accuracy = 1 - (blue["processor"] - red["net"]) / blue["processor"]

    hp_accuracy[match_number] = {
        "blue": blue_accuracy,
        "red": red_accuracy,
        "blue_processor": blue["processor"],
        "red_processor": red["processor"],
        "blue_net": blue["net"],
        "red_net": red["net"],
    }

csv = "Match #,Blue HP Accuracy,Red HP Accuracy,Blue Processor Scored,Red Processor Scored,Blue Net Scored,Red Net Scored\n"

for match_number, match in hp_accuracy.items():
    csv += (
        f"{match_number},{match['blue']},{match['red']},"
        f"{match['blue_processor']},{match['red_processor']},{match['blue_net']},{match['red_net']}\n"
    )

open("hp_accuracy.csv", "w").write(csv)
