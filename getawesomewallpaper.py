import tweepy, random, requests, ctypes, os, configparser, sys, json
from tqdm import tqdm
config = configparser.RawConfigParser()
try:
    config.read('config.ini')
    configvars = dict(config.items('API Keys'))
    accessToken = str(configvars['access-token'])
    accessTokenSecret = str(configvars['access-token-secret'])
    consumerKey = str(configvars['api-key'])
    consumerKeySecret = str(configvars['api-secret-key'])
except:
    with open('config.ini', 'w') as f: 
        defaultConfig = "; Place your consumer key/secret and access token/secret here. "\
        "If you need them, visit https://developer.twitter.com/en/portal/projects-and-apps"\
        "\n[API Keys]"\
        "\napi-key="\
        "\napi-secret-key="\
        "\naccess-token="\
        "\naccess-token-secret="\
        "\n[Settings]"\
        "\n; Get latest wallpaper only (yes/no)"\
        "\nget-latest=no"\
        "\n; Reuse previously used wallpapers (yes/no)"\
        "\nreuse-wallpapers=yes"
        f.write(defaultConfig)
try:
    getLatest = config['Settings'].getboolean('get-latest')
except:
    getLatest = False

try:
    reuseWallpapers = config['Settings'].getboolean('reuse-wallpapers')

except:
    reuseWallpapers = False
try:
    with open('used-wallpapers.json', 'r') as f:
        usedWallpapers = json.load(f)
except:
    usedWallpapers = []

def get_timeline():
    try:
        auth = tweepy.OAuthHandler(consumerKey, consumerKeySecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        tweets = api.user_timeline("awesomepapers", count = 200, exclude_replies = True)
        return tweets
    except:
        ctypes.windll.user32.MessageBoxW(0, "API Key Not Found or Expired. Please check your config.ini file", "API Key Error", 0x0 | 0x10)
        sys.exit()
tweets = get_timeline()
print(f"Found {len(tweets)} awesome wallpapers")
i = 0
while True:
    if i == len(tweets):
        print("Couldn't find new image, exiting...")
        sys.exit()
    if getLatest:
        index = 0
    else:
        index = random.randint(0, len(tweets) - 1)
    tweet = tweets[index]
    media = tweets[index].entities['media']
    image = media[0]['media_url']
    if not reuseWallpapers and image in usedWallpapers:
        print("Already used that one! Finding another")
        i += 1
    else:
        break
print(f"Selected image: {image}")
print("Requesting image...")
response = requests.get(image, stream=True)
response_size = int(response.headers.get('content-length', 0))
progressbar = tqdm(total=response_size, unit='iB', unit_scale=True)
with open("background.png", "wb") as f: 
    for data in response.iter_content(1024):
        progressbar.update(len(data))
        f.write(data)
progressbar.close()
if response_size != 0 and progressbar.n != response_size:
    print("ERROR, something went wrong")
    sys.exit()
else:
    print("Downloaded Image")
ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{os.getcwd()}/background.png", 0)
if not reuseWallpapers:
    usedWallpapers.append(image)
    with open('used-wallpapers.json', 'w') as f:
        output = json.dumps(usedWallpapers)
        f.write(output)
print("Successfully set image as wallpaper\nok bye lmao")