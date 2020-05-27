# Tristan Hilbert
# 5/26/2020
# Birthday Date CSV Parser
#
#

from birthday import Birthday
import csv
from itertools import islice
import datetime
from operator import attrgetter

# A map might be better here for lookups, 
# but we'll use a list for now
_birthday_object_list = []

# Here I go with some pre-optimization O.O
# We can use a list of lookups for the start of each
# month

# 1 - Month of the year => Index in birthday_tuple_list
# 0 will also default to the same values as it's neighbor
_month_lookups = []

# Check if we have parsed a file or not
# This is done by checking if we have populated month_lookups yet
def _has_parsed_file():
    return len(_month_lookups) != 0

def parse_csv(path):
    global _month_lookups, _birthday_object_list

    _month_lookups = []
    _birthday_object_list = []

    # CSV Format: "fname", "lname", "birthday", "grade"
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        # Assumes the first row are labels
        for row in islice(reader, 1, None):
            # Discard Empty Rows
            if(row[2] == ""):
                continue

            # Append Birthday Object
            _birthday_object_list.append( Birthday(row) )

    _birthday_object_list.sort(key=attrgetter("month", "day"))

    # Prepare to setup lookup table for list
    month = _birthday_object_list[0].month

    # Any months skipped should be at 0 including non-month 0
    for i in range(month + 1):
        _month_lookups.append(0)

    for i in range(len(_birthday_object_list)):
        if _birthday_object_list[i].month > month:
            new_month = _birthday_object_list[i].month
            for j in range(new_month - month):
                _month_lookups.append(i)
            
            month = new_month

# Assumes Date Object
# Inclusive Range
def get_birthdays_from_range(beg_date, end_date):
    global _month_lookups, _birthday_object_list

    res = []
    starting_index = _month_lookups[beg_date.month]
    
    # Assure that starting index is < end_date but >= beg_date
    while _birthday_object_list[starting_index].month == beg_date.month and _birthday_object_list[starting_index].day < beg_date.day:
        starting_index += 1
    
    ending_index = starting_index

    while _birthday_object_list[ending_index].month < end_date.month:
        ending_index += 1

    while _birthday_object_list[ending_index].month == end_date.month and _birthday_object_list[ending_index].day <= end_date.day:
        ending_index += 1

    # Now the range [starting_index, ending_index) should be good to go
    if starting_index != ending_index:
        return _birthday_object_list[starting_index : ending_index]
    else:
        return []



# Should hold other interfaces
def get_birthday_list():
    global _birthday_object_list
    if(_has_parsed_file()):
        return _birthday_object_list
    else:
        print("Birthday Parser needs to run the function")
        print("   parse_csv   ")
        print("first!")
        raise RuntimeError

def _get_month_lookup():
    global _birthday_object_list
    return _month_lookups




# The tests pass, but I would like to see more
# erroneous output tried out within this function!
#
def _test_get_birthdays_from_range():
    global _month_lookups, _birthday_object_list

    temp = _month_lookups
    temp1 = _birthday_object_list

    parse_csv("test-files/Birthdays-Tristan.csv")

    beg_date = datetime.date(2020, 1, 24)
    end_date = datetime.date(2020, 1, 24)

    print("\n")
    print(_month_lookups)
    print("\n")
    
    assert len(get_birthdays_from_range(beg_date, end_date)) == 0

    beg_date = datetime.date(2020, 2, 20)
    end_date = datetime.date(2020, 3, 20)

    assert len(get_birthdays_from_range(beg_date, end_date)) == 4

    beg_date = datetime.date(2020, 6, 3)
    end_date = datetime.date(2020, 6, 6)

    assert len(get_birthdays_from_range(beg_date, end_date)) == 2

    _month_lookups = temp
    _birthday_object_list = temp1