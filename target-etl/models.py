from enum import StrEnum


class SIGNALCOLUMNS(StrEnum):
    NAME='name'
    DATA='data'
    TIMESTAMP='timestamp'
    SIGNAL_ID='signal_id'
    VALUE='value'

class DATACOLUMNS(StrEnum):
     TIMESTAMP='timestamp'
     WIND_SPEED='wind_speed'
     POWER='power'
     AMBIENT_TEMPERATURE='ambient_temperature'
