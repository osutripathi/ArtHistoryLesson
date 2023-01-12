import json, random, requests, webbrowser


#Prints a clean-looking progress bar in the terminal
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


#Load in different movements and the respective number of artworks associated with them
with open("assets\queries.json") as query_file:
    queries = json.load(query_file)
selected_queries = [random.choice(list(queries.keys())) for q in range(10)]


print("Loading different artworks...")
images = []
for query in progressBar(selected_queries, prefix = "Progress", suffix = "Complete", length = 50):
    query_result = requests.get("https://api.artic.edu/api/v1/artworks/search", params = {"q": query, "page": random.randint(1, queries[query])})
    query_result = dict(query_result.json())    #Convert JSON from request into a workable dictionary (Python version of hashmap)

    image_id = query_result["data"][random.randint(0, len(query_result["data"]) - 1)]["id"]
    image_query_url = f"https://api.artic.edu/api/v1/artworks/{image_id}?fields=id,title,image_id,artist_title"
    image_query = dict(requests.get(image_query_url).json())
    image_url = f"{image_query['config']['iiif_url']}/{image_query['data']['image_id']}/full/843,/0/default.jpg"

    images.append((query, image_query["data"]["title"], image_query["data"]["artist_title"], image_url))


with open("web-ui\index1.html", "rt") as input_file:
    html_prefix = input_file.readlines()
with open("web-ui\index2.html", "rt") as input_file:
    html_suffix = input_file.readlines()
with open("index.html", "wt") as output_file:
    for line in html_prefix:
        output_file.write(line)
    output_file.write("\n")
    for image in images:
        html_docstring = f"<div class='slideshow-images' artMovement='{image[0]}' "
        art_title = image[1].replace("'", '"')
        html_docstring += f"artTitle='{art_title}' "
        html_docstring += f'artist="{image[2]}">'
        html_docstring += f"<img src='{image[3]}'></div>"
        output_file.write(html_docstring + "\n")
    for line in html_suffix:
        output_file.write(line)


print("Opening browser...")
webbrowser.open("index.html")