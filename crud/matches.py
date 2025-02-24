from sqlalchemy.orm import Session
from models.match import Match


# Додавання нового матчу
def add_match(db: Session, match_data: dict):
    new_match = Match(
        match_id=match_data["match_id"],
        team1=match_data["team1"],
        team2=match_data["team2"],
        time=match_data["time"],
        score_team1=match_data["score_team1"],
        score_team2=match_data["score_team2"],
        period=match_data["period"],
    )
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    return new_match


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
