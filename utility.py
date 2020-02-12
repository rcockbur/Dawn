from globals import *
from random import randint
import time
print("running utility.py")

string_length = 5

def measure(func):
    def wrapper(*args, **kwargs):
        t = time.time()
        r = func(*args, **kwargs)
        t = time.time() - t
        if hasattr(func, "total_time"):
            func.total_time = func.total_time + t
            func.count = func.count + 1
        else:
            func.total_time = t
            func.count = 1
        t_average = func.total_time / func.count
        str_average = str(round(t_average, string_length))
        str_current = str(round(t, string_length))
        for i in range(string_length + 2 - len(str_average)):
            str_average = str_average + "0"
        for i in range(string_length + 2 - len(str_current)):
            str_current = str_current + "0"
        print("func:",func.__name__, "  time:", str_current, "  avg:", str_average)
        return r
    return wrapper

def format_date(date):
    if date[DT_DAY_OM] < 10:
        day_string = "0" + str(date[DT_DAY_OM])
    else:
        day_string = str(date[DT_DAY_OM])
    return MONTH_NAMES[date[DT_MONTH_OY]] + " " + day_string + ", " + str(date[DT_YEAR])

def format_datetime(date):
    if date[DT_HOUR_OD] < 10:
        hour_string = "0" + str(date[DT_HOUR_OD]) + ":00"
    else:
        hour_string = str(date[DT_HOUR_OD]) + ":00"

    if date[DT_DAY_OM] < 10:
        day_string = "0" + str(date[DT_DAY_OM])
    else:
        day_string = str(date[DT_DAY_OM])

    return hour_string + " " + MONTH_NAMES[date[DT_MONTH_OY]] + " " + day_string + ", " + str(date[DT_YEAR])



def format_datetime_from_hour(hour):
    if hour is not None:
        day = hour // HOURS_PER_DAY
        month = day // DAYS_PER_MONTH
        year = month // MONTHS_PER_YEAR
        hour_of_day = hour % HOURS_PER_DAY
        day_of_month = day % DAYS_PER_MONTH
        month_of_year = month % MONTHS_PER_YEAR

        if hour_of_day < 10:
            hour_string = "0" + str(hour_of_day) + ":00"
        else:
            hour_string = str(hour_of_day) + ":00"

        if day_of_month < 10:
            day_string = "0" + str(day_of_month)
        else:
            day_string = str(day_of_month)

        return hour_string + " " + MONTH_NAMES[month_of_year] + " " + day_string + ", " + str(year)
    else:
        return "None"

def format_type_list(_list):
    return "[" + ",".join((_item.__name__ for _item in _list)) + "]"

def format_ability_list(ability_list):
    return "[" + ",".join((_item.__class__.__name__ for _item in ability_list)) + "]"

def format_date_from_day(day):
    if day is not None:
        month = day // DAYS_PER_MONTH
        year = month // MONTHS_PER_YEAR
        day_of_month = day % DAYS_PER_MONTH
        month_of_year = month % MONTHS_PER_YEAR

        if day_of_month < 10:
            day_string = "0" + str(day_of_month)
        else:
            day_string = str(day_of_month)

        return MONTH_NAMES[month_of_year] + " " + day_string + ", " + str(year)
    else:
        return "None"

def format_name_from_id(id):
    entity = MAP.get_entity_by_id(id)
    if entity is not None:
        return entity.name
    entity = MAP.get_destroyed_entity_by_id(id)
    if entity is not None:
        return entity.name + "(D)"
    return "None"

def format_entity_header(unit):
    s = ""
    if hasattr(unit, "is_male"):
        if unit.is_male: s = "(M)"
        else: s = "(F) "

    if hasattr(unit, "age"):
        s = s + str(unit.age)

    return s 
    

def unit_report(entity_types):
    s = ""
    i = 0
    for unit_class in entity_types:
        i += 1
        if i == 2: 
            s = s + "    "
        num_born = unit_class.monthly_born
        num_died = unit_class.monthly_died_age + unit_class.monthly_died_starved + unit_class.monthly_died_hunted
        diff = num_born - num_died
        if diff >= 0:
            diff_sign = "+"
        else:
            diff_sign = "-"
        diff = abs(diff)
        s = s + unit_class.__name__ 
        count = len(MAP.get_entities_of_type(unit_class, False))
        if count < 100:
            s = s + " "
            if count < 10:
                s = s + " "
        s = s + "  " + str(count) + " "
        if diff < 100: s = s + " "
        if diff < 10: s = s + " "
        s = s + diff_sign + str(diff) + ":"
        if num_born < 10: s = s + " "
        s = s + "  +" + str(num_born) 
        if num_died < 10: s = s + " "
        s = s + "  -" + str(num_died)
        s = s + " "
        if unit_class.monthly_died_age < 10: s = s + " "
        s = s + str(unit_class.monthly_died_age) + "/"
        if unit_class.monthly_died_starved < 10: s = s + " "
        s = s + str(unit_class.monthly_died_starved) + "/"
        if unit_class.monthly_died_hunted < 10: s = s + " "
        s = s + str(unit_class.monthly_died_hunted)
        unit_class.monthly_born = 0
        unit_class.monthly_died_age = 0
        unit_class.monthly_died_hunted = 0
        unit_class.monthly_died_starved = 0
    print(s)

def weighted_random(pairs):
    boundary_temp = 0
    boundaries = [0]
    num_pairs = 0
    for pair in pairs:
        num_pairs+=1
        boundary_temp = boundary_temp + pair[1]
        boundaries.append(boundary_temp)
    if boundaries[num_pairs] > 0:
        chosen_int = randint(0, boundaries[num_pairs]-1)
        for boundary_lower in range(num_pairs):
            boundary_upper = boundary_lower + 1
            if boundaries[boundary_upper] > boundaries[boundary_lower]:
                if boundaries[boundary_upper] > chosen_int >= boundaries[boundary_lower]:
                    return pairs[boundary_lower][0]
        raise RuntimeError("No direction found")
    return None