from datetime import datetime, timedelta
import requests
import json

dataSource="https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json"

ukPopulation = 66435600

# This file stores 14 days of daily data as of 08/06/2020 and gets updated with new data every time it arrives
dataFile = "daily_data.txt"
historicalData = json.load(open(dataFile))

# This file stores the produced rate data
rateFile = "rate_data.txt"
rateData = json.load(open(rateFile))


# List of the last 14 dates
dates = []
for i in range(0, 14):
    dayNdaysago = datetime.now() - timedelta(days=i)
    pretty = dayNdaysago.strftime('%d/%m/%Y')
    dates.append(pretty)


def fetch_latest_data(historicalData):
    response = json.loads(requests.get(dataSource).text)

    lastUpdatedAt=response["metadata"]["lastUpdatedAt"]
    latestNumber=response["dailyRecords"]["dailyLabConfirmedCases"]

    latestDate = datetime.strptime(lastUpdatedAt.split(sep="T")[0], '%Y-%m-%d').strftime('%d/%m/%Y')

    # If data from API is not in the historical data file - add it
    if latestDate not in historicalData:
        historicalData[latestDate] = latestNumber

        # Write new UK data to dataFile
        print("NEW DATA!")
        with open(dataFile, 'w') as file:
            file.write(json.dumps(historicalData)) # use `json.loads` to do the reverse
    else:
        print("No new data was published since the last update!")

    calc_rate(latestDate, historicalData)


# Calculate the rate over 100000 people
def calc_rate(latestDate, historicalData):
    try:
        fourteenDayNumbers = [historicalData[d] for d in dates]

        fourteenDayTotal = sum(fourteenDayNumbers)

        ukFourteenDayRatePer100k = (fourteenDayTotal * 100000)/ukPopulation
        print("RATE=" + str(ukFourteenDayRatePer100k))

        write_rate_to_file(latestDate, ukFourteenDayRatePer100k)
    except KeyError:
        print("No data was published for today yet!")


# Write new rate data to a file
def write_rate_to_file(latestDate, ukFourteenDayRatePer100k):
    rateData[latestDate] = ukFourteenDayRatePer100k

    with open(rateFile, 'w') as file:
        file.write(json.dumps(rateData)) # use `json.loads` to do the reverse


fetch_latest_data(historicalData)
