from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import json

# Helper method to convert unicode minus to '-' (minus symbol)
def normalize_odds(odds):
    return odds.replace('\u2212', '-')

# Setup headless Chrome
options = webdriver.ChromeOptions()
# options.add_argument('--headless') -> not headless for user to visualize what's happening
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Instantiate Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# DraftKings NFL page
url = "https://sportsbook.draftkings.com/leagues/football/nfl-preseason"
driver.get(url)

# Use selenium webdriver to find nfl market odds (wait for all pages to load)
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cb-market__button-odds")))
except Exception as e:
    print(f"Page did not load completely within the specified time. {e}")

# Get fully rendered HTML
html = driver.page_source
with open("draftkings_snapshot.html", "w") as f:
    f.write(html)

# Print status of page
print("Contains '/event/' links:", "/event/" in html)
print("Count a[href^='/event/'] via BeautifulSoup:", len(BeautifulSoup(html, "html.parser").select("a[href^='/event/']")))
print("Has geo/consent text?:", any(x in html.lower() for x in [
    "verify your location",
    "not available in your location",
    "accept all cookies"
]))

# Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Create games dictionary
games = {"matchups":[]}

# Find all game blocks
game_blocks = soup.select("div.cb-market__template")

# Create Dummy variable to track matchups in dictionary
simple_count = 0

# Loop through teams from games found on DraftKings
for block in game_blocks:
    try:
        # Team name section
        team_name_tag = block.select_one("span.cb-market__label-inner")
        team_name = team_name_tag.text.strip() if team_name_tag else "Unknown Team"

        # Odds and lines section
        odds_tags = block.select("span.cb-market__button-odds")
        points_tags = block.select("span.cb-market__button-points")

        # Clean up odds and lines
        odds = [tag.text.strip() for tag in odds_tags]
        points = [tag.text.strip() for tag in points_tags]

        # Format and add games to dictionary
        spread = ""
        ou = ""
        ml = ""
        if len(odds) == 3 and len(points) == 2:
            spread = points[0]+" at "+normalize_odds(odds[0])
            ou = points[1]+" at "+normalize_odds(odds[1])
            ml = normalize_odds(odds[2])
        elif len(odds) == 2 and len(points) == 1:
            ou = points[0] + " at " + normalize_odds(odds[0])
            ml = normalize_odds(odds[1])
        else:
            print(f"Problem with odds and points. {odds}, {points}")

        # Match up games between teams in dictionary
        if simple_count % 2 == 0:
            games["matchups"].append(
                {
                    "Matchup": str(team_name) + " at ",
                    str(team_name):
                        {
                            "Spread": spread,
                            "Over": ou,
                            "Moneyline": ml
                        }
                }
            )
        else:
            games["matchups"][-1]["Matchup"] = games["matchups"][-1]["Matchup"] + str(team_name)
            games["matchups"][-1][str(team_name)] = {
                            "Pitcher": pitcher,
                            "Spread": spread,
                            "Under": ou,
                            "Moneyline": ml
                        }

        simple_count += 1

    except Exception as e:
        print(f"Error parsing block: {e}")

# Save to JSON
with open("dk_nfl.json", "w") as f:
    json.dump(games, f, indent=2)

# Print dictionary to console
print("Extracted games:", json.dumps(games, indent=2))