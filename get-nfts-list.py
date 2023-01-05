import argparse
import csv
import requests
import time
import sys

from datetime import datetime, timedelta
from pathlib import Path

# Inputs
parser = argparse.ArgumentParser()
parser.add_argument("--ticker", help="Ticker of the collection", required=True)
parser.add_argument("--trait_type", help="Item to retrieve", required=False)
parser.add_argument("--name", help="Item to retrieve", required=False)
parser.add_argument("--duration", help="Number of day(s) of holding", required=False)

args = parser.parse_args()

# Constants
EMOON_ADDRESS = "erd1w9mmxz6533m7cf08gehs8phkun2x4e8689ecfk3makk3dgzsgurszhsxk4"
DEAD_RARE_ADDRESS = "erd1qqqqqqqqqqqqqpgqd9rvv2n378e27jcts8vfwynpx0gfl5ufz6hqhfy0u0"
TRUST_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgq6wegs2xkypfpync8mn2sa5cmpqjlvrhwz5nqgepyg8"
FRAMEIT_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgq705fxpfrjne0tl3ece0rrspykq88mynn4kxs2cg43s"
ELROND_NFT_SWAP_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgq8xwzu82v8ex3h4ayl5lsvxqxnhecpwyvwe0sf2qj4e"
ISENGARD_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgqy63d2wjymqergsxugu9p8tayp970gy6zlwfq8n6ruf"

# creating a black listed array so that these addresses won't get the token
black_listed_addresses = [EMOON_ADDRESS,
                          DEAD_RARE_ADDRESS,
                          TRUST_WALLET_ADDRESS,
                          FRAMEIT_WALLET_ADDRESS,
                          ELROND_NFT_SWAP_WALLET_ADDRESS,
                          ISENGARD_WALLET_ADDRESS]

nft_collection_name = args.ticker
days_of_holding = 0 if args.duration is None else int(args.duration)
values = []
single_wallet = []
all_wallet = []
current_date = datetime.now()

if days_of_holding > 0:
    end_date = current_date + timedelta(days=-days_of_holding)
    timestamp = end_date.timestamp()
    timestamp = int(timestamp)

i = 0
while i < 10000:
    nfts = requests.get(f'https://api.multiversX.com/collections/{nft_collection_name}/nfts?from=' + str(
        i) + '&size=100&withOwner=true').json()
    try:
        if nfts['message'] == 'Validation failed for argument \'collection\': Invalid collection identifier.':
            print(f'Collection {nft_collection_name} does not exist\n')
            sys.exit()
    except:
        pass
    for nft in nfts:
        if args.trait_type and args.name:
            try:
                for item_query in nft['metadata']['attributes']:
                    if args.trait_type == item_query['trait_type'] and args.name == item_query['value']:
                        if nft["owner"] not in single_wallet:
                            single_wallet.append(nft["owner"])
                        all_wallet.append(nft["owner"])
            except:
                pass
        else:
            try:
                if nft["owner"] not in single_wallet:
                    single_wallet.append(nft["owner"])
                all_wallet.append(nft["owner"])
            except:
                pass
    time.sleep(0.09)
    i = i + 100

# files name
if args.trait_type and args.name:
    txt_file = current_date.strftime(f"%b-%d-%Y-{nft_collection_name}-{args.name}.txt")
    result_csv = current_date.strftime(f"output/%b-%d-%Y-{nft_collection_name}-{args.name}")
else:
    if args.duration is not None and days_of_holding > 0:
        txt_file = current_date.strftime(f"%b-%d-%Y-with-duration-{nft_collection_name}.txt")
        result_csv = current_date.strftime(f"output/%b-%d-%Y-with-duration-{nft_collection_name}")
    else:
        txt_file = current_date.strftime(f"%b-%d-%Y-{nft_collection_name}.txt")
        result_csv = current_date.strftime(f"output/%b-%d-%Y-{nft_collection_name}")

for wallet in single_wallet:
    if wallet not in black_listed_addresses:
        if args.duration is None or days_of_holding == 0:
            value = {"owner": wallet, "nftsCount": all_wallet.count(wallet)}
            values.append(value)
        elif args.duration is not None and days_of_holding > 0:
            api_url = f"https://api.multiversX.com/accounts/{wallet}/nfts?size=10000&search={nft_collection_name}"
            r = requests.get(api_url)
            nfts = r.json()
            all_nfts = len(nfts)
            if args.trait_type and args.name:
                eligible_nfts = 0
                for nft in nfts:
                    time.sleep(0.09)
                    nft_identifier = nft["identifier"]
                    try:
                        for item_query in nft['metadata']['attributes']:
                            if args.trait_type == item_query['trait_type'] and args.name == item_query['value']:
                                transactions_with_nfts_url = f"https://api.multiversX.com/transactions?status=success&token={nft_identifier}&after={timestamp}&withScamInfo=false"
                                r = requests.get(transactions_with_nfts_url)
                                txs = r.json()
                                if len(txs) == 0:
                                    # didn't found transactions, adding to eligible nfts
                                    eligible_nfts = eligible_nfts + 1
                    except:
                        pass

                value = {"owner": wallet, "nftsCount": eligible_nfts}
                values.append(value)
            else:
                eligible_nfts = all_nfts
                for nft in nfts:
                    time.sleep(0.09)
                    nft_identifier = nft["identifier"]
                    eligible_nfts = all_nfts
                    transactions_with_nfts_url = f"https://api.multiversX.com/transactions?status=success&token={nft_identifier}&after={timestamp}&withScamInfo=false"
                    r = requests.get(transactions_with_nfts_url)
                    txs = r.json()
                    if len(txs) != 0:
                        # found transactions, subtracting from eligible nfts
                        eligible_nfts = eligible_nfts - 1

                value = {"owner": wallet, "nftsCount": eligible_nfts}
                values.append(value)

# Create output
name_of_file = "output/{}".format(txt_file)

p = Path('output')
p.mkdir(parents=True, exist_ok=True)
func_txt = open(name_of_file, "w")

values.sort(key=lambda x: x.get('nftsCount'), reverse=True)

with open(current_date.strftime(f"{result_csv}.csv"), "wt") as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Address", "Count"])  # write header

    for output in values:
        func_txt.write(output.__str__() + "\n")
        writer.writerow([output['owner'], output['nftsCount']])

# Compute useful info

total_nft = 0
average = 0

for nft in range(0, len(values)):
    total_nft = total_nft + values[nft]['nftsCount']

if len(values) > 0:
    average = round(total_nft / len(values), 2)

print(f'\n----- OUTPUT INFO -----\n')
print(f'Number of wallets: {len(values)}')
print(f'Number of NFTs: {total_nft}\n')
print(f'Average Nbr of NFTs per wallet {average}\n')
print('No duration specified' if args.duration is None else f'For last {days_of_holding} Day(s)')
print(f'\n----- Made by ElrondBuddies <3 -----\n')
