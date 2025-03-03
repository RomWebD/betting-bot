import sys
import os

# Додаємо кореневу папку проєкту в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
from models.match import Match
from models.coefficient import Coefficient
from openpyxl import Workbook
import json
from collections import defaultdict


def extract_total_by_quarter(values_json, cps):
    """Витягує Total для кожної чверті з JSON, враховуючи cps"""
    total_data = {
        "Full Match": None,
        "1st Quarter": None,
        "2nd Quarter": None,
        "3rd Quarter": None,
        "4th Quarter": None,
    }
    try:
        cps = int(cps) if cps else 0
        for item in values_json:
            block_name = item.get("block_name", "")
            if "Total" in block_name:
                # Full Match
                if (
                    "1st quarter" not in block_name
                    and "2nd quarter" not in block_name
                    and "3rd quarter" not in block_name
                    and "4th quarter" not in block_name
                ):
                    if cps == 1:
                        total_data["1st Quarter"] = item.get("coefficient_data", [])
                    elif cps == 2:
                        total_data["2nd Quarter"] = item.get("coefficient_data", [])
                    elif cps == 3:
                        total_data["3rd Quarter"] = item.get("coefficient_data", [])
                    elif cps == 4:
                        total_data["4th Quarter"] = item.get("coefficient_data", [])
                    else:
                        total_data["Full Match"] = item.get("coefficient_data", [])
                elif "1st quarter" in block_name:
                    total_data["1st Quarter"] = item.get("coefficient_data", [])
                elif "2nd quarter" in block_name:
                    total_data["2nd Quarter"] = item.get("coefficient_data", [])
                elif "3rd quarter" in block_name:
                    total_data["3rd Quarter"] = item.get("coefficient_data", [])
                elif "4th quarter" in block_name:
                    total_data["4th Quarter"] = item.get("coefficient_data", [])
    except Exception as e:
        print(f"Error extracting totals: {e}")

    return total_data


def export_coefficients_to_excel():
    db: Session = SessionLocal()

    # Витягуємо ВСІ коефіцієнти з БД
    coefficients = db.query(Coefficient).all()

    # Групуємо коефіцієнти по match_id
    match_coefficients = defaultdict(list)
    for coef in coefficients:
        match_coefficients[coef.match_id].append(coef)

    # Відбираємо тільки ті матчі, де є всі 4 квартали (cp=1,2,3,4)
    valid_match_ids = []
    for match_id, coefs in match_coefficients.items():
        cp_values = {coef.cp for coef in coefs}
        if {"1", "2", "3", "4"}.issubset(cp_values):  # Якщо є всі 4 чверті
            valid_match_ids.append(match_id)

    # Тепер беремо всі матчі, які залишилися після фільтрації
    matches = db.query(Match).filter(Match.match_id.in_(valid_match_ids)).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Coefficients Data"

    # Заголовки таблиці
    headers = [
        "Match ID",
        "League",
        "Team 1",
        "Team 2",
        "cps",
        "Status",
        "Total - Full Match",
        "Total - 1st Quarter",
        "Total - 2nd Quarter",
        "Total - 3rd Quarter",
        "Total - 4th Quarter",
        "score1",
        "score2",
        "time",
    ]
    ws.append(headers)

    # Заповнення таблиці даними
    for match in matches:
        coefs = match_coefficients[match.match_id]

        for coef in coefs:
            values = coef.values
            if isinstance(values, str):
                values = json.loads(values)
            total_data = extract_total_by_quarter(values, coef.cp)

            row = [
                match.match_id,
                match.league,
                match.team1,
                match.team2,
                coef.cp,
                match.status,
                json.dumps(total_data["Full Match"], ensure_ascii=False),
                json.dumps(total_data["1st Quarter"], ensure_ascii=False),
                json.dumps(total_data["2nd Quarter"], ensure_ascii=False),
                json.dumps(total_data["3rd Quarter"], ensure_ascii=False),
                json.dumps(total_data["4th Quarter"], ensure_ascii=False),
                coef.score1,
                coef.score2,
                coef.time,
            ]
            ws.append(row)

    # Збереження в Excel
    output_file = "data/coefficients_data.xlsx"
    wb.save(output_file)
    print(f"✅ Дані збережено у файлі: {output_file}")

    db.close()


if __name__ == "__main__":
    export_coefficients_to_excel()
