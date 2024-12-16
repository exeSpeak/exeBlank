from datetime import datetime

# Game start date set to December 8, 2024 at 8:00 AM
newGame_startDate = datetime(2024, 12, 8, 8, 0, 0)

def returnStartDateAsString():
    """Return the game start date in YYYY-MM-DD format"""
    return newGame_startDate.strftime("%Y-%m-%d")