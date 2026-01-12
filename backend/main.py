# Datei: main.py

from fastapi import FastAPI, UploadFile, HTTPException, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import base64
import os
import json
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import re
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Border, Side, Alignment
from pydantic import BaseModel

# 🔹 Umgebung laden (.env mit OPENAI_API_KEY)
load_dotenv()

app = FastAPI()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60.0,  # 60 second timeout to prevent hanging forever
    max_retries=2
)

# 🔹 CORS freischalten (Frontend darf auf Backend zugreifen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion: besser gezielt Domain angeben
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Favicon
# ------------------------------
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# ------------------------------
# Test-Endpoint
# ------------------------------
@app.get("/")
def read_root():
    return {"message": "Clarity Coach API läuft ✅"}

# ------------------------------
# Health Check
# ------------------------------
@app.get("/health")
def health_check():
    """Check if backend and OpenAI API are working"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return {"status": "error", "message": "OpenAI API key not found"}
    
    if api_key == "your-api-key-here":
        return {"status": "error", "message": "OpenAI API key not configured (still using placeholder)"}
    
    # Test OpenAI connection
    try:
        test_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return {
            "status": "ok", 
            "message": "Backend and OpenAI API working",
            "api_key_valid": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"OpenAI API error: {str(e)}",
            "api_key_valid": False
        }


# ------------------------------
# Hilfsfunktion: Clarity-Coach-Prompt ausführen
# ------------------------------
def run_clarity_coach(full_text: str):
    """
    Nimmt reinen Aufgabentext und gibt die strukturierte Aufgabenliste zurück:
    [
      {
        "number": "1",
        "topic": "...",
        "difficulty": "leicht/mittel/anspruchsvoll",
        "task": "volle Aufgabenangabe",
        "subtasks": [
          {
            "label": "a",
            "task": "Text der Teilaufgabe a",
            "questions": ["...", "..."]
          }
        ]
      },
      ...
    ]
    """

    clarity_prompt = f"""
Du bist der KI-Entwicklungsassistent für das Projekt Clarity Coach.

Deine Aufgabe:
- Analysiere den folgenden Aufgabentext (mehrere Aufgaben mit Teilaufgaben möglich).
- Erkenne Aufgaben (1., 2., 3., …) und Teilaufgaben (a), b), c), …).
- Erstelle für jede Aufgabe und jede Teilaufgabe:
  • "number": Aufgabennummer als String (z.B. "1")
  • "topic": kurzes Thema (z.B. "Kubische Gleichungen", "Potenzfunktionen")
  • "difficulty": "leicht", "mittel" oder "anspruchsvoll"
  • "task": vollständiger Text der übergeordneten Aufgabe (ohne die einzelnen Teilaufgaben)
  • "subtasks": Liste von Objekten mit:
      - "label": Buchstabe der Teilaufgabe, z.B. "a"
      - "task": Text der Teilaufgabe
      - "questions": 3–5 sokratische Fragen (Strings)

WICHTIG: Die Fragen müssen **sehr aufgabenspezifisch** sein und sich konkret auf Terme, Zahlen und Begriffe der jeweiligen Teilaufgabe beziehen.

Für jede Teilaufgabe erstelle Fragen aus diesen Kategorien (in beliebiger Reihenfolge):

1. STRUKTUR-FRAGE
   - Frage nach der Form der Gleichung/Funktion und ihren Bestandteilen.
   - Nenne mindestens einen konkreten Term oder eine Zahl aus der Aufgabe.
   - Beispiel: „Welche Zahl wird in der Gleichung x^3 - 27 = 0 als Kubikzahl verwendet?“

2. UMFORMUNGS-FRAGE
   - Frage nach einem konkreten nächsten Rechenschritt.
   - Beispiel: „Wie kannst du die -27 in der Gleichung x^3 - 27 = 0 auf die andere Seite bringen?“

3. OPERATIONS-FRAGE
   - Frage nach der passenden Rechenoperation/Funktion (z.B. Wurzel, Logarithmus, Ableitung).
   - Beispiel: „Welche Umkehrfunktion brauchst du, um aus x^3 wieder x zu erhalten?“

4. KONTROLL- ODER INTERPRETATIONS-FRAGE
   - Frage nach der Bedeutung des Ergebnisses, der Anzahl der Lösungen, Monotonie, etc.
   - Beispiel: „Was sagt dir die Tatsache, dass f'(x) = 3x^2 ≥ 0 für alle x über die Anzahl der Nullstellen von f(x) = x^3 - 27?“

Regeln für die Formulierung:
- Jede Frage muss mindestens EIN konkretes Element aus der Teilaufgabe enthalten
  (z.B. eine Zahl wie 27 oder 1/27, einen Term wie x^3, f(x), oder einen Fachbegriff wie „Nullstelle“).
