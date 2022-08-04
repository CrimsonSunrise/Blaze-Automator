balance_description = "Saldo Atual: R$185.8403 BRL(R$185.84 + R$0 Dinheiro de Bônus)"

currency = None
symbol = None

if "R$" in balance_description:
    currency = "BRL"
    symbol = "R$"
elif "$" in balance_description:
    currency = "USD"
    symbol = "$"
elif "€" in balance_description:
    currency = "EUR"
    symbol = "€"

balance = balance_description.split("(")[1].replace(")", "").replace(symbol, "")
real = float(balance.split("+")[0].strip())
bonus = float(balance.split("+")[1].strip().split(" ")[0])
print([real, bonus])