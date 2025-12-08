### The relevant chunk of the 24 hour weather forecast api response
# {
#   "code": 0,
#   "data": {
#     "records": [
#       {
#         "date": "2025-12-05",
#         "updatedTimestamp": "2025-12-05T20:40:47+08:00",
#         "general": {
#           "temperature": {
#             "low": 24,
#             "high": 33,
#             "unit": "Degrees Celsius"
#           },
#           "relativeHumidity": {
#             "low": 60,
#             "high": 95,
#             "unit": "Percentage"
#           },
#           "forecast": {
#             "code": "TL",
#             "text": "Thundery Showers"
#           },
#           "validPeriod": {
#             "start": "2025-12-05T18:00:00+08:00",
#             "end": "2025-12-06T18:00:00+08:00",
#             "text": "6 PM 5 Dec to 6 PM 6 Dec"
#           },
#           "wind": {
#             "speed": {
#               "low": 15,
#               "high": 25
#             },
#             "direction": "N"
#           }
#         },

date = response["data"]["records"]["date"] # i.e., "date": "2025-12-05",
update_timestamp = response["data"]["records"]["updatedTimestamp"] # i.e., "updatedTimestamp": "2025-12-05T20:40:47+08:00"
temp_low = response["data"]["records"]["general"]["temperature"]["low"] # i.e., "low": 24,
temp_high = response["data"]["records"]["general"]["temperature"]["high"] # i.e., "high": 33,
temp_unit = response["data"]["records"]["general"]["temperature"]["unit"] # i.e., "unit": "Degrees Celsius"
humid_low = response["data"]["records"]["general"]["relativeHumidity"]["low"] # i.e., "low": 60,
humid_high = response["data"]["records"]["general"]["relativeHumidity"]["high"] # i.e., "high": 95,
humid_unit = response["data"]["records"]["general"]["relativeHumidity"]["unit"] # i.e., "unit": "Percentage"
forecast_code = response["data"]["records"]["general"]["forecast"]["code"] # i.e., "code": "TL",
forecast_text = response["data"]["records"]["general"]["forecast"]["text"] # i.e., "text": "Thundery Showers"
valid_range = response["data"]["records"]["general"]["validPeriod"]["text"] # i.e., "text": "6 PM 5 Dec to 6 PM 6 Dec"
wind_low = response["data"]["records"]["general"]["wind"]["speed"]["low"] # i.e., "low": 15,
wind_high = response["data"]["records"]["general"]["wind"]["speed"]["high"] # i.e., "high": 25
wind_dir = response["data"]["records"]["general"]["wind"]["direction"] # i.e., "direction": "N"