- Vermeide generische Fragen wie:
  • „Was sagt dir die Gleichung über x?“
  • „Wie kannst du die Gleichung lösen?“
  • „Welche Schritte musst du machen?“
- Formuliere die Fragen so, dass der Schüler *konkrete* nächste Schritte beschreiben muss
  (z.B. „Welche Zahl…“, „Welchen Term…“, „Welche Umformung…“, „Welche Eigenschaft…“).

Ausgabeformat:
- Gib ein JSON-OBJEKT mit GENAU einem Feld "tasks" zurück.
- "tasks" ist eine LISTE von Aufgabenobjekten wie im folgenden Schema:

{{
  "tasks": [
    {{
      "number": "1",
      "topic": "Kubische Gleichungen",
      "difficulty": "mittel",
      "task": "Zeige, dass die Gleichung nur eine reelle Lösung besitzt.",
      "subtasks": [
        {{
          "label": "a",
          "task": "x^3 - 27 = 0",
          "questions": [
            "Frage 1 ...",
            "Frage 2 ...",
            "Frage 3 ..."
          ]
        }}
      ]
    }}
  ]
}}

Keine Erklärtexte außerhalb dieses JSON-Objekts, keine Markdown-Codeblöcke.

Hier ist der vollständige Aufgabentext:

{full_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein geduldiger, sokratischer Mathematiklehrer. "
                    "Du erzeugst sehr aufgabenspezifische Fragen und gibst "
                    "die Antwort ausschließlich als gültiges JSON-Objekt mit dem Feld 'tasks' zurück."
                ),
            },
            {"role": "user", "content": clarity_prompt},
        ],
    )

    raw = response.choices[0].message.content
    
    # Safe printing for Windows console (handle Unicode characters)
    try:
        print("\n--- GPT-Raw-Response (JSON-Modus) ---\n", raw, "\n------------------------\n")
    except UnicodeEncodeError:
        print("\n--- GPT-Raw-Response (JSON-Modus) ---\n[Response contains Unicode characters - check logs]\n------------------------\n")
    
    try:
        obj = json.loads(raw)
        tasks = obj.get("tasks", None)
        if isinstance(tasks, list):
            return tasks
        if isinstance(obj, list):
            return obj
        return {
            "error": "Antwort hatte nicht das erwartete Format (Feld 'tasks' fehlt oder ist keine Liste).",
            "raw_output": raw,
        }
    except Exception as e:
        print(f"[ERROR] JSON-Fehler im JSON-Modus: {e}")
        return {
            "error": "Konnte JSON nicht korrekt verarbeiten",
            "raw_output": raw,
        }


# ------------------------------
# Textbasierte Eingabe (z.B. für Tests)
# ------------------------------
@app.post("/clarity")
def clarity(input: dict = Body(...)):
    user_input = input.get("task", "")
    if not user_input.strip():
        return {"error": "Kein Aufgabentext übergeben."}

    result = run_clarity_coach(user_input)
    return result


