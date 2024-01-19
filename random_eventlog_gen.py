import pandas as pd
import random
from datetime import datetime, timedelta

# module error:
# https://stackoverflow.com/questions/63388135/vs-code-modulenotfounderror-no-module-named-pandas

# Defining constants for the event log generation
NUM_CASES = 100  # Total number of cases
ACTIVITIES = ["Bestellung aufnehmen", "Ware kommissionieren", "Ware verpacken", "Ware versenden", "Qualitätskontrolle", "Sonderanfertigung"]
PATHS = {
    "Pfad A": ["Bestellung aufnehmen", "Ware kommissionieren", "Ware verpacken", "Ware versenden"],
    "Pfad B": ["Bestellung aufnehmen", "Ware kommissionieren", "Qualitätskontrolle", "Ware versenden"],
    "Pfad C": ["Bestellung aufnehmen", "Ware kommissionieren", "Sonderanfertigung", "Ware versenden"]
}
PATH_PROBABILITIES = [0.4, 0.35, 0.25]  # Probabilities for paths A, B, and C

# Additional attributes data
NAMES = ["Anna Schmidt", "Max Müller", "Julia Schneider", "Niklas Weber", "Sophia Bauer", "Lukas Wagner", "Mia Fischer", "Leon Zimmermann", "Emma Hoffmann", "Felix Schröder"]
PRODUCTS = ["Produkt " + str(i) for i in range(1, 21)]
PRODUCT_PRICES = {product: round(random.uniform(50, 500), 2) for product in PRODUCTS}
CUSTOMERS = ["Firma " + str(i) for i in range(1, 31)]
LOCATIONS = ["Standort " + str(i) for i in range(1, 11)]

# Function to generate a random path
def generate_path():
    path = random.choices(list(PATHS.values()), weights=PATH_PROBABILITIES, k=1)[0]
    return path

# Generating the event log
event_log = []
for case_id in range(1, NUM_CASES + 1):
    path = generate_path()
    timestamp = datetime.now()
    for activity in path:
        event_log.append({
            "Fallnummer": case_id,
            "Aktivität": activity,
            "Zeitstempel": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Name": random.choice(NAMES),
            "Kosten (EUR)": round(random.uniform(10, 100), 2),
            "Produkt": random.choice(PRODUCTS),
            "Produktpreis (EUR)": PRODUCT_PRICES[PRODUCTS[0]],
            "Kunde": random.choice(CUSTOMERS),
            "Abnahmeort": random.choice(LOCATIONS),
            "Abgabeort": random.choice(LOCATIONS)
        })
        # Increment timestamp by a random number of hours
        timestamp += timedelta(hours=random.randint(1, 5))

# Creating a DataFrame from the event log
event_log_df = pd.DataFrame(event_log)

# Display the first few rows of the dataframe
event_log_df.head()