from datetime import datetime, timedelta, date

class Shift:
    def __init__(self, date: str, hours=None):
        if hours:
            self.start = datetime.strptime(date + hours[0], "%d/%m/%y%H.%M")
            self.end = datetime.strptime(date + hours[1], "%d/%m/%y%H.%M")
            if self.end < self.start:
                self.end += timedelta(days=1)
            self.all_day = False
        else:     
            self.start = datetime.strptime(date, "%d/%m/%y")
            self.end = datetime.strptime(date, "%d/%m/%y")  
            self.all_day = True 

        self.summary = "Work" if not self.all_day else "Free"

        if self.all_day:
            self.colour = 11 # red
        elif self.start.hour <= 5:
            self.colour = 2 # sage
        else:
            self.colour = 10 # basil

    def get_start(self):
        if self.all_day:
            return datetime.strftime(self.start, "%Y-%m-%d")
        else:
            return self.start.isoformat() + "Z"

    def get_end(self):
        if self.all_day:
            return datetime.strftime(self.end, "%Y-%m-%d")
        else:
            return self.end.isoformat() + "Z"

    def calculate_hours(self):
        delta = self.end - self.start
        return delta.seconds / 3600 


if __name__ == "__main__":
    s1 = Shift("01/10/19")
    s2 = Shift("01/10/19", ["04.00", "12.00"])
    s3 = Shift("01/10/19", ["10.00", "12.00"])
    # print(s.start.isoformat("T"))
    # print(s.get_start())