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

robot_key_stats = {}

for match_number, match in matches_with_robots.items():
    for team in match["match_info"]["teams"]:
        team_number = team["teamNumber"]
        if team_number not in robot_key_stats:
            robot_key_stats[team_number] = []
        alliance_data = match["match_results"]["alliances"][
            "Red" in team["station"] and 1 or 0
        ]
        robot_key_stats[team_number].append(
            {
                "match_number": match_number,
                "climb_state": alliance_data["endGameRobot" + team["station"][-1]],
                "auto_line_state": alliance_data["autoLineRobot" + team["station"][-1]],
            }
        )

csv = ""
robots_never_leave = []

for team_number, team_data in robot_key_stats.items():
    print(f"Team {team_number}:")
    csv += f"{team_number},\n"
    percent_auto_leave = sum(
        [match_data["auto_line_state"] == "Yes" for match_data in team_data]
    ) / len(team_data)
    if percent_auto_leave == 0:
        robots_never_leave.append(team_number)
    for match_data in team_data:
        csv += f"{match_data['match_number']},{match_data['climb_state']},{match_data['auto_line_state']},\n"
        print(
            f"Match {match_data['match_number']}: Climb state: {match_data['climb_state']}, Auto line state: {match_data['auto_line_state']}"
        )
    csv += ",\n"
    print()

print("robots not leaving auto line:", robots_never_leave)
print(
    "% of total robots",
    round(len(robots_never_leave) / len(robot_key_stats) * 100, 2),
    f"({len(robots_never_leave)} out of {len(robot_key_stats)})",
)

print(csv)
