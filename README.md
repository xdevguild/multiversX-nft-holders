# elrond-nft-holders
elrond-nft-holders

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
