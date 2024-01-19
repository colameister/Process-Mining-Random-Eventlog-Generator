import csv
import random
from datetime import datetime, timedelta

# Liste von Aktivitäten
activities = ["Auftrag erhalten", "Ware abholen", "Transport beginnen", "Transport beenden",
              "Produkt ins Lager legen", "Produkt aus Lager nehmen"]

# Liste von Personen ohne Umlaute
people = ["Max Mustermann", "Sarah Schmidt", "Lena Mueller", "Timo Wagner", "Lisa Schulz",
          "Jan Becker", "Laura Fischer", "Paul Zimmer", "Lisa Mueller", "Nico Schmidt",
          "Emma Weber", "Leonie Richter", "David Meyer", "Sophia Lang", "Luca Huber",
          "Mia Schmitt", "Jonas Richter", "Emilia Wagner", "Noah Becker", "Hannah Meyer"]

# Liste von Produkten und ihren Preisen
products = [("Produkt A", 100.00), ("Produkt B", 120.00), ("Produkt C", 80.00), ("Produkt D", 70.00),
            ("Produkt E", 150.00), ("Produkt F", 110.00), ("Produkt G", 95.00), ("Produkt H", 130.00),
            ("Produkt I", 90.00), ("Produkt J", 75.00), ("Produkt K", 110.00), ("Produkt L", 140.00),
            ("Produkt M", 95.00), ("Produkt N", 75.00), ("Produkt O", 120.00), ("Produkt P", 100.00),
            ("Produkt Q", 110.00), ("Produkt R", 130.00), ("Produkt S", 90.00), ("Produkt T", 85.00)]

# Liste von Kunden
customers = ["Firma1", "Firma2", "Firma3", "Firma4", "Firma5", "Firma6", "Firma7", "Firma8", "Firma9", "Firma10",
             "Firma11", "Firma12", "Firma13", "Firma14", "Firma15", "Firma16", "Firma17", "Firma18", "Firma19", "Firma20"]

# Liste von Abnahme- und Abgabeorten
locations = ["Lager A", "Lager B", "Lager C", "Lager D", "Lager E", "Lager F", "Lager G", "Lager H", "Lager I", "Lager J"]

# Anzahl der Ereignisse
num_events = 1000

# CSV-Datei öffnen und schreiben
with open("event_log.csv", mode="w", newline="") as file:
    writer = csv.writer(file)

    # Header schreiben
    writer.writerow(["Fallnummer", "Aktivität", "Zeitstempel", "Ausführende Person",
                     "Kosten (EUR)", "Transportiertes Gut", "Produktpreis (EUR)", "Kunde", "Abnahmeort", "Abgabeort"])

    # Ereignisse generieren
    for i in range(num_events):
        case_number = str(i + 1).zfill(3)  # Fallnummer mit führenden Nullen
        activity = random.choice(activities)
        timestamp = (datetime(2024, 1, 1, 8, 0, 0) + timedelta(minutes=i * 15)).strftime("%Y-%m-%dT%H:%M:%S")
        person = random.choice(people)
        cost = random.uniform(5.00, 100.00)
        product, product_price = random.choice(products)
        customer = random.choice(customers)
        pickup_location = random.choice(locations)
        delivery_location = random.choice(locations)

        # Schreiben Sie die Zeile in die CSV-Datei
        writer.writerow([case_number, activity, timestamp, person, cost, product, product_price, customer, pickup_location, delivery_location])

print("Die CSV-Datei wurde erfolgreich erstellt.")