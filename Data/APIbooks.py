import requests

# link1 = "https://freetestapi.com/api/v1/books"
#
# response = requests.get(link1)
# content = response.json()
#
# print(content)

api_key ="AIzaSyD5j3Enl0Hr_Ar7wlchSIGMMS3XucIwtcs"


def search_books(query, api_key):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage

books = ["programming","cook","cosmic","league of legend","video games","anime","sport","medical"]
for book in books:
    result = search_books(book, api_key)

    if result:
        for item in result.get("items", []):
            print(f"Title: {item['volumeInfo'].get('title','authors')}")
            print(f"authors: {item['volumeInfo'].get('authors')}")
