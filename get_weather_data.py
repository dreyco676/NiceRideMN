import weather
from datetime import datetime
from datetime import timedelta

# 2014-11-26T00:00,2014-11-26T23:59
wc = weather.WeatherClient()

# first day to get data
start_dt = datetime.strptime('2014-11-26T00:00', '%Y-%m-%dT%H:%M')
# end of first day to get data
eod_start_dt = datetime.strptime('2014-11-26T23:59', '%Y-%m-%dT%H:%M')
# last day to get data
end_dt = datetime.strptime('2015-07-01', '%Y-%m-%d') + timedelta(days=1)

while eod_start_dt < end_dt:
    time_st = start_dt.strftime('%Y-%m-%dT%H:%M') + ',' + eod_start_dt.strftime('%Y-%m-%dT%H:%M')
    print(time_st)
    resp = wc.get_hist_weather(start_dt,eod_start_dt)
    wc.save_as_csv('weather_hist.csv')

    # increment dates
    start_dt = start_dt + timedelta(days=1)
    eod_start_dt = eod_start_dt + timedelta(days=1)