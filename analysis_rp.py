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
print('total matches', len(matches_with_robots))

team_nums = []
counts = dict()

def handle(match_info, alliance):
    s = ""
    for t in match_info["teams"]:
        if alliance not in t["station"]:
            continue
        s += str(t["teamNumber"]) + ", "
        team_nums.append(t["teamNumber"])
        counts[t["teamNumber"]] = counts.get(t["teamNumber"], 0) + 1
    print(f'{match_info["matchNumber"]}: {s} {alliance}')

cnt = 0
for match_number, match in matches_with_robots.items():
    match_results = match["match_results"]
    blue = match_results["alliances"][0]
    red = match_results["alliances"][1]

    match_info = match["match_info"]

    if red["rp"] == 6:
        handle(match_info, "Red")
        cnt+=1
    if blue["rp"] == 6:
        handle(match_info, "Blue")
        cnt+=1

print(cnt)

for count in sorted(counts.items(), key=lambda it: it[1]):
    print(count)