# ------------------------------
# Lösung für eine Teilaufgabe generieren
# ------------------------------
@app.post("/solve")
async def solve(payload: dict = Body(...)):
    task_number = payload.get("taskNumber")
    task_text = payload.get("taskText", "")
    topic = payload.get("topic", "")
    sub_label = payload.get("subLabel")
    subtask_text = payload.get("subtaskText", "")

    if not subtask_text or not str(subtask_text).strip():
        raise HTTPException(status_code=400, detail="Keine Teilaufgabe übergeben.")

    solve_prompt = f"""
Du bist ein präziser mathematischer Solver.

Du sollst die folgende Teilaufgabe **vollständig lösen** und knapp begründen.
Die Antwort wird im Frontend zeilenweise verarbeitet und mit KaTeX gerendert.

FORMATREGELN (sehr wichtig):

1. Antworte NUR mit einfachem Text und LaTeX, keine Markdown-Codeblöcke, keine ```.

2. Jede logische Zeile der Lösung steht in einer eigenen Zeile.
   Es gibt KEINE Aufzählungszeichen, KEINE Nummerierung und KEINE Einleitungen wie „Natürlich“ o.Ä.

3. Verwende GENAU ZWEI Label-Zeilen:
   - eine Zeile nur mit:  Lösung:
   - eine spätere Zeile nur mit: Begründung:

4. Alle anderen Zeilen sind entweder
   a) REINE Gleichungs-/Mathe-Zeilen:
      - nur Symbole, Zahlen und LaTeX-Befehle (z.B. x^3 - 27 = 0, x^3 = 27, x = 3,
        p(\\sqrt{{2/3}}) \\approx 4.39, \\Delta < 0, f'(x) = 3x^2, ...)
      - KEINE deutschen Wörter in diesen Zeilen
   b) oder kurze deutsche Textzeilen zur Erklärung,
      z.B. „Es gibt genau eine reelle Lösung.“ oder
      „Das Polynom ist streng monoton wachsend.“

5. Vermische KEINE deutschen Wörter mit LaTeX in derselben Zeile.
   Wenn du etwas erklären willst, schreibe die Erklärung in einer eigenen Textzeile
   ohne LaTeX-Befehle wie \\sqrt, \\frac, \\Rightarrow usw.

6. Verwende KEINE Dollarzeichen ($) und KEINE Umklammerung durch \\[...\\] oder \\(...\\).
   Schreibe die LaTeX-Ausdrücke direkt in die Zeile, z.B.:
   x^3 - 27 = 0
   x^3 = 27
   x = 3

7. Insgesamt sollen es maximal 8–10 Zeilen sein.

Beispiel für das gewünschte Format (nur als Orientierung):

Lösung:
x^3 - 27 = 0
x^3 = 27
x = 3

Begründung:
f(x) = x^3 - 27 ist streng monoton wachsend,
daher gibt es genau eine reelle Lösung.

Jetzt die konkrete Aufgabe:

Thema (falls hilfreich): {topic}

Übergeordnete Aufgabe {task_number}:
{task_text}

Teilaufgabe {sub_label}):
{subtask_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein hilfreicher, aber äußerst knapper Mathematiklehrer. "
                    "Du hältst dich strikt an das geforderte Zeilenformat, "
                    "verwendest keine Markdown-Codeblöcke und keine LaTeX-Delimiters wie $ oder \\[."
                ),
            },
            {"role": "user", "content": solve_prompt},
        ],
    )

    solution_text = response.choices[0].message.content

    # Wir verpacken einfach den Text in ein JSON-Feld
    return {"solution": solution_text}


# ------------------------------
# Datei-Upload (Bild oder PDF)
# ------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        print(f"[UPLOAD] Started: {file.filename}")
        
        filename = file.filename.lower()
        contents = await file.read()
        extracted_texts = []

        print(f"[UPLOAD] File size: {len(contents)} bytes")
        print(f"[UPLOAD] File type: {filename}")

        # Text, PDF oder Bild unterscheiden
        if filename.endswith(".txt"):
            # Textdatei direkt lesen
            print("[UPLOAD] Processing as text file...")
            text_content = contents.decode("utf-8")
            extracted_texts.append(text_content)
            
        elif filename.endswith(".pdf"):
            print("[UPLOAD] Processing as PDF...")
            pdf = fitz.open(stream=BytesIO(contents), filetype="pdf")
            for page_num in range(len(pdf)):
                print(f"[UPLOAD] Processing page {page_num + 1}/{len(pdf)}...")
                page = pdf.load_page(page_num)
                pix = page.get_pixmap(dpi=150)
                img_b64 = base64.b64encode(pix.tobytes("jpeg")).decode("utf-8")

                vision_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        f"Lies den Inhalt dieser Seite ({page_num + 1}) "
                                        "mit allen Mathematikaufgaben und gib NUR den erkannten Text wieder:"
                                    ),
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_b64}"
                                    },
                                },
                            ],
                        }
                    ],
                )
                extracted_texts.append(vision_response.choices[0].message.content)
                
        else:
            # Einzelbild direkt verarbeiten
            print("[UPLOAD] Processing as image...")
            b64 = base64.b64encode(contents).decode("utf-8")
            vision_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Lies den Inhalt dieser Aufgabe und gib NUR den Text wieder:",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                            },
                        ],
                    }
                ],
            )
            extracted_texts.append(vision_response.choices[0].message.content)

        # Gesamttext zusammenfuehren
        print("[UPLOAD] Merging extracted text...")
        full_text = "\n\n".join(extracted_texts)
        print(f"[UPLOAD] Extracted text length: {len(full_text)} characters")

        # Clarity-Coach-Logik auf den erkannten Text anwenden
        print("[UPLOAD] Running Clarity Coach analysis...")
        result = run_clarity_coach(full_text)
        
        print("[UPLOAD] Analysis complete!")
        return result
    
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Upload failed: {error_msg}")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Upload/Analysis failed: {error_msg[:200]}"
        )


# ------------------------------
# Visualization für eine Teilaufgabe generieren
# ------------------------------
@app.post("/visualize")
async def visualize(payload: dict = Body(...)):
    task_number = payload.get("taskNumber")
    task_text = payload.get("taskText", "")
    topic = payload.get("topic", "")
    sub_label = payload.get("subLabel")
    subtask_text = payload.get("subtaskText", "")

    if not subtask_text or not str(subtask_text).strip():
        raise HTTPException(status_code=400, detail="Keine Teilaufgabe übergeben.")

    visualize_prompt = f"""
