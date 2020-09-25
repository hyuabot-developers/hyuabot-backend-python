# External Module
import json
from datetime import datetime
from workalendar.asia import SouthKorea

# Internal Module
from transport.shuttle.date import is_semester

cal = SouthKorea()
now = datetime.now()
def get_departure_info():
    bool_semester = is_semester()
    term = {
        'halt':'/halt',
        'semester':'/semester',
        'vacation_session':'/vacation_session',
        
    }