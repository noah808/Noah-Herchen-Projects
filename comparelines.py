import json


# Custom class Bet represents one type of bet a user can make
class Bet:
    def __init__(self, line, payout, lineType, company, team):
        self.line = line
        self.payout = payout
        self.lineType = lineType
        self.company = company
        self.team = team

    # For output / debugging purposes, return information about bet
    def __repr__(self):
        return str((self.company, self.lineType, self.team, self.line, self.payout))


# list of promising lines to return to user
possible_lines = []

# load lines from earlier api call
with open("data.json", "r") as f:
    data = json.load(f)

# loop through each game from the api call
for game in data["games"]:
    n_spreads = [] # Ex: -5.5
    p_spreads = [] # Ex: +5.5
    u_totals = [] # Ex: Under 40.5 total score
    o_totals = [] # Ex: Over 40.5 total score
    home_h2h = [] # Home moneyline odds
    away_h2h = [] # Away moneyline odds

    # For each game, go through every book
    for bookmaker in game["bookmakers"]:
        # For each book, go through each betting market
        for market in bookmaker["markets"]:
            # SPREADS
            if market["key"] == "spreads":
                for outcome in market["outcomes"]:
                    if outcome["point"] < 0: # Ex: -5.5
                        n_spreads.append(Bet(outcome["point"], outcome["price"], "spread", bookmaker["key"], outcome["name"]))
                    else: # Ex. +5.5
                        p_spreads.append(Bet(outcome["point"], outcome["price"], "spread", bookmaker["key"], outcome["name"]))
            # TOTALS
            elif market["key"] == "totals":
                for outcome in market["outcomes"]:
                    if outcome["name"] == "Under": # Ex: U 40.5
                        u_totals.append(Bet(outcome["point"], outcome["price"], "total", bookmaker["key"], outcome["name"]))
                    else: # Ex: O 40.5
                        o_totals.append(Bet(outcome["point"], outcome["price"], "total", bookmaker["key"], outcome["name"]))
            # MONEYLINE (h2h)
            else:
                for outcome in market["outcomes"]:
                    if outcome["name"] == game["home_team"]: # Home team moneyline
                        home_h2h.append(Bet(None, outcome["price"], "h2h", bookmaker["key"], outcome["name"]))
                    else: # Away team moneyline
                        away_h2h.append(Bet(None, outcome["price"], "h2h", bookmaker["key"], outcome["name"]))

    # Sort all unders in reverse (Ex: [U 41.5, U 40.5, U 39.5])
    u_totals = sorted(u_totals, key=lambda x:x.line, reverse=True)
    # Sort all overs in order (Ex: [O 39.5, O 40.5, O 41.5])
    o_totals = sorted(o_totals, key=lambda x: x.line)

    # Loop through unders and overs, looking for lines with space in between and odds that add up to greater than 0
    # Ex: Over 39.5 at -110, Under 40.5 at +120 (-110 + 120 = 10 > 0)
    # Sweet spot is at 40 points (Both lines hit)
    for u in u_totals:
        for o in o_totals:
            if u.line - o.line >= 1:
                if u.payout + o.payout >= 0:
                    possible_lines.append((u, o))

    # Sort all positive spreads in reverse (Ex: [+1.5, +2.5, +3.5])
    p_spreads = sorted(p_spreads, key=lambda x: x.line, reverse=True)
    # Sort all negative spreads in reverse (Ex: [-3.5, -2.5, -1.5])
    n_spreads = sorted(n_spreads, key=lambda x: x.line, reverse=True)

    # Loop through spreads, looking for lines with space in between and odds that add up to greater than 0
    # Ex: +3.5 at +120, -1.5 at -110 (120 - 110 = 10 > 0)
    # Sweet spot is when favored team wins by 2 or 3 points (Both lines hit)
    for p in p_spreads:
        for n in n_spreads:
            if p.line + n.line >= 1:
                if p.payout + n.payout >= 0:
                    possible_lines.append((p, n))

    # Sort absolute value of all home moneylines in reverse (Ex: [-130, -120, -110, +110])
    home_h2h = sorted(home_h2h, key=lambda x: abs(x.payout), reverse=True)
    # Sort absolute value of all away moneylines in order (Ex: [-110, +110, +120, +130])
    away_h2h = sorted(away_h2h, key=lambda x: abs(x.payout))

    # Loop through moneylines, looking for lines with moneylines that add up to more than 0
    # Ex. Home Team ML +110, Away team ML +130 (Either way make back more than you put in)
    # Putting even money on both teams means 5% return if home team wins, 15% if away team wins
    for h in home_h2h:
        for a in away_h2h:
            if h.payout + a.payout >= 1:
                possible_lines.append((h, a))

# Print to console today's risk-free bets
print(possible_lines)