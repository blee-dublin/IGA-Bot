# Retrieve EGD (European Go Database) information 

import requests
import json


def getEGDPlayerByPin(pin):
  print()
  response = requests.get(
      "https://www.europeangodatabase.eu/EGD/GetPlayerDataByPIN.php?pin=" +
      pin)
  parseData = response.json()

  fname = parseData["Name"]
  lname = parseData["Last_Name"]
  country = parseData["Country_Code"]
  club = parseData["Club"]
  grade = parseData["Grade"]
  egf_place = parseData["EGF_Placement"]
  GoR = parseData["Gor"]
  tot_t = parseData["Tot_Tournaments"]
  last_a = parseData["Last_Appearance"]

  result = fname + ' ' + lname + ', ' + country + ', ' + club + '\nGrade: ' + grade + ', GoR: ' + GoR + ', EGF placement: ' + egf_place + '\nTotal Tournaments: ' + tot_t + ', Last Appearance: ' + last_a

  print(result)
  return result


def getEGDPlayerByNames(names):
  print()

  if len(names) == 2:
    print(names[1])
    response = requests.get(
        "https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php?lastname="
        + names[1])
  elif len(names) == 3:
    print(names[1] + ' ' + names[2])
    response = requests.get(
        "https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php?lastname="
        + names[1] + "&name=" + names[2])

  parseData = response.json()

  formatted_data = json.dumps(parseData,
                              indent=4).replace('"', "").replace(',', "")

  print(formatted_data)

  if len(formatted_data) > 2000:
    formatted_data = ":information_source:  Returned data is too big to display  :information_source:"

  return formatted_data

