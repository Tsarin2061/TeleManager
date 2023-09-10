from functions import process_date
from datetime import datetime,timedelta

def test_process_date():
    present_day = datetime.now()
    tomorrow_day = present_day + timedelta(1)
    assert process_date("10:11") == f"{present_day.strftime('%d/%m/%Y')} 10:11"