Du bist ein Mathematik-Experte, der auf die Erstellung klarer, strukturierter Visualisierungen mathematischer Konzepte spezialisiert ist.

Erstelle eine hilfreiche Visualisierung für die folgende Teilaufgabe, die SCHLÜSSELFAKTEN und konzeptionelles Verständnis hervorhebt.

**Aufgabe {task_number}: {topic}**
Hauptaufgabe: {task_text}

**Teilaufgabe {sub_label}:**
{subtask_text}

Erstelle eine strukturierte Visualisierung, die Folgendes enthält:

1. **Kernkonzepte**: Liste der beteiligten mathematischen Konzepte
2. **Gegebene Informationen**: Welche Daten/Informationen sind gegeben
3. **Gesuchtes**: Was soll gelöst oder bewiesen werden
4. **Relevante Formeln**: Wichtige Formeln oder Sätze, die gelten
5. **Wichtige Fakten**: Kritische Fakten oder Eigenschaften zum Merken
6. **Lösungsansatz-Hinweise**: Strategie auf hohem Niveau (ohne die Lösung zu verraten)

FORMATIERE DEINE ANTWORT WIE FOLGT:
- Verwende ** ** für Abschnittsüberschriften (z.B., **Kernkonzepte**)
- Verwende Aufzählungspunkte mit "- " für Listenelemente
- Verwende Schlüssel-Wert-Paare mit ":" für strukturierte Daten
- Füge mathematische Notation mit LaTeX ein, wo angebracht ($...$ für inline, $$...$$ für display)
- Halte Erklärungen prägnant und visuell
- Fokus auf VERSTÄNDNIS, nicht auf die Lösung

Beispielformat:
**Kernkonzepte**
- Polynomfunktionen
- Nullstellen

**Gegebene Informationen**
- Funktion: $f(x) = x^3 - 27$
- Definitionsbereich: Reelle Zahlen

**Gesuchtes**
- Alle reellen Lösungen

Gib NICHT die vollständige Lösung. Konzentriere dich auf die visuelle Organisation der Fakten und Konzepte.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a mathematics visualization assistant."},
                {"role": "user", "content": visualize_prompt}
            ],
            temperature=0.7
        )

        visualization_text = response.choices[0].message.content

        # Safe printing for Windows console
        try:
            print("\n--- Visualization Generated ---\n", visualization_text[:200], "...\n")
        except UnicodeEncodeError:
            print("\n--- Visualization Generated ---\n[Contains Unicode characters]\n")

        return {"visualization": visualization_text}

    except Exception as e:
        print(f"[ERROR] Error generating visualization: {e}")
        raise HTTPException(status_code=500, detail=f"Visualization generation failed: {str(e)}")


