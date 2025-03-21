import urllib.parse

# Encode the username and password
username = "charbelrabbat"
password = "CHra@119900"

encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Construct the MongoDB URI with encoded username and password
mongodb_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@clusterfastapi.0xb6k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFastapi"

# Print the encoded URI
print(mongodb_uri)
