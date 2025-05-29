import gspread
from loguru import logger

from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials


scope = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_service_account_file('client_secret.json', scopes = scope)

client = gspread.authorize(creds)

sheet_id = '1yii1U2gSj0stX3D5IDuS4EyZJicyhx_cluceXLG5JLc'
sheet = client.open_by_key(sheet_id)

worksheet = sheet.get_worksheet(0)

def save_appointment(user_id: int, name: str, phone: str, service: str, date: str, time: str):
    row = [user_id, name, phone, service, date, time, 'новая']
    worksheet.append_row(row)

def get_appointments_for_date(date: str) -> list:
    """Возвращает список времени, уже занятого на указанную дату"""
    busy_times = []
    records = worksheet.get_all_values()[1:]  # Пропускаем заголовок

    for row in records:
        if len(row) < 7:
            continue  # Пропустить неполные строки

        record_date = row[4].strip()
        record_time = row[5].strip()
        status = row[6].strip().lower()

        if record_date == date and status == 'новая':
            busy_times.append(record_time)

    return busy_times

def clear_old_appointments():
    records = worksheet.get_all_values()
    now = datetime.now()
    odt = (now - timedelta(days=2))

    for i, row in enumerate(records[1:], start=2):  # Пропускаем заголовок, строки начинаются с 2
        date_str = row[4].strip()
        time_str = row[5].strip()
        status = row[6].strip().lower()

        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
            if dt < now and status == "новая":
                worksheet.update_cell(i, 7, "просрочено")
                logger.debug("1 заявка просрочена")
            elif odt < dt and status == "просрочено":
                worksheet.delete_rows(i)
                logger.debug("1 заявка удалена")
        except Exception as e:
            print(f"Ошибка в строке {i}: {e}")
