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

    images.append((query, image_url))

with open("assets\image_urls.txt", "wt") as output_file:
    for image in images:
        output_file.write(f"{image[0]}\n{image[1]}\n\n")

print("Opening browser...")
webbrowser.open("web-ui\index.html")