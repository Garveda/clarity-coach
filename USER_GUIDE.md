# Clarity Coach - Benutzerhandbuch

**Version:** 2.0 (Nach UI/UX-Optimierung)  
**Letzte Aktualisierung:** 2026-01-12

---

## Inhaltsverzeichnis

1. [Überblick](#1-überblick)
2. [Erste Schritte](#2-erste-schritte)
3. [Hauptfunktionen](#3-hauptfunktionen)
4. [Sokratische Hilfestellungen](#4-sokratische-hilfestellungen)
5. [Visuelle Hilfe](#5-visuelle-hilfe)
6. [Ansatz-Prüfung](#6-ansatz-prüfung)
7. [Sitzungsprotokollierung](#7-sitzungsprotokollierung)
8. [Selbstständigkeits-Score](#8-selbstständigkeits-score)
9. [Tipps für effektives Lernen](#9-tipps-für-effektives-lernen)
10. [Fehlerbehebung](#10-fehlerbehebung)

---

## 1. Überblick

**Clarity Coach** ist ein KI-gestütztes Lernwerkzeug, das auf der **sokratischen Methode** basiert. Anstatt direkte Lösungen zu zeigen, stellt das System gezielte Fragen und gibt progressive Hilfestellungen, die zum selbstständigen Denken anregen.

### Philosophie

> *"Ich kann niemandem etwas beibringen, ich kann ihn nur zum Denken anregen."* - Sokrates

Clarity Coach hilft dir dabei:
- **Selbstständig** Lösungswege zu entdecken
- **Kritisches Denken** zu entwickeln
- **Tiefes Verständnis** statt oberflächlichem Auswendiglernen

---

## 2. Erste Schritte

### 2.1 Anwendung starten

1. **Backend starten:**
   ```powershell
   cd backend
   .\venv\Scripts\activate
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Frontend starten:**
   ```powershell
   cd clarity-coach-main
   npm run dev
   ```

3. **Browser öffnen:** `http://localhost:5173`

### 2.2 Aufgabe hochladen

1. Klicke auf **"Datei auswählen"** oder ziehe eine Datei in den Upload-Bereich
2. Unterstützte Formate: **PDF, PNG, JPG, TXT**
3. Warte auf die Analyse (dauert ca. 10-30 Sekunden)

---

## 3. Hauptfunktionen

### Funktionsübersicht

| Funktion | Symbol | Beschreibung |
|----------|--------|--------------|
| Sokratische Fragen | 🤔 | Leitfragen zum Nachdenken |
| Hilfestellung | 💡 | 3-stufige progressive Hinweise |
| Visuelle Hilfe | 💡 | Grafiken, Animationen, Keyfacts |
| Ansatz prüfen | ✓ | Feedback ohne Lösung zu verraten |
| Protokollieren | 📊 | Sitzung speichern |

---

## 4. Sokratische Hilfestellungen

### 4.1 Das 3-Stufen-System

Klicke auf **"🤔 Hilfestellung"**, um progressive Hinweise zu erhalten:

#### Stufe 1: Sokratische Frage
- Offene Fragen, die zum Nachdenken anregen
- Beispiel: *"Welche Eigenschaft hat die Ableitung an Extremstellen?"*

#### Stufe 2: Anleitender Hinweis
- Konkretere Anleitung für den nächsten Schritt
- Beispiel: *"Berechne zuerst f'(x) und setze sie gleich null."*

#### Stufe 3: Spezifische Hilfe
- Sehr konkreter Hinweis (aber KEINE vollständige Lösung!)
- Beispiel: *"Bei f(x) = x³ - 3x² ist f'(x) = 3x² - 6x"*

### 4.2 Anzeige

```
╔════════════════════════════════════════════════╗
║  💡 Hilfestellung (Stufe 2/3)     [Anleitend]  ║
╠════════════════════════════════════════════════╣
║  Berechne die Ableitung f'(x) mit der          ║
║  Potenzregel und setze das Ergebnis            ║
║  gleich null.                                  ║
║                                                ║
║  ✓ Du schaffst das! 💪                         ║
║                                                ║
║  [Weitere Hilfe benötigt?]                     ║
╚════════════════════════════════════════════════╝
```

---

## 5. Visuelle Hilfe

### 5.1 Smart Visual Button

Klicke auf **"💡 Visuelle Hilfe"** - das System wählt automatisch die beste Darstellung:

| Typ | Wann verwendet | Beispiel |
|-----|----------------|----------|
| **Grafik** 📈 | Funktionen, Kurven | Plotly-Diagramm |
| **Animation** 🎬 | Schritt-für-Schritt | GSAP-Animation |
| **Keyfacts** 📋 | Formeln, Definitionen | Strukturierte Liste |

### 5.2 Intelligente Auswahl

Das System berücksichtigt:
- **Aufgabentyp** (z.B. Extremwert → Grafik)
- **Bisherige Hilfe** (Hints verwendet → Animation)
- **Lernfortschritt** (Wiederholte Fragen → Grafik)

---

## 6. Ansatz-Prüfung

### 6.1 Was ist die Ansatz-Prüfung?

Die Ansatz-Prüfung analysiert deinen Lösungsweg und gibt **konstruktives Feedback**, ohne die Lösung zu verraten.

### 6.2 Verwendung

1. Klicke auf **"✓ Meinen Ansatz prüfen"**
2. Beschreibe deinen Lösungsansatz im Textfeld
3. Klicke auf **"✓ Ansatz überprüfen"**

### 6.3 Beispieleingabe

```
Ich habe zuerst die Ableitung berechnet:
f'(x) = 3x² - 6x
Dann habe ich f'(x) = 0 gesetzt:
3x² - 6x = 0
3x(x - 2) = 0
Also x₁ = 0 und x₂ = 2
```

### 6.4 Feedback-Anzeige

```
╔════════════════════════════════════════════════╗
║  ✓ Auf dem richtigen Weg!        ★★★★☆        ║
╠════════════════════════════════════════════════╣
║  Dein Ansatz ist grundsätzlich richtig.        ║
║                                                ║
║  ✓ Was gut war:                                ║
║    • Ableitung korrekt berechnet               ║
║    • Nullsetzen richtig angewendet             ║
║                                                ║
║  → Verbesserungsvorschläge:                    ║
║    • Überprüfe die Lösungen mit f''(x)         ║
║                                                ║
║  📍 Nächster Schritt:                          ║
║    Bestimme die Art der Extremstellen          ║
║                                                ║
║  ✓ Weiter so! Du bist fast am Ziel!            ║
╚════════════════════════════════════════════════╝
```

### 6.5 Bewertungsskala

| Sterne | Bedeutung |
|--------|-----------|
| ★★★★★ | Perfekter Ansatz |
| ★★★★☆ | Fast richtig |
| ★★★☆☆ | Teilweise richtig |
| ★★☆☆☆ | Auf falschem Weg |
| ★☆☆☆☆ | Komplett falsch |

---

## 7. Sitzungsprotokollierung

### 7.1 Sitzung protokollieren

1. Klicke auf **"📊 Sitzung protokollieren"**
2. Fülle das Formular aus:
   - Name, Klasse, Schule
   - Fach, Thema, Schwierigkeitsgrad
   - Optionale Notizen

### 7.2 Automatisch erfasste Daten

- **Nutzungsstatistik** (Visualisierungen, Animationen, etc.)
- **Hilfestellungen verwendet**
- **Ansatzprüfungen durchgeführt**
- **Selbstständigkeits-Score**
- **Sitzungsdauer**

### 7.3 Excel-Export

Daten werden gespeichert in:
```
Clarity_Coach_Session_Log.xlsx
```

---

## 8. Selbstständigkeits-Score

### 8.1 Was ist der Score?

Der **Selbstständigkeits-Score** zeigt, wie eigenständig du Aufgaben gelöst hast.

### 8.2 Berechnung

| Hilfe verwendet | Score | Bewertung |
|-----------------|-------|-----------|
| 0 | ★★★★★ (5) | Eigenständig |
| 1-2 | ★★★★☆ (4) | Minimal unterstützt |
| 3-5 | ★★★☆☆ (3) | Moderat unterstützt |
| 6-8 | ★★☆☆☆ (2) | Stark unterstützt |
| 9+ | ★☆☆☆☆ (1) | Intensive Betreuung |

### 8.3 Interpretation

- **Score 5**: Du hast die Aufgabe ohne Hilfe gelöst - ausgezeichnet!
- **Score 4**: Minimale Unterstützung - sehr gut!
- **Score 3**: Du hast dich durch die Aufgabe gearbeitet - gut!
- **Score 2**: Du brauchst noch Übung bei diesem Thema
- **Score 1**: Dieses Thema sollte intensiver wiederholt werden

---

## 9. Tipps für effektives Lernen

### Do's ✓

- **Lies die sokratischen Fragen sorgfältig** - sie enthalten wichtige Hinweise
- **Versuche selbst zu denken**, bevor du weitere Hilfe anforderst
- **Nutze die Ansatz-Prüfung**, um dein Verständnis zu testen
- **Arbeite schrittweise** - nicht alles auf einmal

### Don'ts ✗

- ~~Sofort alle Hilfestellungen anfordern~~
- ~~Aufgaben überspringen, die schwer erscheinen~~
- ~~Den Ansatz-Checker ohne echten Versuch nutzen~~

### Lernstrategie

```
1. Lies die Aufgabe sorgfältig
       ↓
2. Überlege selbst (5 Minuten)
       ↓
3. Nutze sokratische Fragen
       ↓
4. Versuche erneut
       ↓
5. Bei Bedarf: Visuelle Hilfe
       ↓
6. Ansatz prüfen lassen
       ↓
7. Progressive Hilfestellung (nur wenn nötig)
```

---

## 10. Fehlerbehebung

### Problem: Upload hängt

**Lösung:**
1. Prüfe, ob das Backend läuft
2. Prüfe die `.env`-Datei (OPENAI_API_KEY)
3. Starte beide Server neu

### Problem: Keine Visualisierung möglich

**Lösung:**
- Bei abstrakten Aufgaben ohne konkrete Funktion kann keine Grafik erstellt werden
- Nutze stattdessen die Animation oder Keyfacts

### Problem: Session-Speicherung schlägt fehl

**Lösung:**
1. Prüfe, ob die Excel-Datei existiert
2. Schließe die Excel-Datei, falls sie geöffnet ist
3. Prüfe Schreibrechte im Ordner

### Kontakt bei Problemen

Bei weiteren Fragen oder Problemen wende dich an den Administrator.

---

**© 2026 Clarity Coach - Sokratisches Lernen mit KI**
