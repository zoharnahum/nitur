import urllib.parse
import webbrowser
pic = input("input pic")
url = f"https://www.google.com/search?q={pic}&tbm=isch"
webbrowser.open(url)
