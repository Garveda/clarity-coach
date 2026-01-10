"""
Create Excel Session Log Template
This script creates the Clarity_Coach_Session_Log.xlsx file with proper structure
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

def create_session_log_template():
    """Create the Excel template for session logging"""
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Session_Log"
    
    # Define headers
    headers = [
        "Session_ID",
        "Datum",
        "Uhrzeit",
        "Benutzer_Name",
        "Klasse",
        "Schule",
        "Fach",
        "Thema",
        "Aufgabentyp",
        "Schwierigkeitsgrad",
        "Datei_Name",
        "Datei_Typ",
        "Anzahl_Aufgaben",
        "Anzahl_Teilaufgaben",
        "Visualisierungen_Genutzt",
        "Animationen_Genutzt",
        "Grafiken_Genutzt",
        "Lösungen_Angezeigt",
        "Feedback",
        "Sitzungsdauer_Minuten",
        "Notizen"
    ]
    
    # Style definitions
    header_fill = PatternFill(start_color="1e3a5f", end_color="1e3a5f", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=11)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Write headers
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = border
    
    # Set column widths
    column_widths = {
        'A': 12,  # Session_ID
        'B': 12,  # Datum
        'C': 10,  # Uhrzeit
        'D': 18,  # Benutzer_Name
        'E': 10,  # Klasse
        'F': 20,  # Schule
        'G': 15,  # Fach
        'H': 25,  # Thema
        'I': 18,  # Aufgabentyp
        'J': 16,  # Schwierigkeitsgrad
        'K': 20,  # Datei_Name
        'L': 12,  # Datei_Typ
        'M': 15,  # Anzahl_Aufgaben
        'N': 18,  # Anzahl_Teilaufgaben
        'O': 20,  # Visualisierungen_Genutzt
        'P': 20,  # Animationen_Genutzt
        'Q': 18,  # Grafiken_Genutzt
        'R': 18,  # Lösungen_Angezeigt
        'S': 15,  # Feedback
        'T': 20,  # Sitzungsdauer_Minuten
        'U': 30,  # Notizen
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # Set row height for header
    ws.row_dimensions[1].height = 30
    
    # Add example row (optional, can be removed)
    example_data = [
        "001",
        datetime.now().strftime("%Y-%m-%d"),
        datetime.now().strftime("%H:%M:%S"),
        "Max Mustermann",
        "10a",
        "Gymnasium Beispiel",
        "Mathematik",
        "Quadratische Gleichungen",
        "Gleichungen lösen",
        "Mittel",
        "aufgabe_quadratisch.pdf",
        "PDF",
        "1",
        "3",
        "2",
        "1",
        "0",
        "3",
        "Helpful",
        "15.5",
        "Gute Fortschritte beim Verständnis"
    ]
    
    for col_num, value in enumerate(example_data, 1):
        cell = ws.cell(row=2, column=col_num)
        cell.value = value
        cell.border = border
        cell.alignment = Alignment(horizontal='left', vertical='center')
    
    # Freeze first row
    ws.freeze_panes = 'A2'
    
    # Save file
    output_path = r"C:\Users\admin\Desktop\Sonstiges\HMS_PROJEKT\clarity-coach\Clarity_Coach_Session_Log.xlsx"
    wb.save(output_path)
    print(f"[SUCCESS] Excel template created at: {output_path}")
    print(f"[INFO] Template includes {len(headers)} columns")
    return output_path

if __name__ == "__main__":
    create_session_log_template()
