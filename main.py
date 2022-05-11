import asyncio 
import csv 
import aiohttp 


wallets = list() 
raffle_entries = list()


with open("eth.csv", newline='') as f:
	reader = csv.DictReader(f)
	wallets = [row['WALLET ADDRESS'] for row in reader]


def make_tasks(session, wallets):
  tasks = [session.get(f"https://mint-api.zeta-nft.io/?address={wallet}") for wallet in wallets]
  return tasks 

def log_results(results): 
	with open("results.csv", "w", newline="") as f:
		headers= ["WALLET ADDRESS", "ZETA RESULT"]
		writer = csv.DictWriter(f, fieldnames=headers)
		writer.writeheader()
		[writer.writerow({"WALLET ADDRESS": pair[0], "ZETA RESULT": pair[1]}) for pair in results]

async def main():
	async with aiohttp.ClientSession() as session:
		tasks = make_tasks(session, wallets)
		results = await asyncio.gather(*tasks)
		for result in results:
			response = await result.text()
			wallet = str(result.url).replace("https://mint-api.zeta-nft.io/?address=","")
			raffle_entries.append([response, wallet])
		log_results(raffle_entries)

asyncio.run(main())