# ------------------------------
# Manim Animation für eine Teilaufgabe generieren
# ------------------------------
@app.post("/animate")
async def animate(payload: dict = Body(...)):
    task_number = payload.get("taskNumber")
    task_text = payload.get("taskText", "")
    topic = payload.get("topic", "")
    sub_label = payload.get("subLabel")
    subtask_text = payload.get("subtaskText", "")

    if not subtask_text or not str(subtask_text).strip():
        raise HTTPException(status_code=400, detail="Keine Teilaufgabe übergeben.")

    animate_prompt = f"""
Du bist ein Experte für mathematische Animationen. Erstelle eine Schritt-für-Schritt Animation für folgende Aufgabe.

**Aufgabe {task_number}: {topic}**
Hauptaufgabe: {task_text}

**Teilaufgabe {sub_label}:**
{subtask_text}

Erstelle eine JSON-Struktur für eine Browser-Animation (mit Canvas/SVG + GSAP + KaTeX).

ANFORDERUNGEN:
1. 3-5 klare Animationsschritte
2. Jeder Schritt hat: Text-Erklärung + mathematische Formel (LaTeX)
3. Beschreibe visuelle Effekte (fadeIn, scale, move, highlight, etc.)
4. Halte es einfach und verständlich

ANTWORTFORMAT (reines JSON, keine Erklärungen):
{{
  "title": "Kurzer Titel der Aufgabe",
  "steps": [
    {{
      "id": 1,
      "description": "Beschreibung was passiert",
      "latex": "x^2 + 3x - 4 = 0",
      "animation": "fadeIn",
      "duration": 1.0,
      "position": "center"
    }},
    {{
      "id": 2,
      "description": "Nächster Schritt",
      "latex": "x^2 + 3x = 4",
      "animation": "highlight",
      "duration": 0.8,
      "position": "center",
      "highlight": "+3x"
    }},
    {{
      "id": 3,
      "description": "Transformation",
      "latex": "(x + 4)(x - 1) = 0",
      "animation": "transform",
      "duration": 1.2,
      "position": "center"
    }}
  ]
}}

VERFÜGBARE ANIMATIONEN:
- fadeIn: Element erscheint
- fadeOut: Element verschwindet
- scale: Element wird größer/kleiner
- move: Element bewegt sich
- highlight: Teil wird hervorgehoben
- transform: Sanfte Umwandlung
- bounce: Springender Effekt

POSITIONEN: "center", "top", "bottom", "left", "right"

Gib NUR das JSON zurück, keine Markdown-Codeblöcke, keine Erklärungen.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein Experte für mathematische Visualisierungen und Animationen."},
                {"role": "user", "content": animate_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        animation_json_str = response.choices[0].message.content
        
        # Safe printing
        try:
            print("\n--- Animation JSON Generated ---\n", animation_json_str[:300], "...\n")
        except UnicodeEncodeError:
            print("\n--- Animation JSON Generated ---\n[Contains Unicode characters]\n")

        # Parse JSON
        animation_data = json.loads(animation_json_str)
        
        # Return the animation data for browser rendering
        return {
            "animationData": animation_data,
            "success": True
        }

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON Parse Error: {e}")
        raise HTTPException(status_code=500, detail=f"Animation JSON parsing failed: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Error generating animation: {e}")
        raise HTTPException(status_code=500, detail=f"Animation generation failed: {str(e)}")


# ------------------------------
# Plotly Graph für eine Teilaufgabe generieren
# ------------------------------
@app.post("/plot")
async def plot_task(payload: dict = Body(...)):
    task_number = payload.get("taskNumber")
    task_text = payload.get("taskText", "")
    topic = payload.get("topic", "")
    sub_label = payload.get("subLabel")
    subtask_text = payload.get("subtaskText", "")

    if not subtask_text or not str(subtask_text).strip():
        raise HTTPException(status_code=400, detail="Keine Teilaufgabe übergeben.")

    plot_prompt = f"""
Du bist ein Experte für mathematische Visualisierungen. Analysiere die folgende Aufgabe und bestimme, ob eine grafische Darstellung sinnvoll ist.

**Aufgabe {task_number}: {topic}**
Hauptaufgabe: {task_text}

**Teilaufgabe {sub_label}:**
{subtask_text}

ENTSCHEIDE:
1. Ist eine grafische Darstellung für diese Aufgabe möglich und sinnvoll?
2. Hat die Aufgabe eine KONKRETE Funktion mit SPEZIFISCHEN Werten? (Nicht abstrakt mit a, b, c)
3. Wenn JA: Welche Art von Graph? (Funktionsplot, Polynom, Parabel, Gerade, Kreis, etc.)
4. Extrahiere die relevanten Parameter

WICHTIG:
- Wenn die Aufgabe nur abstrakte Bedingungen wie "f'(x₁) = 0" oder "f''(x₁) ≠ 0" enthält OHNE konkrete Funktion → plottable: false
- Wenn die Aufgabe Parameter wie a, b, c enthält OHNE konkrete Werte → plottable: false  
- NUR wenn eine konkrete Funktion wie "x³ - 27" oder "2x + 3" gegeben ist → plottable: true

ANTWORTFORMAT (reines JSON):
{{
  "plottable": true/false,
  "reason": "Kurze Begründung warum ja/nein",
  "graphType": "function" / "polynomial" / "line" / "circle" / "points" / "none",
  "function": "mathematischer Ausdruck in Python-Syntax, z.B. x**3 - 27",
  "domain": {{"xMin": -10, "xMax": 10, "yMin": -50, "yMax": 50}},
  "title": "Titel für die Grafik",
  "xLabel": "x",
  "yLabel": "y oder f(x)",
  "points": [  // Nur wenn graphType = "points"
    {{"x": 1, "y": 2, "label": "Punkt A"}},
    {{"x": 3, "y": 4, "label": "Punkt B"}}
  ],
  "specialPoints": [  // Wichtige Punkte wie Nullstellen, Extrema
    {{"x": 3, "y": 0, "label": "Nullstelle", "color": "red"}}
  ]
}}

BEISPIELE:

