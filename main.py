from Automation import Bot

Bot.Start(detach=True, headless=False)

login, reason = Bot.Login(email="YOUR BLAZE EMAIL", password="YOUR BLAZE PASSWORD")

if login == True:
    
    print(Bot.Get_Balance())

    # Bot.Bet(bets=[("black", 2)], return_results=True)
else:
    print(reason)


Bot.Stop()