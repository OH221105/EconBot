# Libraries
import discord
import os

import singletons
import constants
import utils

from saveload import saveload
from econ.jobs import listings

import commands

import startup

from commands import bank, earnings, inventory, display, training, apply, operator, gambling
from commands.display import balance, markets, inventory, clock, energy, help, profile, jobs, leaderboard, changelog
from commands.operator import permissions, management, cheats
from commands.earnings import work, crime, rob, beg
from commands.operator.cheats import money
from commands.gambling import slots, blackjack, roulette
from commands.gambling.blackjack import blackjack

# Client Event Functions
@singletons.client.event
async def on_ready():

    await startup.StartUp()

@singletons.client.event
async def on_message(message : discord.Message):

    if message.author.id == singletons.client.user.id: # This ignores bot's own messages.
        return

    if len(message.content) == 0: # This ignores any gif or image messages.
        return

    if message.content[0] == constants.PREFIX:
        await InvokeEcon(message=message)

async def InvokeEcon(message : discord.Message) -> None:
    """The Root Function of User-bot Interaction."""
    #await message.reply("Invoked Me!") # Uncomment when debugging.

    command = utils.GetCommand(message=message.content)
    action = command[0].lower()
    command = utils.StripEmpty(_list=command)

    match action:
        case "help":
            await commands.display.help.Help(message=message, command=command)
        case "profile":
            await commands.display.profile.DisplayProfile(message=message, command=command)
        case "prof":
            await commands.display.profile.DisplayProfile(message=message, command=command)
        case "leaderboard":
            await commands.display.leaderboard.DisplayLeaderboard(message=message)
        case "lb":
            await commands.display.leaderboard.DisplayLeaderboard(message=message)
        
        # Bank Commands
        case "balance":
            await commands.display.balance.DisplayBalance(message=message, command=command)
        case "bal":
            await commands.display.balance.DisplayBalance(message=message, command=command)
        case "withdraw":
            await commands.bank.Withdraw(message=message, command=command)
        case "with":
            await commands.bank.Withdraw(message=message, command=command)
        case "deposit":
            await commands.bank.Deposit(message=message, command=command)
        case "dep":
            await commands.bank.Deposit(message=message, command=command)
        case "pay":
            await commands.bank.Pay(message=message, command=command)
            
        # Earnings commands
        case "work":
            if constants.ENABLE_JOBS and constants.ENABLE_UNEMPLOYED_WORK:
                await commands.earnings.work.Work(message=message)
                
            elif constants.ENABLE_JOBS and not constants.ENABLE_UNEMPLOYED_WORK:
                await commands.earnings.work.JobOnlyWork(message=message)
            
            elif not constants.ENABLE_JOBS and constants.ENABLE_UNEMPLOYED_WORK:
                await commands.earnings.work.WorkNoJob(message=message)
            else:
                await utils.ReplyWithException(message=message, exception_msg="Conflicting setting! Notify Bot operator.", exception_desc="Jobs and Unemployed work are **both** disabled.")
        
        case "crime":
            if not constants.ENABLE_CRIME:
                return
            await commands.earnings.crime.Crime(message=message)
        case "beg":
            if not constants.ENABLE_BEG:
                return
            await commands.earnings.beg.Beg(message=message)
        case "rob":
            if not constants.ENABLE_ROB:
                return
            await commands.earnings.rob.Rob(message=message, command=command)
        
        # Training commands
        case "workout":
            await commands.training.Workout(message=message)
        case "excercise":
            await commands.training.Workout(message=message)
        case "study":
            await commands.training.Study(message=message)
        case "paint":
            await commands.training.Paint(message=message)
        case "socialize":
            await commands.training.Socialize(message=message)
        

        case "shop":
            await commands.display.markets.DisplayMarket(message=message, command=command)
        case "market":
            await commands.display.markets.DisplayMarket(message=message, command=command)
        
        # Job commands
        case "jobs":
            if constants.ENABLE_JOBS:
                await commands.display.jobs.DisplayJobs(message=message)
        case "apply":
            if constants.ENABLE_JOBS:
                await commands.apply.Apply(message=message, command=command)
        case "info":
            if constants.ENABLE_JOBS:
                await commands.display.jobs.DisplayJobInfo(message=message, command=command)

        # Item commands
        case "buy":
            await commands.inventory.Buy(message=message, command=command)
        case "sell":
            await commands.inventory.Sell(message=message, command=command)
        case "inventory":
            await commands.display.inventory.DisplayInventory(message=message)
        case "inv":
            await commands.display.inventory.DisplayInventory(message=message, command=command)
        case "use":
            await commands.inventory.UseItem(message=message, command=command)
        case "give":
           await commands.inventory.Give(message=message, command=command)
        

        case "clock":
            await commands.display.clock.DisplayClock(message=message)
        case "energy":
            await commands.display.energy.DisplayEnergy(message=message)
        case "changelogs":
            await commands.display.changelog.DisplayChangelog(message=message)
        case "changelog":
            await commands.display.changelog.DisplayChangelog(message=message)
        case "changes":
            await commands.display.changelog.DisplayChangelog(message=message)
        case "cl":
            await commands.display.changelog.DisplayChangelog(message=message)
        
        # OPERATOR COMMANDS
        case "operator":
            await commands.operator.permissions.AddOperator(message=message, command=command)
        case "op":
            await commands.operator.permissions.AddOperator(message=message, command=command)
        case "deop":
            await commands.operator.permissions.RemoveOperator(message=message, command=command)
        case "save":
            await commands.operator.management.ManualSave(message=message)
        case "addcash":
            await commands.operator.cheats.money.AddCash(message=message, command=command)
        case "ac":
            await commands.operator.cheats.money.AddCash(message=message, command=command)
        case "removecash":
            await commands.operator.cheats.money.RemoveCash(message=message, command=command)
        case "rc":
            await commands.operator.cheats.money.RemoveCash(message=message, command=command)
        case "adddeposit":
            await commands.operator.cheats.money.AddDeposit(message=message, command=command)
        case "ad":
            await commands.operator.cheats.money.AddDeposit(message=message, command=command)
        case "removedeposit":
            await commands.operator.cheats.money.RemoveDeposit(message=message, command=command)
        case "rd":
            await commands.operator.cheats.money.RemoveDeposit(message=message, command=command)
        
        # Gambling commands

        case "blackjack":
            if not constants.ENABLE_BJ:
                return
            await commands.gambling.blackjack.BlackJack(message=message, command=command)
        case "bj":
            if not constants.ENABLE_BJ:
                return
            await commands.gambling.blackjack.blackjack.BlackJack(message=message, command=command)
        case "slots":
            if not constants.ENABLE_SLOTS:
                return
            await commands.gambling.slots.SlotMachine(message=message, command=command)
        case "roulette":
            if not constants.ENABLE_ROULETTE:
                return
            await commands.gambling.roulette.Roulette(message=message, command=command)

        case _: # None of the above.
            embed = discord.Embed(title="   Invalid Command..",description=f"do ``{constants.PREFIX}help`` to see all commands and command groups.", color=constants.EXCEPTION_COLOR)
            await message.reply(embed=embed)


singletons.client.run(os.getenv("econtoken"))
