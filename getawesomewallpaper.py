import tweepy, random, requests, ctypes, os, configparser, sys
try:
    config = configparser.RawConfigParser()
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
        "\naccess-token-secret="
        f.write(defaultConfig)
try:
    auth = tweepy.OAuthHandler(consumerKey, consumerKeySecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
    tweets = api.user_timeline("awesomepapers", count = 200, exclude_replies = True)
except:
    ctypes.windll.user32.MessageBoxW(0, "API Key Not Found or Expired. Please check your config.ini file", "API Key Error", 0x0 | 0x10)
    sys.exit()
print("Found a buncha awesome wallpapers")
index = random.randint(0, len(tweets) - 1)
print(len(tweets))
tweet = tweets[index]
media = tweets[index].entities['media']
image = media[0]['media_url']
print(f"Selected image: {image}")
response = requests.get(image)
with open("background.png", "wb") as f: f.write(response.content)
print(f"Image Downloaded")
ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{os.getcwd()}/background.png", 0)
print("Successfully set image as wallpaper\nok bye lmao")