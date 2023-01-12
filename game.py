import requests, webbrowser, random

while True:
    print("Openning new artwork...")

    has_styles = False
    while has_styles == False:
        pagenum = random.randint(0, 100)
        entrynum = random.randint(0, 9)
        query_result = requests.get("https://api.artic.edu/api/v1/artworks/search", params = {"q": "painting", "page": str(pagenum)})
        query_result = dict(query_result.json())
        single_query = query_result["data"][entrynum]["api_link"]
        artwork = requests.get(single_query)
        artwork = dict(artwork.json())

        artwork = artwork["data"]
        image_id = artwork["image_id"]
        base_url = query_result["config"]["iiif_url"]

        styles = artwork["style_titles"]
        
        if list(styles).__len__() > 0:
            has_styles = True

    webbrowser.open(base_url + "/" + image_id + "/full/843,/0/default.jpg", 2)
    style_guess = input("What artistic movement/style is this a part of? ")

    correct = False
    for style in styles:
        if style_guess.lower() == str(style).lower():
            correct = True

    if correct == True:
        print("Correct! You got it!")
    else:
        print("Incorrect. This painting is classified as " + artwork["style_title"])
    if artwork["artist_title"] is None:
        print("This is " + artwork["title"] + " by unknown")
    else:
        print("This is " + artwork["title"] + " by " + artwork["artist_title"])