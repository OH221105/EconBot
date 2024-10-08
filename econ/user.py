from econ import bank, energy, attribute, jobs
from econ.jobs import job, jobs
from econ.items import item

class User:
    uid : int # Unique ID of the user.
    op :  bool # Is the user an operator?

    bank_acc : bank.BankAccount
    occupation : job.Job
    networth : float
    attributes : dict[str, attribute.Attribute]
    energy : energy.EnergyBar

    inventory : list

    def __init__(self, uid) -> None:
        self.inventory = [[]]
        self.uid = uid
        self.op = False
        self.bank_acc = bank.BankAccount()
        #self.occupation = jobs.jobs["economist"] 
        self.occupation = job.Job(name="Unemployed", description="Loser", requirements={})
        self.energy = energy.EnergyBar(max_energy=10, current_energy=10)
        self.networth = 0.0
        self.attributes = {
        "Strength" : attribute.Attribute(level=10.0),
        "Dexterity" : attribute.Attribute(level=5.0),
        "Intelligence" : attribute.Attribute(level=10.0),
        "Charisma" : attribute.Attribute(level=10.0),
        "Creativity" : attribute.Attribute(level=10.0),
        "Employability" : attribute.Attribute(level=5.0),
        }
    
    def AddNewItemInventory(self, item) -> None:
        from constants import PAGE_LEN
        """Adds a new item to the inventory."""
        if len(self.inventory[-1]) == PAGE_LEN:
            self.inventory.append([item])
        else:
            self.inventory[-1].append(item)

    def UpdateNetWorth(self) -> None:
        """Updates and sets the networth of the user."""
        networth = self.bank_acc.GetCashOnHand() + self.bank_acc.GetDeposit()
        for page in self.inventory:
            for item in page:
                networth += item.GetCost() * item.GetQuantity()
        self.SetNetWorth(networth=networth)
    
    def GetIncome(self) -> float:
        """Returns the income of the user."""
        return self.occupation.GetHourlyPay()

    def GetNetWorth(self) -> float:
        self.UpdateNetWorth()
        return self.networth
    
    def SetNetWorth(self, networth : float) -> None:
        self.networth = networth
    
    def __str__(self) -> str:
        return f"UID: {self.uid}\nBank Account: {self.bank_acc}\nEnergy: {self.energy}\nAttributes: {self.attributes}\nNetworth: {self.networth}"
        