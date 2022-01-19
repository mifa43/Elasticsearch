from http.client import responses
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

# def send_request_document_bulk() -> str:
#     """
#     Definicija koja cita csv fajl i salje request na api gde se upisuje u elastic
#     """
#     df = pad.read_csv("/korisnik.csv")
#     l = []
    
#     for i in range(len(df["ime"])):
#         print(df["ime"][i])
#         l.append({
#         "ime":f"{df['ime'][i]}",
#         "prezime":f"{df['prezime'][i]}",
#         "godine":f"{df['godine'][i]}",
#         "grad":f"{df['grad'][i]}",
#         "drzava":f"{df['drzava'][i]}"
        
#         })
#     print(l)
#     url = 'http://fastapi-es:8080/create-document-bulk-job'
#     data = {"indices": "2", "document": l}
#     requests.post(url, json = data)
#send_request_document_bulk()

def send_request_helpers_bulk() -> str:
    """
    Definicija koja cita csv fajl i salje request na api gde se upisuje u elastic bulk helpers
    """
    df = pad.read_csv("nike_2020_04_13.csv")
    l = []
    
    for i in range(len(df["Product Name"])):
        print(df["Product Name"][i])
        l.append({
        "URL":f"{df['URL'][i]}",
        "Product Name":f"{df['Product Name'][i]}",
        "Product ID":f"{df['Product ID'][i]}",
        "Listing Price":f"{df['Listing Price'][i]}",
        "Sale Price":f"{df['Sale Price'][i]}",
        "Discount":f"{df['Discount'][i]}",
        "Brand":f"{df['Brand'][i]}",
        "Description":f"{df['Description'][i]}",
        "Rating":f"{df['Rating'][i]}",
        "Reviews":f"{df['Reviews'][i]}",
        "Images":f"{df['Images'][i]}",
        "Last Visited":f"{df['Last Visited'][i]}",
        
        })
    print(l)
    url = 'http://fastapi-es:8080/bulk'
    data = {"indices": "products", "document": l}
    requests.post(url, json = data)
#send_request_helpers_bulk()
if __name__ == "__main__":
    send_request_helpers_bulk()
#URL,Product Name,Product ID,Listing Price,Sale Price,Discount,Brand,Description,Rating,Reviews,Images,Last Visited