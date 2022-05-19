import argparse
import csv
import requests

from datetime import datetime
from pathlib import Path

# Inputs
parser = argparse.ArgumentParser()
parser.add_argument("--ticker", help="Ticker of the collection", required=True)
parser.add_argument("--trait_type", help="Item to retrieve", required=False)
parser.add_argument("--name", help="Item to retrieve", required=False)


args = parser.parse_args()

# Constants
EMOON_ADDRESS = "erd1w9mmxz6533m7cf08gehs8phkun2x4e8689ecfk3makk3dgzsgurszhsxk4"
DEAD_RARE_ADDRESS = "erd1qqqqqqqqqqqqqpgqd9rvv2n378e27jcts8vfwynpx0gfl5ufz6hqhfy0u0"
TRUST_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgq6wegs2xkypfpync8mn2sa5cmpqjlvrhwz5nqgepyg8"
FRAMEIT_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgq705fxpfrjne0tl3ece0rrspykq88mynn4kxs2cg43s"
ELROND_NFT_SWAP_WALLET_ADDRESS = "erd1qqqqqqqqqqqqqpgq8xwzu82v8ex3h4ayl5lsvxqxnhecpwyvwe0sf2qj4e"
ISENGARD_WALLET_ADDRESS="erd1qqqqqqqqqqqqqpgqy63d2wjymqergsxugu9p8tayp970gy6zlwfq8n6ruf"

# creating a black listed array so that these addresses won't get the token
black_listed_addresses = [EMOON_ADDRESS,
                          DEAD_RARE_ADDRESS,
                          TRUST_WALLET_ADDRESS,
                          FRAMEIT_WALLET_ADDRESS,
                          ELROND_NFT_SWAP_WALLET_ADDRESS,
                          ISENGARD_WALLET_ADDRESS]

nft_collection_name = args.ticker
values=[]
single_wallet = []
all_wallet = []
current_date = datetime.now()

if args.trait_type and args.name:
    i = 0
    while i < 1000:
        nfts = requests.get(f'https://api.elrond.com/collections/{nft_collection_name}/nfts?from=' + str(
            i) + '&size=100&withOwner=true').json()
        for nft in nfts:
            try:
                for item_query in nft['metadata']['attributes']:
                    if args.trait_type == item_query['trait_type'] and args.name == item_query['value']:
                        if nft["owner"] not in single_wallet:
                            single_wallet.append(nft["owner"])
                        all_wallet.append(nft["owner"])
            except:
                pass
        i = i + 100

    # files name
    txt_file = current_date.strftime(f"%b-%d-%Y-{nft_collection_name}-{args.name}.txt")
    result_csv = current_date.strftime(f"output/%b-%d-%Y-{nft_collection_name}-{args.name}")

else:
    i = 0
    while i < 10000:
        nfts = requests.get(f'https://api.elrond.com/collections/{nft_collection_name}/nfts?from=' + str(
            i) + '&size=100&withOwner=true').json()
        for nft in nfts:
            try:
                if nft["owner"] not in single_wallet:
                    single_wallet.append(nft["owner"])
                all_wallet.append(nft["owner"])
            except:
                pass
        i = i + 100

    # files name
    txt_file = current_date.strftime(f"%b-%d-%Y-{nft_collection_name}.txt")
    result_csv = current_date.strftime(f"output/%b-%d-%Y-{nft_collection_name}")

for wallet in single_wallet:
    if wallet not in black_listed_addresses:
        value = {"owner": wallet, "nftsCount": all_wallet.count(wallet)}
        values.append(value)

#Create output
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

