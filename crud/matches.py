from sqlalchemy.orm import Session
from database import SessionLocal
from models.match import Match
from datetime import datetime, timedelta
from sqlalchemy import select, and_


# Додавання нового матчу
def add_match(db: Session, match_data: dict):
    new_match = Match(
        match_id=match_data["match_id"],
        league=match_data["league"],
        team1=match_data["team1"],
        team2=match_data["team2"],
        status=match_data["status"],
        curr_period_quarter=match_data["cps"],
        additional_info=match_data["information"],
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match


# Додавання або оновлення кількох матчів за один запит
def add_or_update_matches(matches_data: list):
    db: Session = SessionLocal()

    # Отримуємо всі match_id, які були створені сьогодні
    today = datetime.now().date()
    existing_matches = {
        row[0]: row[1]
        for row in db.execute(
            select(Match.match_id, Match.status).where(
                and_(
                    Match.match_id.in_([match["match_id"] for match in matches_data]),
                    Match.created_at >= datetime.combine(today, datetime.min.time()),
                    Match.created_at
                    < datetime.combine(today + timedelta(days=1), datetime.min.time()),
                )
            )
        ).fetchall()
    }

    new_matches = []
    for match in matches_data:
        match_id = match["match_id"]
        new_status = match["status"]

        # Якщо матч вже існує і статус змінився
        if match_id in existing_matches and existing_matches[match_id] != new_status:
            db.query(Match).filter(Match.match_id == match_id).update(
                {
                    "status": new_status,
                    "curr_period_quarter": match.get("cps", ""),
                    "additional_info": match.get("information", ""),
                }
            )
        # Якщо такого match_id ще немає, додаємо новий запис
        elif match_id not in existing_matches:
            new_matches.append(
                Match(
                    match_id=match_id,
                    league=match["league"],
                    team1=match["team1"],
                    team2=match["team2"],
                    status=new_status,
                    curr_period_quarter=match.get("cps", ""),
                    additional_info=match.get("information", ""),
                )
            )

    # Масове додавання нових матчів, якщо є
    if new_matches:
        db.bulk_save_objects(new_matches)

    db.commit()
    return new_matches


# Оновлення матчу
def update_match(db: Session, match_id: str, match_data: dict):
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if match:
        match.team1 = match_data["team1"]
        match.team2 = match_data["team2"]
        match.time = match_data["time"]
        match.score_team1 = match_data["score_team1"]
        match.score_team2 = match_data["score_team2"]
        match.period = match_data["period"]
        db.commit()
        db.refresh(match)
    return match


# Отримання матчу за match_id
def get_match_by_id(db: Session, match_id: str):
    return db.query(Match).filter(Match.match_id == match_id).first()


def get_live_matches():
    db: Session = SessionLocal()
    live_matches = db.query(Match).filter(Match.status.in_(["live", "scheduled"])).all()
    db.close()
    return live_matches


def get_finished_matches():
    db: Session = SessionLocal()
    affected_rows = (
        db.query(Match)
        .filter(
            Match.status.in_(["scheduled", "live"]),
            Match.created_at < datetime.today().date(),
        )
        .update({"status": "finished"})
    )
    db.commit()
    db.close()

    print(f"Оновлено {affected_rows} матчів на статус 'finished'.")


# Функція для зміни статусу матчу на 'finished' за match_id
def finish_match_by_id(match_id: int):
    db: Session = SessionLocal()
    try:
        affected_rows = (
            db.query(Match)
            .filter(Match.match_id == match_id)
            .update({"status": "finished"})
        )
        db.commit()
        print(f"Матч з match_id={match_id} оновлено на статус 'finished'.")
    except Exception as e:
        db.rollback()
        print(f"Помилка при оновленні статусу матчу: {e}")
    finally:
        db.close()
