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
    # Falls die Datei nicht existiert, starte mit bestimmter Revision
    revision_number = 10
    logging.debug("Revision_file_path nicht gefunden.")

# Definierte logische Pfade
paths = {
    'Custom Pfad 1': [  # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
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
    'Custom Pfad 2': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde noch nicht bezahlt)
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
        "Zahlungsabwicklung durchführen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 3': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde schon bezahlt)
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
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
}

# Liste von Produkten und ihren Preisen
products = [("Produkt A", 100.00), ("Produkt B", 120.00), ("Produkt C", 80.00), ("Produkt D", 70.00),
            ("Produkt E", 150.00), ("Produkt F", 110.00), ("Produkt G", 95.00), ("Produkt H", 130.00),
            ("Produkt I", 90.00), ("Produkt J", 75.00), ("Produkt K", 110.00), ("Produkt L", 140.00),
            ("Produkt M", 95.00), ("Produkt N", 75.00), ("Produkt O", 120.00), ("Produkt P", 100.00),
            ("Produkt Q", 110.00), ("Produkt R", 130.00), ("Produkt S", 90.00), ("Produkt T", 85.00)]

# Liste von Kunden
customers = [
    "Siemens",          # Elektrotechnik und Automatisierung
    "BASF",             # Chemie
    "Boeing",           # Luft- und Raumfahrt
    "Volkswagen",       # Automobil
    "Toyota",           # Automobil
    "General Electric", # Mischkonzern mit Schwerpunkt Technologie und Produktion
    "Airbus",           # Luft- und Raumfahrt
    "Daimler AG",       # Automobil
    "Bayer",            # Pharmazeutika und Agrarchemie
    "Intel",            # Halbleiter
    "General Motors",   # Automobil
    "Ford Motor",       # Automobil
    "Honda Motor",      # Automobil und Motorräder
    "Hitachi",          # Elektronik und Maschinenbau
    "Mitsubishi Electric", # Elektrotechnik
    "Nestlé",           # Lebensmittelverarbeitung
    "PepsiCo",          # Lebensmittelverarbeitung
    "Procter & Gamble", # Konsumgüter
    "Samsung Electronics", # Elektronik
    "Sony",             # Elektronik
]

# Liste von Abnahme- und Abgabeorten
locations = ["Lager A", "Lager B", "Lager C", "Lager D", "Lager E", "Lager F", "Lager G", "Lager H", "Lager I", "Lager J"]

# Kostenrahmen für jede Aktivität
activity_costs = {
    "Kunden-Daten aufnehmen": (2, 4),
    "Kunden-Daten in System übertragen": (1, 3),
    "Zahlvorgang abschließen": (2, 3),
    "Bestellung im System eintragen": (4, 9),
    "Lagerbestand überprüfen": (2, 8),
    "Auftragsabwicklung im System starten": (3, 6),
    "Artikel zusammenstellen": (8, 15),
    "Ware verpacken": (3, 8),
    "Gewicht prüfen": (1, 3),
    "Anzahl der Artikel überprüfen": (2, 5),
    "Verpackung prüfen": (2, 4),
    "Paket zur Warenausgabe bringen": (4, 9),
    "Paket an Kunde übergeben": (2, 3),
    "Bestellstatus im System ändern": (1, 3),
    "Zahlungsabwicklung durchführen": (2, 3),
    "Informationen an Transporteur übermitteln": (2, 6),
    "Paket an Transporteur übergeben": (6, 12),
    "Bezahlaufforderung an Kunde schicken": (1, 3),
    "Fehler im System eintragen": (5, 8),
    "Bestandsverwaltung informieren": (2, 4),
    "Versicherungs-Bescheinigung dazulegen": (1, 2),
    "Artikel bestellen": (6, 9),
    "Information an Kunde über verspätetet Lieferzeit verschicken": (1, 3),
    "Kunden-Daten abfragen (automatische Übertragung ins System)": (3, 7),
    "Rechnungsadesse aufnehmen": (1, 2),
    "Rechnungsadesse im System eintragen": (1, 3),
    "Fehlende Daten ermitteln": (5, 8),
    "Kunden bzgl. fehlender Daten anschreiben": (6, 12),
    "Vollständigkeit der Daten prüfen": (4, 8)
}

# Zuerst lege ich die Zuordnung der Aktivitäten zu den Abteilungen fest.
abteilungen_zuordnung = {
    "Auftragsannahme": [
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Rechnungsadesse aufnehmen",
        "Rechnungsadesse im System eintragen",
        "Fehlende Daten ermitteln",
        "Kunden bzgl. fehlender Daten anschreiben",
        "Vollständigkeit der Daten prüfen",
        "Kunden-Daten abfragen (automatische Übertragung ins System)"
    ],
    "Bestandsverwaltung": [
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken"
    ],
    "Lager": [
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Versicherungs-Bescheinigung dazulegen"
    ],
    "Qualitätskontrolle": [
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintragen",
        "Bestandsverwaltung informieren"
    ],
    "Warenausgang": [
        "Paket zur Warenausgabe bringen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern",
        "Zahlungsabwicklung durchführen",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bezahlaufforderung an Kunde schicken"
    ]
}

# Definition der Zuordnung von Abteilungen zu spezifischen Personen
abteilungen_personen_zuordnung = {
    "Auftragsannahme": ["Max Mustermann", "Sarah Schmidt", "Lena Mueller", "Timo Wagner", "Lisa Schulz"],
    "Bestandsverwaltung": ["Jan Becker", "Laura Fischer", "Paul Zimmer", "Lisa Mueller", "Nico Schmidt"],
    "Warenausgang": ["Emma Weber", "Leonie Richter", "David Meyer", "Sophia Lang", "Luca Huber"],
    "Lager": ["Mia Schmitt", "Jonas Richter"],
    "Qualitätskontrolle": ["Emilia Wagner", "Noah Becker", "Hannah Meyer"],
}

