# Skyroom Bot
Bot for keeping you online in [skyroom.online](https://www.skyroom.online/) (online classroom)

## Setup
Clone repo and download dependencies:
```shell
git clone https://github.com/Arian8j2/SkyroomBot.git
cd SkyroomBot
pip install -r requirements.txt
```

## How to use
Run `skyroom_bot.py` for command line interface:
```shell
python skyroom_bot.py
```

or `gui.py` for graphical interface
```shell
python gui.py
```
(Thanks to [mparsabadri](https://github.com/mparsabadri/) for helping with gui)

It asks for credentials to login, There are multiple ways to loin to class and you can say it by looking at url, e.g if url is like `https://www.skyroom.online/ch/madresegholam/shimi` you just pass **url**, **username**, **password** to bot and you are good to go.

But some urls are like `https://www.skyroom.online/ch/madresegholam/shimi/t/eyJ0eXAiOiJKV1QiL.../` in this case you enter **url** just like previous way, and then enter nothing for **username** and **password** and then enter **token** that here is `eyJ0eXAiOiJKV1QiL...` (that is very longer in real url).

### License
Feel free to create your own script using Skyroom Bot. Enjoy!