import isodate
from datetime import timedelta
from json_parsing import parse_work_time_to_normal_time, parse_normal_time_to_work_time


print(parse_work_time_to_normal_time("P1W1DT2H2S"))
print(parse_normal_time_to_work_time("P2DT2H2S"))

# print(isodate.parse_duration('PT20H'))
#
# work_hours = timedelta(hours=0.5 * 40)
# print(work_hours)
# print(isodate.duration_isoformat(work_hours))
