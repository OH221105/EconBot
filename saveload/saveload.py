import os
import singletons
import math
import constants
import pickle
import threading
import time
import asyncio

loaded = False
save_task : asyncio.Task

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the save file
save_path = os.path.join(script_dir, 'userdata.pkl')

print(save_path)

async def timed_save(interval):
    while True:
        await asyncio.sleep(interval)
        print("Auto-Saving...")
        await SaveUserDict()

# Start the timed save in a separate thread

async def initiate_save():
    global save_task
    print("Initiating timed save..")
    save_task = asyncio.create_task(timed_save(constants.SAVE_INTERVAL))


def LoadAll() -> bool:
    global loaded
    """Loads all data from files."""
    if not LoadUserDict():
        return False
    if not LoadMarketPages():
        return False
    if not LoadBlackMarketPages():
        return False
    loaded = True
    return True


async def SaveUserDict() -> None:
    try:
        with open(save_path, 'wb') as file:
            pickle.dump(singletons.user_dict, file=file)
            print("--- Saved Userdata Successfully ---")
    except Exception as err:
        print(f"Error: {err}")

def LoadUserDict() -> bool:
    if not os.path.exists(save_path):
        os.mknod(save_path)
    with open(save_path,'rb') as file:
       singletons.user_dict = pickle.load(file=file)
       return True

def LoadMarketPages() -> bool:
    """Loads market item list into market pages."""
    print(f"Loading market ...")
    pages = math.ceil(len(singletons.market) / constants.PAGE_LEN)
    for i in range(pages):
        for j in range(constants.PAGE_LEN):
            try:
                singletons.market_pages[i].append(singletons.market[(constants.PAGE_LEN*i)+j])
            except IndexError:
                return True
            except Exception as e:
                print(e,singletons.market_pages[i])
                return False
        singletons.market_pages.append([]) # Adds new empty page list
    else:
        if singletons.market_pages[-1] == []:
            singletons.market_pages[-1].remove()
        return True
    
def LoadBlackMarketPages() -> bool:
    """Loads blackmarket item list into blackmarket pages."""
    print(f"Loading blackmarket ...")
    pages = math.ceil(len(singletons.black_market) / constants.PAGE_LEN)
    for i in range(pages):
        for j in range(constants.PAGE_LEN):
            try:
                singletons.black_market_pages[i].append(singletons.black_market[(constants.PAGE_LEN*i)+j])
            except IndexError:
                return True
            except Exception as e:
                print(e,singletons.black_market_pages[i])
                return False
        singletons.black_market_pages.append([]) # Adds new empty page list
    else:
        if singletons.black_market_pages[-1] == []:
            singletons.black_market_pages[-1].remove()
        return True
    

# def SaveUserDict() -> bool:
#     try:
#         data = {}
#         for server_id, user_list in singletons.user_dict.items():
#             data[str(server_id)] = []
#             for user in user_list:
#                 user_data = {
#                     "uid": user.uid,
#                     "bank_acc": {
#                         "cash_on_hand": user.bank_acc.GetCashOnHand(),
#                         "deposit": user.bank_acc.GetDeposit()
#                     },
#                     "inventory": []
#                 }
#                 for page in user.inventory:
#                     page_data = []
#                     for item in page:
#                         item_data = {
#                             "name": item.GetName(),
#                             "quantity": item.GetQuantity(),
#                             "cost": item.GetCost()
#                         }
#                         page_data.append(item_data)
#                     user_data["inventory"].append(page_data)
#                 data[str(server_id)].append(user_data)
        
#         with open("user_data.json", "w") as f:
#             json.dump(data, f, indent=4)
#         return True
#     except Exception as e:
#         print(f"Error saving user data: {e}")
#         return False


# def LoadUserDict() -> bool:
#     try:
#         if not os.path.exists("user_data.json"):
#             return False

#         with open("user_data.json", "r") as f:
#             data = json.load(f)

#         singletons.user_dict.clear()
#         for server_id, user_list in data.items():
#             singletons.user_dict[int(server_id)] = []
#             for user_data in user_list:
#                 user = econessentials.User(uid=user_data["uid"])
#                 user.bank_acc.SetCashOnHand(user_data["bank_acc"]["cash_on_hand"])
#                 user.bank_acc.SetDeposit(user_data["bank_acc"]["deposit"])
                
#                 user.inventory = []
#                 for page in user_data["inventory"]:
#                     inventory_page = []
#                     for item_data in page:
#                         if item_data["name"] == "Insult Bag":
#                             item = items.InsultBag(quantity=item_data["quantity"])
#                         elif item_data["name"] == "Complement Bag":
#                             item = items.ComplementBag(quantity=item_data["quantity"])
#                         else:
#                             continue
#                         item.SetCost(item_data["cost"])
#                         inventory_page.append(item)
#                     user.inventory.append(inventory_page)
                
#                 singletons.user_dict[int(server_id)].append(user)
        
#         return True
#     except Exception as e:
#         print(f"Error loading user data: {e}")
#         return False