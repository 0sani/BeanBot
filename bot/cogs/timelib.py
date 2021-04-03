class Time:
    def __init__(self, time):
        self.string = time
        self.seconds = 0

        ## Gets the number of seconds until unmute
        try:
            for i in time.split():
                self.seconds += int(i[:-1]) * {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}[i[-1]]
        except:
            raise TimeError


class TimeError(Exception):
    pass

