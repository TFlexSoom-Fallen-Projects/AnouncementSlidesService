# Tristan Hilbert
# 5/27/2020
# Object Definition For Birthday for better resolutions


# Get's a string in the format "mm/dd"
# Returns a tuple
def _get_month_day_tuple(date_str):
    parts = date_str.split("/")
    if(len(parts) != 2):
        raise RuntimeError

    month = int(parts[0])
    day = int(parts[1])

    if month <= 0 or month >= 13:
        raise RuntimeError
    if day <= 0 or day >= 31:
        raise RuntimeError

    return (month, day)

# Test Function for get_month_day_tuple to make sure it
# works and errors correctly. Sanity checks and all!
def _test_get_month_day_tuple():
    assert (10, 30) == _get_month_day_tuple("10/30")
    assert (1, 30) == _get_month_day_tuple("1/30")
    assert (1, 3) == _get_month_day_tuple("1/3")
    bad_input = ["", "13/1", "0/0", "2/35", "30/30", "/23", "10/"]
    for b in bad_input:
        try:
            _get_month_day_tuple(b)
            print(b + "  - Was Erroneously successful!")
            raise AssertionError    
        except AssertionError as e:
            raise AssertionError

        except Exception as e:
            pass    


class Birthday:

    # Constructor
    # tple: (fname, lname, date_str, grade)
    def __init__(self, tple):
        self.fname = tple[0]
        self.lname = tple[1]
        self.date_str = tple[2]
        self.grade = tple[3]

        # Add month and day fields
        self._parse_datestr()

    def get_month(self):
        return self.month
    

    def get_day(self):
        return self.day
    

    def _parse_datestr(self):
        self.month, self.day = _get_month_day_tuple(self.date_str)

    def __repr__(self):
        name = "name: " + self.fname + " " + self.lname
        g = "grade: " + self.grade
        bday_str = "bday: " + self.date_str

        return "(" + name + ", " + g + ", " + bday_str + ")"

