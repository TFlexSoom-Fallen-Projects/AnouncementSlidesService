# Tristan Hilbert
# 5/27/2020
# Simple Test Runner for Birthday Test
#
#

from birthday import _test_get_month_day_tuple

from b_parser import parse_csv, get_birthday_list, _test_get_birthdays_from_range

if __name__ == "__main__":
    _test_get_month_day_tuple()
    parse_csv("test-files/Birthdays-Tristan.csv")
    print(get_birthday_list())

    _test_get_birthdays_from_range()
    
    