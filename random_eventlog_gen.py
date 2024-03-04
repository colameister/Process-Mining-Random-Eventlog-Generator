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
    'Custom Pfad 4': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde noch nicht bezahlt)
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
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
     'Custom Pfad 5': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde noch nicht bezahlt, dopplete Nachfrage notwendig)
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
        "Bezahlaufforderung an Kunde schicken",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 6': [  # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung) (Kunde schon bezahlt)
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
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
   'Custom Pfad 7': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung) (Kunde noch nicht bezahlt)
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
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
    'Custom Pfad 8': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung nein) (Kunde schon bezahlt)
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
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
    'Custom Pfad 9': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung nein) (Kunde noch nicht bezahlt)
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
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 10': [  # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert über 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Paket zur Warenausgabe bringen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 11': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert über 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde noch nicht bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Paket zur Warenausgabe bringen",
        "Zahlungsabwicklung durchführen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 12': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert über EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 13': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Alle Artikel vorhanden) (Warenwert über 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde noch nicht bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
     'Custom Pfad 14': [  # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Nicht alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
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
    'Custom Pfad 15': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Nicht alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde noch nicht bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
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
    'Custom Pfad 16': [  # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Nicht alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
    'Custom Pfad 17': [ # (Kunde bestellt im Laden) (Kunde bezahlt direkt) (Nicht alle Artikel vorhanden) (Warenwert über EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Zahlvorgang abschließen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 18': [  # (Kunde bestellt über Online Shop) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten abfragen (automatische Übertragung ins System)",
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
     'Custom Pfad 19': [ # (Kunde bestellt über Online Shop) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde noch nicht bezahlt, dopplete Nachfrage notwendig)
        "Kunden-Daten abfragen (automatische Übertragung ins System)",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Bezahlaufforderung an Kunde schicken",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 20': [  # (Kunde bestellt über Online-Shop) (Alle Artikel vorhanden) (Warenwert über 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten abfragen (automatische Übertragung ins System)",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Paket zur Warenausgabe bringen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 21': [  # (Kunde bestellt über Online-Shop) (Nicht alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten abfragen (automatische Übertragung ins System)",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
    'Custom Pfad 22': [ # (Kunde bestellt über Online Shop) (Nicht alle Artikel vorhanden) (Warenwert über EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde schon bezahlt)
        "Kunden-Daten abfragen (automatische Übertragung ins System)",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
     'Custom Pfad 23': [  # (Kunde bestellt im Laden) (Kunde bezahlt nicht direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Rechnungsadesse aufnehmen",
        "Rechnungsadesse im System eintragen",
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
    'Custom Pfad 24': [ # (Kunde bestellt im Laden) (Kunde bezahlt nicht direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde noch nicht bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Rechnungsadesse aufnehmen",
        "Rechnungsadesse im System eintragen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 25': [ # (Kunde bestellt im Laden) (Kunde bezahlt nicht direkt) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung nein) (Kunde noch nicht bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Rechnungsadesse aufnehmen",
        "Rechnungsadesse im System eintragen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 26': [  # (Kunde bestellt im Laden) (Kunde bezahlt nicht direkt) (Nicht alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung) (Kunde schon bezahlt)
        "Kunden-Daten aufnehmen",
        "Kunden-Daten in System übertragen",
        "Rechnungsadesse aufnehmen",
        "Rechnungsadesse im System eintragen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
    'Custom Pfad 27': [  # (Kunde bestellt über E-Mail) (Daten vollständig) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Vollständigkeit der Daten prüfen",
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
    'Custom Pfad 28': [ # (Kunde bestellt über E-Mail) (Daten vollständig) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde schon bezahlt)
        "Vollständigkeit der Daten prüfen",
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
    'Custom Pfad 29': [ # (Kunde bestellt über E-Mail) (Daten vollständig) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung) (Kunde noch nicht bezahlt)
        "Vollständigkeit der Daten prüfen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
     'Custom Pfad 30': [  # (Kunde bestellt über E-Mail) (Daten vollständig) (Alle Artikel vorhanden) (Warenwert über 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Vollständigkeit der Daten prüfen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Paket zur Warenausgabe bringen",
        "Paket an Kunde übergeben",
        "Bestellstatus im System ändern"
    ],
     'Custom Pfad 31': [  # (Kunde bestellt über E-Mail) (Daten vollständig) (Nicht alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Vollständigkeit der Daten prüfen",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
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
    'Custom Pfad 32': [  # (Kunde bestellt über E-Mail) (Daten unvollständig) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung) (Kunde schon bezahlt)
        "Vollständigkeit der Daten prüfen",
        "Fehlende Daten ermitteln",
        "Kunden bzgl. fehlender Daten anschreiben",
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
     'Custom Pfad 33': [ # (Kunde bestellt über E-Mail) (Daten unvollständig) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde noch nicht bezahlt, dopplete Nachfrage notwendig)
        "Vollständigkeit der Daten prüfen",
        "Fehlende Daten ermitteln",
        "Kunden bzgl. fehlender Daten anschreiben",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Bezahlaufforderung an Kunde schicken",
        "Bezahlaufforderung an Kunde schicken",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
    'Custom Pfad 34': [ # (Kunde bestellt über E-Mail) (Daten unvollständig) (Alle Artikel vorhanden) (Warenwert unter 50 EUR) (Ware entspricht nicht Bestellung; erneuter Durchlauf) (Selbstabholung nein) (Kunde schon bezahlt)
         "Vollständigkeit der Daten prüfen",
        "Fehlende Daten ermitteln",
        "Kunden bzgl. fehlender Daten anschreiben",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Fehler im System eintrgen",
        "Bestandsverwaltung informieren",
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
     'Custom Pfad 35': [ # (Kunde bestellt über E-Mail) (Daten unvollständig) (Nicht alle Artikel vorhanden) (Warenwert über EUR) (Ware entspricht Bestellung) (Selbstabholung nein) (Kunde schon bezahlt)
        "Vollständigkeit der Daten prüfen",
        "Fehlende Daten ermitteln",
        "Kunden bzgl. fehlender Daten anschreiben",
        "Bestellung im System eintragen",
        "Lagerbestand überprüfen",
        "Artikel bestellen",
        "Information an Kunde über verspätetet Lieferzeit verschicken",
        "Auftragsabwicklung im System starten",
        "Artikel zusammenstellen",
        "Versicherungs-Bescheinigung dazulegen",
        "Ware verpacken",
        "Gewicht prüfen",
        "Anzahl der Artikel überprüfen",
        "Verpackung prüfen",
        "Informationen an Transporteur übermitteln",
        "Paket an Transporteur übergeben",
        "Bestellstatus im System ändern"
    ],
}

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
    "Kunden-Daten aufnehmen": (1, 3),
    "Kunden-Daten in System übertragen": (2, 5),
    "Zahlvorgang abschließen": (3, 7),
    "Bestellung im System eintragen": (4, 9),
    "Lagerbestand überprüfen": (1, 3),
    "Auftragsabwicklung im System starten": (5, 10),
    "Artikel zusammenstellen": (2, 6),
    "Ware verpacken": (3, 8),
    "Gewicht prüfen": (1, 3),
    "Anzahl der Artikel überprüfen": (2, 5),
    "Verpackung prüfen": (3, 7),
    "Paket zur Warenausgabe bringen": (4, 9),
    "Paket an Kunde übergeben": (5, 10),
    "Bestellstatus im System ändern": (1, 3),
    "Zahlungsabwicklung durchführen": (6, 12),
    "Informationen an Transporteur übermitteln": (6, 12),
    "Paket an Transporteur übergeben": (6, 12),
    "Bezahlaufforderung an Kunde schicken": (6, 12),
    "Fehler im System eintrgen": (6, 12),
    "Bestandsverwaltung informieren": (6, 12),
    "Versicherungs-Bescheinigung dazulegen": (6, 12),
    "Artikel bestellen": (6, 12),
    "Information an Kunde über verspätetet Lieferzeit verschicken": (6, 12),
    "Kunden-Daten abfragen (automatische Übertragung ins System)": (6, 12),
    "Rechnungsadesse aufnehmen": (6, 12),
    "Rechnungsadesse im System eintragen": (6, 12),
    "Vollständigkeit der Daten prüfen": (6, 12),
    "Fehlende Daten ermitteln": (6, 12),
    "Kunden bzgl. fehlender Daten anschreiben": (6, 12),
    "Vollständigkeit der Daten prüfen": (6, 12)
}

# Anzahl der Ereignisse
num_events = 100

# Bevor die CSV-Datei erstellt wird, erhöhen wir die Revisionsnummer
revision_number += 1

# CSV-Datei öffnen und schreiben
with open(f"event_log_rev{revision_number}.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Fallnummer", "Aktivität", "Zeitstempel", "Ausführende Person", "Kosten (EUR)", "Kunde", "Transportiertes Gut", "Produktpreis (EUR)", "Abnahmeort", "Abgabeort"])

    for i in range(1, num_events + 1):
        case_number = str(i).zfill(3)
        selected_path = random.choice(list(paths.values()))
        # Für jeden Fall ein Produkt und einen Kunden auswählen
        product_tuple = random.choice(products)
        product_name, product_price = product_tuple
        # Ersetze Punkt durch Komma für die Ausgabe in der CSV-Datei
        product_price_for_csv = str(product_price).replace(".", ",")
        customer = random.choice(customers)

        timestamp = datetime.now()
        for activity in selected_path:  # Durchlaufe die Aktivitäten des ausgewählten Pfades
            person = random.choice(people)
            pickup_location = random.choice(locations)
            delivery_location = random.choice(locations)

            # Kostenrahmen für die aktuelle Aktivität
            min_cost, max_cost = activity_costs.get(activity, (1, 10))
            # Zufällige Kosten innerhalb des Kostenrahmens generieren
            cost = round(random.uniform(min_cost, max_cost), 2)
            cost_for_csv = str(cost).replace(".", ",")
            # Speichern / Schreiben in CSV-Datei
            writer.writerow([case_number, activity, timestamp.strftime("%Y-%m-%d %H:%M:%S"), person, cost_for_csv, customer, product_name, product_price_for_csv, pickup_location, delivery_location])

            # Zeitstempel für die nächste Aktivität inkrementieren
            timestamp += timedelta(minutes=random.randint(1, 60))

    # Speichern der aktualisierten Revisionsnummer in der JSON-Datei
    with open(revision_file_path, 'w') as file:
        json.dump({'revision_number': revision_number}, file)
        logging.debug(f"Revisionsnummer aktualisiert und gespeichert: {revision_number}")

# Fertigstellungslog :)
print(f"Die CSV-Datei 'event_log_rev{revision_number}.csv' wurde erfolgreich erstellt.")
logging.debug(f"CSV-Datei erfolgreich erstellt: event_log_rev{revision_number}.csv")