# Aktivitätsabhängige Ortszuordnungen
aktivitaetsabhaengige_orte = {
    "Kunden-Daten aufnehmen": ["Schalter"],
    "Kunden-Daten in System übertragen": ["online"],
    "Zahlvorgang abschließen": ["Schalter"],
    "Bestellung im System eintragen": ["online"],
    "Lagerbestand überprüfen": ["online"],
    "Auftragsabwicklung im System starten": ["online"],
    "Artikel zusammenstellen": ["Lager A", "Lager B", "Lager C"],
    "Ware verpacken": ["Lager C"],
    "Gewicht prüfen": ["Lager C"],
    "Anzahl der Artikel überprüfen": ["Lager C"],
    "Verpackung prüfen": ["Lager C"],
    "Paket zur Warenausgabe bringen": ["Warenausgabe 1", "Warenausgabe 2"],
    "Paket an Kunde übergeben": ["Warenausgabe 1", "Warenausgabe 2"],
    "Bestellstatus im System ändern": ["online"],
    "Zahlungsabwicklung durchführen": ["Warenausgabe 1", "Warenausgabe 2"],
    "Informationen an Transporteur übermitteln": ["online"],
    "Paket an Transporteur übergeben": ["Warenausgabe 3"],
    "Bezahlaufforderung an Kunde schicken": ["online"],
    "Fehler im System eintragen": ["online"],
    "Bestandsverwaltung informieren": ["online"],
    "Versicherungs-Bescheinigung dazulegen": ["Lager C"],
    "Artikel bestellen": ["online"],
    "Information an Kunde über verspätetet Lieferzeit verschicken": ["online"],
    "Kunden-Daten abfragen (automatische Übertragung ins System)": ["online"],
    "Rechnungsadesse aufnehmen": ["Schalter"],
    "Rechnungsadesse im System eintragen": ["online"],
    "Fehlende Daten ermitteln": ["online"],
    "Kunden bzgl. fehlender Daten anschreiben": ["online"],
    "Vollständigkeit der Daten prüfen": ["online"],
}

# Ich definiere eine Hilfsfunktion, um die ausführende Person basierend auf der Abteilung zu ermitteln.
def ermittle_person(abteilung):
    return random.choice(abteilungen_personen_zuordnung.get(abteilung, []))


# Ich definiere eine Hilfsfunktion, um die Abteilung basierend auf der Aktivität zu ermitteln.
def ermittle_abteilung(aktivitaet):
    for abteilung, aktivitaeten in abteilungen_zuordnung.items():
        if aktivitaet in aktivitaeten:
            return abteilung
    return "Unbekannt"


# Zuordnung von Warenausgabe für jede Fallnummer
warenausgabe_zuordnung = {}

def ermittle_ort(activity, case_number):
    if activity in ["Paket zur Warenausgabe bringen", "Paket an Kunde übergeben", "Zahlungsabwicklung durchführen"]:
        if case_number not in warenausgabe_zuordnung:
            warenausgabe_zuordnung[case_number] = random.choice(["Warenausgabe 1", "Warenausgabe 2"])
        return warenausgabe_zuordnung[case_number]
    else:
        ort_options = aktivitaetsabhaengige_orte.get(activity, ["Unbekannt"])
        return random.choice(ort_options)


# Anzahl der Ereignisse
num_events = 100

# Bevor die CSV-Datei erstellt wird, erhöhen wir die Revisionsnummer
revision_number += 1

# CSV-Datei öffnen und schreiben
with open(f"event_log_rev{revision_number}.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Aktualisierte Spaltenüberschriften
    writer.writerow(["Fallnummer", "Aktivität", "Zeitstempel", "Abteilung", "Ausführende Person", "Kosten (EUR)", "Kunde", "Transportiertes Gut", "Produktpreis (EUR)", "Ort"])

    for i in range(1, num_events + 1):
        case_number = str(i).zfill(3)
        selected_path = random.choice(list(paths.values()))
        product_tuple = random.choice(products)
        product_name, product_price = product_tuple
        product_price_for_csv = str(product_price).replace(".", ",")
        customer = random.choice(customers)

        timestamp = datetime.now()
        for activity in selected_path:
            abteilung = ermittle_abteilung(activity)
            person = ermittle_person(abteilung)
            min_cost, max_cost = activity_costs.get(activity, (1, 10))
            cost = round(random.uniform(min_cost, max_cost), 2)
            cost_for_csv = str(cost).replace(".", ",")
            ort = ermittle_ort(activity, case_number)

            # Aktualisierte Zeilendaten ohne "Abnahmeort" und "Abgabeort", stattdessen "Ort"
            writer.writerow([case_number, activity, timestamp.strftime("%Y-%m-%d %H:%M:%S"), abteilung, person, cost_for_csv, customer, product_name, product_price_for_csv, ort])

            timestamp += timedelta(minutes=random.randint(1, 60))

    with open(revision_file_path, 'w') as file:
        json.dump({'revision_number': revision_number}, file)
    logging.debug(f"Revisionsnummer aktualisiert und gespeichert: {revision_number}")

print(f"Die CSV-Datei 'event_log_rev{revision_number}.csv' wurde erfolgreich erstellt.")
logging.debug(f"CSV-Datei erfolgreich erstellt: event_log_rev{revision_number}.csv")