Aufgabe: "Löse x^3 - 27 = 0"
{{
  "plottable": true,
  "reason": "Funktionsplot zeigt die Nullstelle visuell",
  "graphType": "polynomial",
  "function": "x**3 - 27",
  "domain": {{"xMin": -5, "xMax": 5, "yMin": -50, "yMax": 50}},
  "title": "f(x) = x³ - 27",
  "xLabel": "x",
  "yLabel": "f(x)",
  "specialPoints": [{{"x": 3, "y": 0, "label": "Nullstelle x=3", "color": "red"}}]
}}

Aufgabe: "Berechne 5 + 3"
{{
  "plottable": false,
  "reason": "Einfache Arithmetik ohne grafische Komponente",
  "graphType": "none"
}}

Aufgabe: "Zeige, dass f'(x₁) = 0 und f''(x₁) ≠ 0 gilt"
{{
  "plottable": false,
  "reason": "Abstrakte Bedingung ohne konkrete Funktion - keine spezifischen Werte für f(x)",
  "graphType": "none"
}}

Aufgabe: "Zeichne die Gerade durch A(1,2) und B(3,6)"
{{
  "plottable": true,
  "reason": "Gerade mit gegebenen Punkten",
  "graphType": "line",
  "function": "2*x",
  "domain": {{"xMin": 0, "xMax": 5, "yMin": 0, "yMax": 10}},
  "title": "Gerade durch A und B",
  "xLabel": "x",
  "yLabel": "y",
  "points": [
    {{"x": 1, "y": 2, "label": "A"}},
    {{"x": 3, "y": 6, "label": "B"}}
  ]
}}

