from Automation import Bot

bot = Bot()

bot.Start(headless=False)

login, reason = bot.Login(email="YOUR BLAZE EMAIL", password="YOUR BLAZE PASSWORD")

if login == True:
    
    print(bot.Get_Balance())
    
    # Uncomment to perform a bet
    # bot.Bet(bets=[{"color": "white", "amount": 2}], return_results=True)
else:
    print(reason)


bot.Stop()