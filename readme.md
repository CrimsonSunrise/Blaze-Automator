# A software to automate Blaze bets

A :star: is much appreciated! 🥰

<a href="https://www.buymeacoffee.com/crimsonsunrise" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png"/></a>

## Requirements:

```Python 3.7 or above```

```Selenium```

We're using Chrome Webdriver as the browser, which can be found and downloaded at [this page](https://chromedriver.chromium.org/downloads). Download the same version you're using within your installed Chrome browser and place it in the same folder as the `main.py` file.

## :warning: Disclaimer

#### BETTING OFTEN USES REAL MONEY AND ITS ALWAYS A RISK TO BET WITH OR WITHOUT PROPER KNOWLEDGE. THIS REPOSITORY AND PEOPLE LINKED TO IT ARE NOT RESPONSIBLE FOR ANY POSSIBLE LOSSES THAT MAY OCCUR. USE THIS SOFTWARE AND/OR THE INFORMATION AT YOUR OWN RISK.

## Table of content

* [How to use it?](#how-to)
    * [Start](#start)
    * [Login](#login)
    * [Get Balance](#get-balance)
    * [Bet](#bet)
    * [Stop](#stop)
* [Contribute](#contribute)

<a name="how-to"></a>
## How to use it?

First, import our bot from the ```Automation.py``` script and instantiate our ```Bot``` class:

```python
from Automation import Bot
bot = Bot()
```

Now we have access to the methods that we will need.

<a name="start"></a>
### Start

The first method is the ```Start``` method. It is responsible to instantiate our browser and load the ```BASE_URL```.

```python
bot.Start()
```

<!-- We can set the browser to be headless or not with the ```headless``` parameter. -->

<a name="login"></a>
### Login

After starting up, we can now use the method ```Login``` to start a new session with our Blaze credentials. This method returns an array with the first value being ```success``` and the second being the ```reason``` if success is False.

```python
success, reason = bot.Login("YOUR BLAZE EMAIL", "YOUR BLAZE PASSWORD")

if success:
    print("Yay")
else:
    print(reason)
```

<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: #8a6d3b;; background-color: #fcf8e3; border-color: #faebcc;">
<b>IMPORTANT!</b><br/>
After the browser opens and automatically fill the login form with your information, a <b>Captcha</b> will be shown for you to solve. The algorithm will only proccees after solving the <b>Captcha</b>.
</div>

<a name="get-balance"></a>
### Get_Balance

Now that we successfully loged in, we can check our balance with the method ```Get_Balance()``` that returns an array with 2 values, the first is the real balance and the second is the bonus balance.

```python
real, bonus = bot.Get_Balance()

print(real, bonus)
```

<a name="bet"></a>
### Bet

The next is the ```Bet``` method and it has 3 parameters.

```python
bot.Bet(game="double/crash", bets=["array of bets"], return_results=True/False)
```

• The first parameter is the game mode, being `double` or `crash`.

• The second parameter is an array of bets. Each bet should be formated as below.

• The third parameter is a boolean which defines if the result of the bet will be returned.



#### • Double


```python
# Colors: red, black, white

bet1 = {
    "color": "red",
    "amount": 1.7
}

bet2 = {
    "color": "white",
    "amount": 1.7
}

bot.Bet(game="double", bets=[bet1, bet2], return_results=True)
```

#### • Crash

```python
# Always set autoCashout over 1.01, otherwise you will always lose.

bet1 = {
    "autoCashout": 1.01,
    "amount": 1.7
}

# Bet function for crash receive only 1 bet as argument.
bot.Bet(game="crash", bet=bet1, return_results=True)
```

Once called, the method will imediatelly check if the bet window is open. If it is, will bet with the selected options right away, if not it will wait for the next bet window.

If ```return_results``` is set to True, after placing the bets, it will wait for the complete rolling status and will compare the bets with the result and then will return an array with 2 items, the first item being the total profit for the bets and the second being the bet array with respective results.

<a name="stop"></a>
### Stop

Last but not least its the ```Stop``` method. When called it close our browser window and finish our chromedrive instance.

```python
bot.Stop()
```

<a name="contribute"></a>
## Contribute

This is a hobby project so bugs might occur during testing or production. If you found any bugs or have any suggestion on how to improve it or any questions, feel free to open an issue, I'll be more than happy to hear from you.

If you like to add your own features to it, feel free to fork and open a pull request.