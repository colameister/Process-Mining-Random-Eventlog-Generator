import csv
import random
from datetime import datetime, timedelta

# Definierte logische Pfade
paths = {
    'Pfad1': ["Auftrag eingegangen", "Ware aus Lager geholt", "Ware zum Versand vorbereitet", "Ware versandt"],
    'Pfad2': ["Auftrag eingegangen", "Ware zur Produktion gebracht", "Ware hergestellt", "Ware verpackt", "Ware versandt"],
    # Fügen Sie bei Bedarf weitere Pfade hinzu
}

# Liste von Aktivitäten
activities = ["Auftrag eingegangen", "Ware aus Lager geholt", "Ware zur Produktion gebracht",
              "Ware hergestellt", "Ware verpackt", "Ware zum Versand vorbereitet", "Ware versandt",
              "Ware beim Kunden angekommen", "Rechnung erstellt", "Zahlung erhalten",
              "Ware retourniert", "Reparatur durchgeführt", "Ware umgeladen",
              "Qualitätskontrolle durchgeführt", "Ware gelagert", "Ware entsorgt",
              "Kundensupport angefragt", "Angebot erstellt", "Vertragsverhandlungen geführt",
              "Bestellung aufgenommen", "Rechnung versendet", "Rechnung bezahlt",
              "Ware wiederverkauft", "Personal geschult", "Marketingaktion durchgeführt",
              "Lieferanten kontaktiert", "Produktionsplanung erstellt", "Rückverfolgbarkeitsprüfung",
              "Verpackungsmaterial bestellt", "Werbekampagne gestartet", "Preisverhandlungen geführt"]

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
num_events = 100

# Revisionsnummer
revision_number = 7

# Initialisiere eine Liste, um zu verfolgen, welche Aktivitäten bereits in einem Fall aufgetreten sind
activities_per_case = {}

# CSV-Datei öffnen und schreiben
with open(f"event_log_rev{revision_number}.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Header schreiben
    writer.writerow(["Fallnummer", "Aktivität", "Zeitstempel", "Ausführende Person",
                     "Kosten (EUR)", "Transportiertes Gut", "Produktpreis (EUR)", "Kunde", "Abnahmeort", "Abgabeort"])

    # Ereignisse generieren
    for i in range(num_events):
        case_number = str(random.randint(1, 10)).zfill(3)  # Fallnummer ist nicht einzigartig
        selected_path = random.choice(list(paths.keys()))  # Einen Pfad zufällig auswählen
        for activity in paths[selected_path]:  # Durchlaufe die Aktivitäten des ausgewählten Pfades
            timestamp = (datetime.now() + timedelta(minutes=random.randint(1, 60))).strftime("%Y-%m-%d %H:%M:%S")
            person = random.choice(people)
            product, product_price = random.choice(products)
            customer = random.choice(customers)
            pickup_location = random.choice(locations)
            delivery_location = random.choice(locations)
            # Speichern / Schreiben in CSV-Datei
            writer.writerow([case_number, activity, timestamp, person, round(product_price, 2), product[0], product_price, customer, pickup_location, delivery_location])

# Fertigstellungslog :)
print(f"Die CSV-Datei 'event_log_rev{revision_number}.csv' wurde erfolgreich erstellt.")