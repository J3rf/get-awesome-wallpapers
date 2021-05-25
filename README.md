# Awesome Wallpaper Getter
<img align="right" width="200" height="200" src="https://pbs.twimg.com/profile_images/1387861394012311553/6o9rYvdJ.jpg">

very cool application for getting wallpaper from twitter user [**Awesome Wallpapers**](https://twitter.com/awesomepapers).

written in python with my ape brain

also only works on windows because i'm very smart
## Requirements
- **Tweepy**
```console
pip install tweepy
```
- **ConfigParser**
```console
pip install configparser
```
- **tqdm**
```console
pip install tqdm
```
- **Requests**
```console
pip install requests
```
- **The Config file... i guess?**

This is ignored in the git repository. It's auto-generated when the program is run, but requires your own **API Keys** from a twitter app. If you don't have an app, you can make one at [**Twitter Application Management**](https://apps.twitter.com/).
## Building
To build the executable, I used **PyInstaller**.
```console
pip install pyinstaller

pyinstaller --noconsole --icon=icon.ico getawesomewallpaper.py -F
```