Gib NUR das JSON zurück, keine Erklärungen, keine Markdown-Codeblöcke.
"""

    try:
        print("[PLOT] Analyzing task for plottability...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein Experte für mathematische Visualisierungen. Antworte nur mit gültigem JSON."},
                {"role": "user", "content": plot_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        plot_json_str = response.choices[0].message.content
        print(f"[PLOT] GPT Response: {plot_json_str[:200]}...")
        
        # Parse JSON
        plot_data = json.loads(plot_json_str)
        
        # Check if plottable
        if not plot_data.get("plottable", False):
            return {
                "plottable": False,
                "message": plot_data.get("reason", "Keine grafische Darstellung möglich für diese Aufgabe")
            }
        
        # Generate plot based on graphType
        graph_type = plot_data.get("graphType", "function")
        
        print(f"[PLOT] Generating {graph_type} plot...")
        
        if graph_type in ["function", "polynomial", "line"]:
            # Function plot
            func_str = plot_data.get("function", "x")
            domain = plot_data.get("domain", {"xMin": -10, "xMax": 10, "yMin": -50, "yMax": 50})
            
            # Generate x values
            x = np.linspace(domain.get("xMin", -10), domain.get("xMax", 10), 500)
            
            # Evaluate function safely
            try:
                # Replace common math notation
                func_str_safe = func_str.replace("^", "**").replace("π", "np.pi").replace("e", "np.e")
                
                # Check if function has undefined variables (like a, b, c for generic polynomials)
                # Try to evaluate with a test value first
                test_x = np.array([1.0])
                test_eval = eval(func_str_safe, {"x": test_x, "np": np, "__builtins__": {}})
                
                # If successful, evaluate for full domain
                y = eval(func_str_safe, {"x": x, "np": np, "__builtins__": {}})
            except (NameError, SyntaxError) as e:
                print(f"[ERROR] Function contains undefined variables or syntax error: {e}")
                return {
                    "plottable": False,
                    "message": "Diese Aufgabe ist zu abstrakt für eine konkrete Grafik. Sie enthält allgemeine Parameter ohne spezifische Werte."
                }
            except Exception as e:
                print(f"[ERROR] Function evaluation failed: {e}")
                return {
                    "plottable": False,
                    "message": f"Konnte Funktion nicht auswerten: {str(e)}"
                }
            
            # Create plot
            fig = go.Figure()
            
            # Add main function
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name=plot_data.get("title", "f(x)"),
                line=dict(color='#2c5f8d', width=3)
            ))
            
            # Add special points (nullstellen, extrema, etc.)
            special_points = plot_data.get("specialPoints", [])
            for point in special_points:
                fig.add_trace(go.Scatter(
                    x=[point.get("x")],
                    y=[point.get("y")],
                    mode='markers+text',
                    name=point.get("label", "Punkt"),
                    marker=dict(size=12, color=point.get("color", "red")),
                    text=[point.get("label", "")],
                    textposition="top center"
                ))
            
            # Add given points
            points = plot_data.get("points", [])
            for point in points:
                fig.add_trace(go.Scatter(
                    x=[point.get("x")],
                    y=[point.get("y")],
                    mode='markers+text',
                    name=point.get("label", "Punkt"),
                    marker=dict(size=10, color='green'),
                    text=[point.get("label", "")],
                    textposition="top center"
                ))
            
            # Update layout
            fig.update_layout(
                title=plot_data.get("title", "Grafik"),
                xaxis_title=plot_data.get("xLabel", "x"),
                yaxis_title=plot_data.get("yLabel", "y"),
                hovermode='x unified',
                template='plotly_white',
                height=500,
                showlegend=True,
                xaxis=dict(
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='gray',
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='gray',
                    gridcolor='lightgray',
                    range=[domain.get("yMin", -50), domain.get("yMax", 50)]
                )
            )
            
            # Convert to JSON data for frontend rendering
            plot_json = fig.to_json()
            
            print("[PLOT] Plot generated successfully!")
            
            return {
                "plotData": plot_json,
                "plottable": True,
                "graphType": graph_type
            }
        
        elif graph_type == "points":
            # Scatter plot with points only
            points = plot_data.get("points", [])
            
            if not points:
                return {
                    "plottable": False,
                    "message": "Keine Punkte zum Plotten vorhanden"
                }
            
            fig = go.Figure()
            
            for point in points:
                fig.add_trace(go.Scatter(
                    x=[point.get("x")],
                    y=[point.get("y")],
                    mode='markers+text',
                    name=point.get("label", "Punkt"),
                    marker=dict(size=12, color='#2c5f8d'),
                    text=[point.get("label", "")],
                    textposition="top center"
                ))
            
            domain = plot_data.get("domain", {"xMin": -10, "xMax": 10, "yMin": -10, "yMax": 10})
            
            fig.update_layout(
                title=plot_data.get("title", "Punkte"),
                xaxis_title=plot_data.get("xLabel", "x"),
                yaxis_title=plot_data.get("yLabel", "y"),
                template='plotly_white',
                height=500,
                showlegend=True,
                xaxis=dict(
                    range=[domain.get("xMin", -10), domain.get("xMax", 10)],
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='gray'
                ),
                yaxis=dict(
                    range=[domain.get("yMin", -10), domain.get("yMax", 10)],
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='gray'
                )
            )
            
            plot_json = fig.to_json()
            
            return {
                "plotData": plot_json,
                "plottable": True,
                "graphType": graph_type
            }
        
        else:
            return {
                "plottable": False,
                "message": f"Graph-Typ '{graph_type}' noch nicht implementiert"
            }

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON Parse Error: {e}")
        raise HTTPException(status_code=500, detail=f"Plot JSON parsing failed: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Error generating plot: {e}")
        raise HTTPException(status_code=500, detail=f"Plot generation failed: {str(e)}")


# ------------------------------
# Session Logging - Excel Integration
# ------------------------------
class SessionLogEntry(BaseModel):
    benutzer_name: str
    klasse: str
    schule: str
    fach: str
    thema: str
    aufgabentyp: str
    schwierigkeitsgrad: str
    datei_name: str
    datei_typ: str
    anzahl_aufgaben: int
    anzahl_teilaufgaben: int
    visualisierungen_genutzt: int
    animationen_genutzt: int
    grafiken_genutzt: int
    loesungen_angezeigt: int
    feedback: str
    sitzungsdauer_minuten: float
    notizen: str


EXCEL_PATH = r"C:\Users\admin\Desktop\Sonstiges\HMS_PROJEKT\clarity-coach\Clarity_Coach_Session_Log.xlsx"


@app.post("/log-session")
async def log_session(entry: SessionLogEntry):
    """
    Log a Clarity Coach session to Excel file
    """
    try:
        print(f"[LOG] Starting session log...")
        
        # Check if Excel file exists
        if not os.path.exists(EXCEL_PATH):
            print(f"[ERROR] Excel file not found at: {EXCEL_PATH}")
            raise HTTPException(
                status_code=500, 
                detail=f"Excel file not found. Please create it first using create_excel_template.py"
            )
        
        # Load workbook
        wb = load_workbook(EXCEL_PATH)
        
        # Get or create Session_Log sheet
        if "Session_Log" not in wb.sheetnames:
            print(f"[ERROR] Session_Log sheet not found")
            raise HTTPException(
                status_code=500,
                detail="Session_Log sheet not found in Excel file"
            )
        
        ws = wb["Session_Log"]
        
        # Find next row
        next_row = ws.max_row + 1
        
        # Generate Session ID (format: YYYYMMDD-###)
        today = datetime.now().strftime("%Y%m%d")
        session_count = next_row - 1  # -1 for header
        session_id = f"{today}-{session_count:03d}"
        
        # Get current date and time
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Prepare data row
        data_row = [
            session_id,
            current_date,
            current_time,
            entry.benutzer_name,
            entry.klasse,
            entry.schule,
            entry.fach,
            entry.thema,
            entry.aufgabentyp,
            entry.schwierigkeitsgrad,
            entry.datei_name,
            entry.datei_typ,
            entry.anzahl_aufgaben,
            entry.anzahl_teilaufgaben,
            entry.visualisierungen_genutzt,
            entry.animationen_genutzt,
            entry.grafiken_genutzt,
            entry.loesungen_angezeigt,
            entry.feedback,
            entry.sitzungsdauer_minuten,
            entry.notizen
        ]
        
        # Write data to row
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        for col_num, value in enumerate(data_row, 1):
            cell = ws.cell(row=next_row, column=col_num)
            cell.value = value
            cell.border = border
            cell.alignment = Alignment(horizontal='left', vertical='center')
        
        # Save workbook
        wb.save(EXCEL_PATH)
        wb.close()
        
        print(f"[LOG] Session logged successfully: {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "message": "Session erfolgreich protokolliert",
            "row": next_row
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[ERROR] Failed to log session: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to log session: {str(e)}"
        )

# ------------------------------
# Assessment Logging Endpoint
# ------------------------------
@app.post("/log-assessment")
async def log_assessment(assessment_data: dict = Body(...)):
    """
    Log post-session assessment to separate Excel sheet (Assessment_Log).
    This endpoint receives tutor/evaluator ratings and observations.
    """
    try:
        print("[ASSESSMENT] Starting assessment log...")
        
        # Check if Excel file exists
        if not os.path.exists(EXCEL_PATH):
            raise HTTPException(
                status_code=404,
                detail="Session log file not found. Please complete a session first."
            )
        
        # Load workbook
        wb = load_workbook(EXCEL_PATH)
        
        # Import styling classes OUTSIDE conditional block (needed for data rows too)
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
        
        # Create Assessment_Log sheet if it doesn't exist
        if "Assessment_Log" not in wb.sheetnames:
            ws = wb.create_sheet("Assessment_Log")
            
            # Define headers
            headers = [
                "Session-ID",
                "Assessment Date",
                "Assessment Time",
                "Assessor Name",
                "AI Question Quality",
                "Engagement Level",
                "Understanding Progress",
                "Efficiency Score",
                "Learner Type Indicator",
                "Question Loops Total",
                "Remarks",
                "Further Considerations",
                "Completion Status"
            ]
            
            # Write headers
            ws.append(headers)
            
            # Style headers (matching Session_Log style)
            header_font = Font(bold=True, color="FFFFFF", size=11)
            header_fill = PatternFill(
                start_color="2C5F8D",
                end_color="2C5F8D",
                fill_type="solid"
            )
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            for col_num, header in enumerate(headers, 1):
                col_letter = get_column_letter(col_num)
                cell = ws[f"{col_letter}1"]
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                
                # Set column widths
                if header in ["Remarks", "Further Considerations"]:
                    ws.column_dimensions[col_letter].width = 40
                elif header == "Session-ID":
                    ws.column_dimensions[col_letter].width = 15
                elif header == "Learner Type Indicator":
                    ws.column_dimensions[col_letter].width = 25
                else:
                    ws.column_dimensions[col_letter].width = 18
            
            print("[ASSESSMENT] Created new Assessment_Log sheet")
        else:
            ws = wb["Assessment_Log"]
        
        # Prepare assessment data row
        now = datetime.now()
        assessment_row = [
            assessment_data.get("sessionId", ""),
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            assessment_data.get("assessorName", "Nicht angegeben"),
            assessment_data.get("aiQuestionQuality", 0),
            assessment_data.get("engagementLevel", 0),
            assessment_data.get("understandingProgress", 0),
            assessment_data.get("efficiencyScore", 0),
            assessment_data.get("learnerTypeIndicator", "Nicht angegeben"),
            assessment_data.get("questionLoops", 0),
            assessment_data.get("remarks", ""),
            assessment_data.get("furtherConsiderations", ""),
            "Complete"
        ]
        
        # Find next row
        next_row = ws.max_row + 1
        
        # Write data with formatting
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        for col_num, value in enumerate(assessment_row, 1):
            cell = ws.cell(row=next_row, column=col_num)
            cell.value = value
            cell.border = border
            cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        
        # Save workbook
        wb.save(EXCEL_PATH)
        wb.close()
        
        session_id = assessment_data.get("sessionId", "Unknown")
        print(f"[ASSESSMENT] Assessment logged successfully for session: {session_id}")
        
        return {
            "success": True,
            "sessionId": session_id,
            "message": "Assessment erfolgreich protokolliert",
            "row": next_row
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"[ERROR] Failed to log assessment: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to log assessment: {str(e)}"
        )
