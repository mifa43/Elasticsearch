import requests
import pandas as pad
import csv
#docker build -t foo .

# head = ["ime", "prezime" , "godine", "grad", "drzava"]
# data = ["Milos", "Zlatkovic", "21", "Beograd", "Rebublika Srbija"]

# with open("/home/milos/Desktop/Elasticsearch/job/src/korisnik.csv", "w") as file:
#     writer = csv.writer(file)
#     writer.writerow(head)
#     writer.writerow(data)
#     file.close()


def send_request():
    df = pad.read_csv("korisnik.csv")
    l = []
    
    for i in range(len(df["ime"])):
        print(df["ime"][i])
        l.append({
        "ime":f"{df['ime'][i]}",
        "prezime":f"{df['prezime'][i]}",
        "godine":f"{df['godine'][i]}",
        "grad":f"{df['grad'][i]}",
        "drzava":f"{df['drzava'][i]}"
        
        })
    print(l)
    url = 'http://fastapi-es:8080/create-document-bulk-job'
    data = {"indices": "2", "document": l}
    requests.post(url, json = data)
send_request()