import requests
from datetime import datetime
import pandas as pd
import json
import time
from datetime import timedelta
import os.path

class WeatherClient(object):

    def __init__(self):
        self.next_req_time = datetime.fromtimestamp(0)
        self.min_rate = 10
        self.day_rate = 1000
        self.num_requests = 0


    def get_hist_weather(self, start_dt, end_dt):
        # https://developer.weathersource.com/documentation/resources/get-history/
        # Example Value: 2004-02-12T08:00+00:00,2004-02-12T23:00+00:00

        time_st = start_dt.isoformat() + ',' + end_dt.isoformat()

        res_fields = 'postal_code,country,timestamp,temp,precip,precipConf,snowfall,snowfallConf,windSpd,windDir,' \
                     'cldCvr,dewPt,feelsLike,relHum,sfcPres,spcHum,wetBulb'

        payload = {'postal_code_eq': '55455', 'country_eq': 'US', 'timestamp_between': time_st, 'period': 'hour',
                   'fields': res_fields, 'limit': 25}

        self._wait_for_rate_limit()
        self.resp = requests.get('https://api.weathersource.com/v1/d1bbff6bdd505dc6e7a8/history_by_postal_code.json?',
                         params=payload)
        self._update_rate_limit()
        return


    def save_as_csv(self, file_out):
        # write data to csv file
        data = json.dumps(self.resp.json())
        df = pd.read_json(data)
        # check file exists, write header if new file
        if not os.path.isfile(file_out):
            df.to_csv(file_out, index=False)
        else:
            # file already exists don't write header again
            df.to_csv(file_out, index=False, header=False, mode='a')
        return

    def _wait_for_rate_limit(self):
        now = datetime.now()

        # daily rate limit handling
        if self.num_requests >= 1000:
            self.next_req_time + timedelta(days=1)
            self.num_requests = 0

        # sleep until ready
        if self.next_req_time > now:
            t = self.next_req_time - now
            time.sleep(t.total_seconds())

    def _update_rate_limit(self):
        request_latency = 0.2
        now = datetime.now()
        self.num_requests += 1
        self.next_req_time = now + timedelta(seconds=(60 / self.min_rate) + request_latency)
