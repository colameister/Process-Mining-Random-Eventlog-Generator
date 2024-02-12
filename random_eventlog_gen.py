import csv
import json
import logging
import random
from datetime import datetime, timedelta

# Konfigurieren des Logging-Moduls
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Pfad zur JSON-Datei, die die Revisionsnummer enthält
revision_file_path = 'revision_number.json'

# Versuche, die Revisionsnummer aus der Datei zu lesen
try:
    with open(revision_file_path, 'r') as file:
        data = json.load(file)
        revision_number = data['revision_number']
    logging.debug(f"Aktuelle Revisionsnummer geladen: {revision_number}")
except FileNotFoundError:
    # Falls die Datei nicht existiert, starte mit bestimmer Revision
    revision_number = 10
    logging.debug("Revision_file_path nicht gefunden.")

# Definierte logische Pfade
paths = {
    'Custom Pfad': [
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Paket zur Warenausgabe bringen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern"
    ],
    'Normaler Auftrag': [
        "Auftrag eingegangen", 
        "Ware aus Lager geholt", 
        "Qualitätskontrolle durchgeführt", 
        "Ware zum Versand vorbereitet", 
        "Ware versandt"
    ],
    'Eilauftrag': [
        "Auftrag eingegangen", 
        "Ware zur Produktion gebracht", 
        "Ware hergestellt", 
        "Ware verpackt", 
        "Schnellversand durchgeführt"
    ],
    'Rücksendung': [
        "Ware beim Kunden angekommen", 
        "Ware retourniert", 
        "Rücksendung geprüft", 
        "Reparatur durchgeführt", 
        "Ware erneut versandt"
    ],
    'Direktverkauf': [
        "Angebot erstellt", 
        "Vertragsverhandlungen geführt", 
        "Bestellung aufgenommen", 
        "Rechnung versendet", 
        "Zahlung erhalten", 
        "Ware direkt verkauft"
    ]
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

# Bevor die CSV-Datei erstellt wird, erhöhen wir die Revisionsnummer
revision_number += 1

# CSV-Datei öffnen und schreiben
with open(f"event_log_rev{revision_number}.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Fallnummer", "Aktivität", "Zeitstempel", "Ausführende Person", "Kosten (EUR)", "Transportiertes Gut", "Produktpreis (EUR)", "Kunde", "Abnahmeort", "Abgabeort"])

    for i in range(1, num_events + 1):
        case_number = str(i).zfill(3)
        selected_path = random.choice(list(paths.values()))
        # Für jeden Fall ein Produkt und einen Kunden auswählen
        product_tuple = random.choice(products)
        product_name, product_price = product_tuple
        customer = random.choice(customers)

        timestamp = datetime.now()
        for activity in selected_path:  # Durchlaufe die Aktivitäten des ausgewählten Pfades
            person = random.choice(people)
            pickup_location = random.choice(locations)
            delivery_location = random.choice(locations)

            # Speichern / Schreiben in CSV-Datei
            writer.writerow([case_number, activity, timestamp.strftime("%Y-%m-%d %H:%M:%S"), person, round(random.uniform(5.00, 100.00), 2), product_name, product_price, customer, pickup_location, delivery_location])

            # Zeitstempel für die nächste Aktivität inkrementieren
            timestamp += timedelta(minutes=random.randint(1, 60))

    # Speichern der aktualisierten Revisionsnummer in der JSON-Datei
    with open(revision_file_path, 'w') as file:
        json.dump({'revision_number': revision_number}, file)
        logging.debug(f"Revisionsnummer aktualisiert und gespeichert: {revision_number}")

# Fertigstellungslog :)
print(f"Die CSV-Datei 'event_log_rev{revision_number}.csv' wurde erfolgreich erstellt.")
logging.debug(f"CSV-Datei erfolgreich erstellt: event_log_rev{revision_number}.csv")