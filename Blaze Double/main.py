from Automation import Bot

bot = Bot()

# bot.Start(False)
bot.Start()

login, reason = bot.Login(email="YOUR BLAZE EMAIL", password="YOUR BLAZE PASSWORD")

if login == True:
    
    print(bot.Get_Balance())
    
    # Uncomment to perform a bet
    # doubleBet = bot.Bet(game="double", bets=[{ "color": "red", "amount": 1.7 }], return_results=True)
    # print(doubleBet)
    
    # crashBet = bot.Bet(game="crash", bets=[{"autoCashout": 1.1, "amount": 1.7}], return_results=True)
    # print(crashBet)
else:
    print(reason)


bot.Stop()