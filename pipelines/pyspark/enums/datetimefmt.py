from enum import StrEnum


class DatetimeLevel(StrEnum):
    weeks = "weeks"
    days = "days"
    hours = "hours"
    minutes = "minutes"
    seconds = "seconds"


class DatetimeFmt(StrEnum):
    date_format = ("yyyy-MM-dd",)
    timestamp_format = ("yyyy-MM-dd'T'HH:mm:ss[.SSS]",)


if __name__ == "__main__":
    print(DatetimeLevel._member_map_.values())
    print(DatetimeLevel.seconds)
    print(type(DatetimeLevel.seconds))
