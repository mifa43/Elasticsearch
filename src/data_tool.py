import pandas as pd
import json
import matplotlib.pyplot as plt
import sys
#kreiranje data frejma
# mySet = {
#     "cars": ["BMW", "Audi", "Ford"],
#     "passings": [3, 7, 2]
# }

# myVar = pd.DataFrame(mySet)
# print(myVar)

#Index - mozemo da procitamo kao dict, Series predstavlja kolone
# listOfElements = {"name": "milos", "years": 21, "city": "Belgrade"}
# a = pd.Series(listOfElements)
# print(a["name"])

#data frejm predstavlja tabelu
# data = {
#     "years": [1990, 1995, 1971],
#     "language": ["python","java","C"]
# }
# myData = pd.DataFrame(data)
# print(myData)

# pomocu loc mozemo da izvucemo jednu ili vise informacija iz data frejma
# data = {
#     "calories": [420, 320, 490],
#     "duroton": [50, 40, 30]
# }
# df = pd.DataFrame(data, index = ["day1", "day2", "day3"])

# print(df.loc[["day1", "day2"]])


# load CSV file
# pd.options.display.max_rows = 500
# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/src/nike_2020_04_13.csv")
# print(df)

# read json
# df = pd.read_json("myJson.json")
# print(df)

# load dict to DataFrame
# data = {
#   "Duration":{
#     "0":60,
#     "1":60,
#     "2":60,
#     "3":45,
#     "4":45,
#     "5":60
#   },
#   "Pulse":{
#     "0":110,
#     "1":117,
#     "2":103,
#     "3":109,
#     "4":117,
#     "5":102
#   },
#   "Maxpulse":{
#     "0":130,
#     "1":145,
#     "2":135,
#     "3":175,
#     "4":148,
#     "5":127
#   },
#   "Calories":{
#     "0":409,
#     "1":479,
#     "2":340,
#     "3":282,
#     "4":406,
#     "5":300
#   }
# }
# df= pd.DataFrame(data)
# print(df)

# head method
# pd.options.display.max_rows = 500
# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/src/nike_2020_04_13.csv")
# # print(df.head(10)) # vraca prvih 5 redova 
# # print(df.tail()) # vraca zadnjih 5 redova
# print(df.info())    #daje informacije o tabeli, tipu podatka, kolone i memorije koju zauzima

#Clean Data

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# # df.dropna(inplace=True)
# df["Date"].fillna("2022/12/1", inplace=True)
# print(df.to_string())

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# x = df["Calories"].mean() #zbirs prosecne vrednosti 
# x = df["Calories"].median() #srednja vrednost nakon sortiranja ka visem
# x = df["Calories"].mode()[0]    #vrednost koja se najcesce ponavlja
# df["Calories"].fillna(x, inplace=True)
# print(df.to_string())

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# df["Date"] = pd.to_datetime(df["Date"]) #konvertuj row date u tip dateTime
# df.dropna(subset=['Date'], inplace=True)    #izbaci nan vrednost
# print(df.to_string())

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# #df.loc[7, "Duration"] = 45
# # for x in df.index:  # loop-ujemo vrdonst i ako je vrdniost veca od 120 setujemo je na 120
# #     if df.loc[x, "Duration"] >120:
# #         df.loc[x, "Duration"] = 120
# #         print(df.to_string())

# for x in df.index:  #brisemo vrednost ako je veca od 120
#     if df.loc[x, "Duration"] > 120:
#         df.drop(x, inplace=True)
#         print(df.to_string())

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# df.drop_duplicates(inplace=True)    # izbaci sve duplikate
# print(df.duplicated())  #provera da li postoji duplikat

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# print(df.corr())    #pronalazenje relacija vise o znacenju vrednosti https://www.w3schools.com/python/pandas/pandas_correlations.asp

# df = pd.read_csv("/home/milos/Desktop/Elasticsearch/dirtydata.csv")
# df.plot()     #vizuelizacija podataka
# plt.show()
# plt.savefig(sys.stdout.buffer)
# sys.stdout.flush()
