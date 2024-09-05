#!/usr/bin/env python3
import requests
import logging
from datetime import datetime
import discord 
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

client = discord.Client(intents=discord.Intents.default())

def writeGasRecordTxt(fileName, inputTxt):
    targetTxtFile = open(fileName, "w")
    targetTxtFile.write(str(inputTxt))
    targetTxtFile.close()

def getFileContent(fileName):
    targetTxtFile = open(fileName, "r")
    fileContent = targetTxtFile.read()
    targetTxtFile.close()
    return fileContent

def priceChecking ():
  try:
    res = requests.get(url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}', headers={"content-type": "application/json"})
    price_res = requests.get(url = f'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={ETHERSCAN_API_KEY}', headers={"content-type": "application/json"})
    data = res.json()
    price_data = price_res.json()

    global time_tracker
    global current_gas

    new_gas = float(data['result']['SafeGasPrice'])
    new_price = float(price_data['result']['ethusd'])
    time_difference = (datetime.now() - time_tracker).total_seconds()/60
    gas_difference = float((new_gas - float(current_gas))/ float(current_gas))
    change_percentage = str((round(gas_difference*100,4)))

    deploy_contract_gas = str(format(new_gas * 5487449 * 1e-9, '.8f'))
    usd_deploy_gas = str(round((new_gas * 5487449  * 1e-9) * new_price, 2))
    
    interaction_gas = str(format(new_gas * 40297 * 1e-9, '.8f'))
    usd_interaction_gas = str(round((new_gas * 40297* 1e-9) * new_price, 2))
    
    mint_gas = str(format(new_gas * 235330 * 1e-9, '.8f'))
    usd_mint_gas = str(round((new_gas * 235330 * 1e-9) * new_price, 2))

    msg = ('Gas changed ' + change_percentage + '%, in ' + 
    str(round(time_difference,2)) + 'minutes, current Safe Gas Price: ' + str(new_gas) + "Gwei \n" + 
    "est. Smart Contract Deployment Cost: " + deploy_contract_gas + "ETH / "+ usd_deploy_gas +"USD, \n" + 
    "est. Interaction Cost: " + interaction_gas + "ETH / "+ usd_interaction_gas +"USD, \n" + 
    "est. Mint/Airdrop Cost: " + mint_gas + "ETH / "+ usd_mint_gas +"USD, \n" + 
    "Current ETH/USD: " + str(new_price)
    )
    print(msg)
    writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/prevGasLog.txt", str(new_gas))

    if(new_gas == current_gas): 
      #init
      pass
    elif(gas_difference >= 2 or gas_difference <= -0.7):
      #2x or -0.7
      print(datetime.now(), ':: 200/70:: gas changed ', gas_difference*100, '%, current gas: ', new_gas)
      writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/gasRecord.txt", new_gas)
      writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/timeTrack.txt", datetime.now())
    elif(gas_difference >= 1 or gas_difference <= -0.5):
      #1x or -0.5
      if(time_difference <= 5):
        #timer
        print(datetime.now(), ':: not 5 min yet, current gas: ', new_gas)
      else:
        print(datetime.now(), ':: 100/50:: gas changed ', gas_difference*100, '%, current gas: ', new_gas)
        writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/gasRecord.txt", new_gas)
        writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/timeTrack.txt", datetime.now())
    elif( gas_difference >= 0.2 or gas_difference <= -0.1):
      #0.2x or -0.1
      if(time_difference <= 60):
        #timer
        print(datetime.now(), ':: not 60 min yet, current gas: ', new_gas)
      else:
        print(datetime.now(), ':: 20/10:: gas changed ', gas_difference*100, '%, current gas: ', new_gas)
        writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/gasRecord.txt", new_gas)
        writeGasRecordTxt(os.path.dirname(os.path.realpath(__file__))+"/timeTrack.txt", datetime.now())
    else:
      print(datetime.now(), ':: Out Of Bound: gas changed ', gas_difference*100, '%, current gas: ', new_gas)
    return msg
    
  except requests.exceptions.RequestException as e:
    logging.error('req error: {}'.format(e.response.status_code))
    logging.error(e.response)
    pass

if __name__ == "__main__":
  current_gas = getFileContent(os.path.dirname(os.path.realpath(__file__))+"/gasRecord.txt")
  time_tracker = datetime.strptime(getFileContent(os.path.dirname(os.path.realpath(__file__))+"/timeTrack.txt")[:19], "%Y-%m-%d %H:%M:%S")

  @client.event
  async def on_ready():
      for guild in client.guilds:
          if guild.name == GUILD:
              msg = priceChecking() 
              channel = client.get_channel(DISCORD_CHANNEL_ID)
              await channel.send(msg)
              break

      print(
          f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})'
      )
      await client.close()

  client.run(TOKEN)

  priceChecking()
