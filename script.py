import requests, webbrowser

style = input("Enter an artistic movement: ")
print("Searching...")

query_result = requests.get("https://api.artic.edu/api/v1/artworks/search", params = {"q": style})
query_result = dict(query_result.json())    #Convert JSON from request into a workable dictionary (Python version of hashmap)

HTML_DOCSTRING = "<!DOCTYPE html><body>"
if "data" in query_result.keys() and len(query_result["data"]) > 0:
    for query in query_result["data"]:
        image_query_url = f"https://api.artic.edu/api/v1/artworks/{query['id']}?fields=id,title,image_id,artist_title"
        image_query = requests.get(image_query_url)
        image_query = dict(image_query.json())
        image_url = f"{image_query['config']['iiif_url']}/{image_query['data']['image_id']}/full/843,/0/default.jpg"

        HTML_DOCSTRING += f"<div><p>Artwork Title: {image_query['data']['title']}</p><p>Artist: {image_query['data']['artist_title']}</p>"
        HTML_DOCSTRING += f"<img src={image_url} width=200 height=200 /><br>"
else:
    HTML_DOCSTRING += "<h1>No Artworks Found</h1>"

HTML_DOCSTRING += "</body>"
with open("index.html", "wt") as output_file:
    output_file.write(HTML_DOCSTRING)


print("Displaying result...")
webbrowser.open("index.html")
