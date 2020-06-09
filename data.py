from datetime import datetime, timedelta
import requests
import json

# dataSource="https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json"
dataSource="https://opendata.ecdc.europa.eu/covid19/casedistribution/json"

# https://www.worldometers.info/world-population/population-by-country
ukPopulation = 67886011

# This file stores the produced rate data, starting on 08/06/2020
rateFile = "rate_data.txt"
rateData = json.load(open(rateFile))


# List of the last 14 dates
def get_report_dates():
    dates = []
    for i in range(0, 14):
        dayNdaysago = datetime.now() - timedelta(days=i)
        pretty = dayNdaysago.strftime('%d/%m/%Y')
        dates.append(pretty)

    fetch_latest_data(dates)


def fetch_latest_data(dates):
    data = dict()

    publicData = json.loads(requests.get(dataSource).text)

    for d in publicData["records"]:
        if d["countriesAndTerritories"] == "United_Kingdom" and d["dateRep"] in dates:
            data[d["dateRep"]] = d["cases"]

    print("Calculating using this New Cases data:")
    print(json.dumps(data))

    calc_rate(data)

# Calculate the rate over 100000 people
def calc_rate(data):
    try:
        allTheDates = [d for d in data]
        latestDate = allTheDates[0]

        allTheNumbers = [int(data[d]) for d in data]
        fourteenDayTotal = sum(allTheNumbers)

        fourteenDayRatePer100k = (fourteenDayTotal * 100000)/ukPopulation

        print("RATE=" + str(fourteenDayRatePer100k))

        write_rate_to_file(latestDate, fourteenDayRatePer100k)
    except KeyError:
        print("No data was published for today yet! Check rate_data.txt for historical rate data.")


# Write new rate data to a file
def write_rate_to_file(latestDate, fourteenDayRatePer100k):
    rateData[latestDate] = fourteenDayRatePer100k

    with open(rateFile, 'w') as file:
        file.write(json.dumps(rateData)) # use `json.loads` to do the reverse


get_report_dates()
