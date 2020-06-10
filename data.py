from datetime import datetime, timedelta
import requests
import json

dataSource="https://opendata.ecdc.europa.eu/covid19/casedistribution/json"

# https://www.worldometers.info/world-population/population-by-country
ukPopulation = 67886011

timeWindow = 14

# This file stores the produced number data, starting on 09/06/2020
rateFile = "rate_data.txt"
rateData = json.load(open(rateFile))

# Date today
today = datetime.today()

# List of the last 14 dates
def get_report_dates():
    timestamps = [today - timedelta(days=x) for x in range(timeWindow)]
    dates = [d.strftime('%d/%m/%Y') for d in timestamps]

    if str(today.strftime('%d/%m/%Y')) in rateData:
         print("Data for today has already been fetched. Here's results:")
         print(json.dumps(rateData, indent=4))
    else:
        fetch_latest_data(dates)

# Get data from dataSource
def fetch_latest_data(dates):
    publicData = json.loads(requests.get(dataSource).text)
    data = {d["dateRep"]: int(d["cases"]) for d in publicData["records"] if d["countriesAndTerritories"] == "United_Kingdom" and d["dateRep"] in dates}

    if str(today.strftime('%d/%m/%Y')) in data:
        print("Calculating using this New Cases data:")
        print(json.dumps(data, indent=4))
        calc_rate(data)
    else:
        print("No data has been published for today yet. Here's previous results:")
        print(json.dumps(rateData, indent=4))

# Calculate the rate over 100000 people
def calc_rate(data):
    allDayTotal = sum(list(data.values()))

    numberPer100k = (allDayTotal * 100000)/ukPopulation

    print("RATE: " + str(numberPer100k))

    write_rate_to_file(numberPer100k)

# Write new rate data to a file
def write_rate_to_file(numberPer100k):
    rateData[str(today.strftime('%d/%m/%Y'))] = numberPer100k

    with open(rateFile, 'w') as file:
        file.write(json.dumps(rateData, indent=4))

get_report_dates()
