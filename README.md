# MultiversX-nft-holders
multiversX-nft-holders

## NFTs holder
Generate a CSV and text file, which shows your NFTs holders and the displays a column of how many NFTs **are in the wallet**.
You can also get all the holders holding NFTs with a specif trait.

#### Getting started
##### 1. Configuring Python
You need to have Python installed on your machine or in the virtual environment.

Check your Python version by running:

```shell
$ python3 --version
```

After that run

```shell
$ pip install -r requirements.txt
```

##### 2. Run the script

```bash
python get-nfts-list.py --ticker EBUDDIES-e18a04
```

```bash
python get-nfts-list.py --ticker EBUDDIES-e18a04 --trait_type Mouth --name Smile
```

Check the **output** folder for results.


<p align="center" >
  <img width="451" alt="CSV" src="https://user-images.githubusercontent.com/23435882/169235388-da661a26-903a-433b-bbac-6829a11b255b.png"><br>
  <b>CSV output</b>
</p>



If you want to distribute $LKMEX or ESDT to your holders you can use this script with the CSV file generated:
https://github.com/xdevguild/esdt-and-lkmek-airdrop-scripts


<p align="center" >
  <img src="https://user-images.githubusercontent.com/23435882/169236163-2ed5bd72-df97-4865-aa28-bf2695e52e43.png"><br>
  <b>Made with ❤️ by Elrond Buddies</b>
</p>
