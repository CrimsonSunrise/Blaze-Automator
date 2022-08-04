# A software to automate Blaze Double operations

<a href="https://www.buymeacoffee.com/crimsonsunrise" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png"/></a>

This project uses Selenium as the browser automation library. Don't forget to install it before using ```pip install selenium```.

We're using Chrome Webdriver as the browser but you can use whatever driver you want, just change the code.

## :warning: Disclaimer

#### BETTING OFTEN USES REAL MONEY AND ITS ALWAYS A RISK TO BET WITH OR WITHOUT PROPER KNOWLEDGE. THIS REPOSITORY AND PEOPLE LINKED TO IT ARE NOT RESPONSIBLE FOR ANY POSSIBLE LOSSES THAT MAY OCCUR. USE THIS SOFTWARE AND/OR THE INFORMATION AT YOUR OWN RISK.

## How to use it?

First, import our bot from the ```Automation.py``` script and instantiate our ```Bot``` class:

```python
from Automation import Bot
bot = Bot()
```

Now we have access to the methods that we will need.

### Start

The first method is the ```Start``` method. It is responsible to instantiate our browser and load the ```BASE_URL```.

```python
bot.Start(headless=False)
```

We can set the browser to be headless or not with the ```headless``` parameter.

### Login

After starting up, we can now use the method ```Login``` to start a new session with our Blaze credentials. This method returns an array with the first value being ```success``` and the second being the ```reason``` if success is False.

```python
success, reason = bot.Login("YOUR BLAZE EMAIL", "YOUR BLAZE PASSWORD")

if success:
    print("Yay")
else:
    print(reason)
```

### Get_Balance

Now that we successfully loged in, we can check our balance with the method ```Get_Balance()``` that returns an array with 2 values, the first is the real balance and the second is the bonus balance.

```python
real, bonus = bot.Get_Balance()

print(real, bonus)
```

### Bet

The next is the ```Bet``` method and it has 2 parameters.

The first parameter is an array with the bets being objects with the following format:

```python
bet1 = {
    "color": "red",
    "amount": 2
}

bet2 = {
    "color": "black",
    "amount": 2
}
```
    
The second parameter is a boolean to chose if you want the method to return the result of the bet or not.

So now we can call our method.

```python
bot.Bet(bets=[bet1, bet2], return_results=True)
```

Once called, the method will imediatelly check if the bet window is open. If it is, will bet on the selected options right away, if not it will wait for the next bet window.

If ```return_results``` is set to True, after placing the bets, it will wait for the complete rolling status and will compare the bets with the result and then will return an array with 2 items, the first item being the total profit for the bets and the second being the bet array with respective results.

### Stop

Last but not least its the ```Stop``` method. When called it close our browser window and finish our chromedrive instance.

```python
bot.Stop()
```