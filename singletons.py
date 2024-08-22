import discord
import items
import saveload
import datetime
# Discord Essential variables

start_time = datetime.datetime.now() # Start time of the bot

class Client(discord.Client):
    async def Save(self):
        # Save accounts before closing
        saveload.SaveUserDict()
        print("Saved!")

    async def close(self):
        # Perform cleanup before closing
        await self.Save()
        
        # Call the parent class's close method
        await super().close()



intents =  discord.Intents.all()
client = Client(intents=intents)

# Market Item Costs
INSULT_BAG_COST = 150.0
COMPLEMENT_BAG_COST = 300.0

ENERGY_DRINK_COST = 350.0
COFFEE_COST = 100.0

ADDERAL_COST = 600.0

# Market
market = [
    items.ComplementBag(quantity=1),
    items.Coffee(quantity=1),
    items.EnergyDrink(quantity=1),
]

market_pages = [
    [], # Page 0
]

# Black Market
black_market = [
    items.InsultBag(quantity=1),
    items.Adderall(quantity=1),
]

black_market_pages = [
    [], # Page 0
]

user_dict = {} # 1067541126518677664: serverid, list[econessentials.User]
