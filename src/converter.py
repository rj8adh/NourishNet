import requests

def get_product_name(upc):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["title"]
        else:
            return "Product not found"
    else:
        return "Error fetching product"
    
upc_code = input("UPC Code: ")
print("UPC code: " + get_product_name(upc_code))