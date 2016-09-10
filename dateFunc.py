import datetime

time1 = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
time2 = "2016-09-08T08:41:35Z"
time2 = datetime.datetime.strptime(time2,"%Y-%m-%dT%H:%M:%SZ")
time2 = datetime.datetime.strptime(str(time2),"%Y-%m-%d %H:%M:%S")
print time1
print time2

timeDiff = time1 - time2
timeDiff = int(timeDiff.total_seconds() / (60*60))
print timeDiff
