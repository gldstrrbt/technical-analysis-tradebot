import time, requests, csv, json
from datetime import datetime

crypto_list = ["Bitcoin", "Ethereum", "Tether", "ripple", "Chainlink", "Litecoin", "Bitcoin Cash", "polkadot-new", "binancecoin", "Cardano", "bitcoin-cash-sv", "USD Coin", "EOS", "Wrapped Bitcoin", "Monero", "TRON", "Stellar", "crypto-com-chain", "Tezos", "leo-token", "Neo", "filecoin", "NEM", "Cosmos", "Dai", "ethlend", "Huobi Token", "Uniswap", "Dash", "yearn.finance", "VeChain", "IOTA", "Waves", "Ethereum Classic", "Binance USD", "Zcash", "theta-token", "havven", "celsius-degree-token", "Maker", "OMG Network", "Compound", "UMA", "Ontology", "Dogecoin", "FTX Token", "OKB", "Kusama", "Algorand", "Basic Attention Token", "bittorrent-2", "NEAR Protocol", "DigiByte", "republic-protocol", "0x", "true-usd", "Decred", "SushiSwap", "HUSD", "Paxos Standard", "HedgeTrade", "Zilliqa", "Qtum", "reserve-rights-token", "Ocean Protocol", "Loopring", "ICON", "Kyber Network", "Hedera Hashgraph", "quant-network", "Bitcoin Gold", "Augur", "THORChain", "Lisk", "Ampleforth", "Blockstack", "Nexo", "terra-luna", "Band Protocol", "Aragon", "ZB Token", "Revain", "Siacoin", "Decentraland", "enjincoin", "SwissBorg", "Elrond", "Numeraire", "CyberVein", "Bitcoin Diamond", "Nano", "The Midas Touch Gold", "Ravencoin", "Status", "Golem", "Bancor", "DxChain Token", "Bytom", "Matic Network", "Kava", "MonaCoin", "Arweave", "holotoken", "iExec RLC", "Swipe", "PAX Gold", "iostoken", "IoTeX", "Verge", "Uquid Coin", "Nervos Network", "MaidSafeCoin", "Gnosis", "zencash", "Storj", "Velas", "KuCoin Shares", "Divi", "Utrust", "Steem", "Komodo", "Civic", "Ankr", "BitShares", "Kleros", "Unibright", "TomoChain", "Chiliz", "Ardor", "aelf", "SingularityNET", "Hive", "Wanchain", "OriginTrail", "SUN", "Keep3rV1", "Syscoin", "Ark", "iris-network", "WAX", "Tellor", "Theta Fuel", "bZx Protocol", "hshare", "Quark-Chain", "Flexacoin", "Energi", "Electroneum", "NOIA Network", "Pundi X", "Fantom", "Stratis", "Fetch-ai", "monaco", "Hyperion", "Kin", "STASIS eurs", "Power Ledger", "Zcoin", "Switcheo", "Loki-network", "Hxro", "WaykiChain", "gatechain-token", "solve-care", "Aeternity", "Harmony", "Aion", "poly", "systems", "xDai", "sero", "Handshake", "adex", "concierge-io", "Ultra", "WINk", "district0x", "Haven", "streamr-datacoin", "ethos", "digitex-futures-exchange", "VIDT Datalink", "Tixl", "IZE", "Counos X", "INO COIN", "HEX", "Insight Chain", "Bitcoin Cash ABC", "Cipher Core Token", "Homeros", "renBTC", "ThoreCoin", "MINDOL", "Creditcoin", "Zelwin", "Basid Coin", "BitcoinPoS", "TNC Coin", "Strong", "botXcoin", "Poseidon Network", "Largo Coin", "Doctors Coin", "Vitae", "Sologenic", "STPAY", "Cryptonex", "YUSRA", "DeFiChain", "TerraKRW", "Helper Search Token", "XinFin Network", "Metacoin", "Bitcoin BEP2", "NewYork Exchange", "Huobi BTC", "Idea Chain Coin", "Bitball Treasure", "Neutrino USD", "Mixin", "Beldex", "GreenPower", "The Transfer Token", "Qcash", "BASIC", "Counos Coin", "Bitbook Gambling", "NEST Protocol", "Mobilian Coin", "Attila", "Joule", "S4FE", "Baer Chain", "MimbleWimbleCoin", "Wrapped BNB", "Hegic", "Oasis Network", "Darma Cash", "MATH", "Tap", "Nexxo", "WhiteCoin", "Keep Network", "Centrality", "Orbit Chain", "AXEL", "Breezecoin", "Chimpion", "CRYPTOBUCKS", "Bankera", "Bitpanda Ecosystem Token", "BTU Protocol", "Elitium", "Bithao", "Amp", "YF Link", "Tratin", "VestChain", "Hellenic Coin", "Sora", "XeniosCoin", "Harvest Finance", "NerveNetwork", "mStable USD", "Rocket Pool", "STEM CELL COIN", "ReddCoin", "cVault.finance", "Zynecoin", "ExtStock Token", "Ultiledger", "Flamingo", "Bonorum", "TitanSwap", "Bloomzed Loyalty Club Ticket", "Metaverse Dualchain Network Architecture", "KardiaChain", "UNI COIN", "Cryptoindex.com 100", "CRYPTO20", "PlayFuel", "USDK", "Melon", "Orbs", "NuCypher", "Thunder Token", "TROY", "Bytecoin", "Axie Infinity", "BOSAGORA", "Everus", "Gleec", "FunFair", "GXChain", "Elastos", "Nectar", "Buggyra Coin Zero", "BitMax Token", "Alpha Finance Lab", "Livepeer", "Venus", "BHEX Token", "MXC", "LTO Network", "Request", "TrustSwap", "CONUN", "COTI", "Trust Wallet Token", "Etherisc DIP Token", "Loom Network", "DAD", "Folgory Coin", "AgaveCoin", "Native Utility Token", "NULS", "Nash Exchange", "ASTA", "1irstcoin", "IDEX", "sUSD", "Wirex Token", "MX Token", "The Sandbox", "Origin Protocol", "Orion Protocol", "Everipedia", "Secret", "ChainX", "Dynamic Trading Rights", "USDX [Kava]", "Mainframe", "VeThor Token", "Levolution", "Bella Protocol", "PARSIQ", "VerusCoin", "OctoFi", "BigONE Token", "ThoreNext", "WOM Protocol", "Metal", "Hashgard", "Cortex", "BORA", "saffron.finance", "Huobi Pool Token", "PIVX", "Injective Protocol", "Beam", "ARPA Chain", "Sport and Leisure", "PancakeSwap", "Ripio Credit Network", "Xensor", "Celer Network", "Zap", "FNB Protocol", "yieldfarming.insure", "Nexalt", "WazirX", "Cindicator", "Akropolis", "Pirate Chain", "YEP COIN", "HARD Protocol", "Ignis", "PeepCoin", "SALT", "YAM v1", "Nebulas", "SAFE2", "Obyte", "CONTRACOIN", "Bridge Oracle", "Bluzelle", "Newscrypto", "Nimiq", "Audius", "Crypterium", "Quantstamp", "BDCC Bitica COIN", "PRIZM", "Grin", "StormX", "Davinci Coin", "Dent", "Invictus Hyperion Fund", "New Year Bull", "Celo Dollar", "TrueChain", "Meta", "Beowulf", "SUKU", "Wixlar", "12Ships", "Rakon", "BitcoinHD", "Dinastycoin", "RChain", "B2BX", "King DAG", "Groestlcoin", "Dragonchain", "Darwinia Network", "Unobtanium", "Molecular Future", "Zenon", "Morpheus.Network", "AirSwap", "DigixDAO", "Function X", "ZBG Token", "SaluS", "Standard Tokenization Protocol", "Agoras Tokens", "DMM: Governance", "Stakenet", "Gas", "Measurable Data Token", "Gemini Dollar", "LBRY Credits", "MediBloc", "Akash Network", "DREP", "Jewel", "Proton", "BHPCoin", "Advanced Internet Blocks", "BitKan", "Prometeus", "Populous", "Sentivate", "PLATINCOIN", "MVL", "Kcash", "Crypto Village Accelerator", "Lambda", "REPO", "Massnet", "Dusk Network", "Fusion", "Sapphire", "Contentos", "IQeon", "MovieBloc", "Bounce Token", "Covesting", "Render Token", "Ergo", "PowerPool", "MiL.k", "Project Pai", "Waves Enterprise", "NKN", "Aergo", "Einsteinium", "DOS Network", "Chromia", "Bitcoin 2", "Aurora", "USDJ", "Cocos-BCX", "Phala.Network", "ERC20", "Nexus", "GHOSTPRISM", "Bit-Z Token", "Perpetual Protocol", "0Chain", "QASH", "Peculium", "GNY", "Metronome", "Apollo Currency", "YFValue", "Level01", "Sapien", "Monolith", "Veritaseum", "Block-Chain.com", "Content Value Network", "CWV Chain", "Enigma", "Moeda Loyalty Points", "Anchor", "YFDAI.FINANCE", "FABRK", "Gem Exchange And Trading", "dForce", "Quantum Resistant Ledger", "Kadena", "BIKI", "The Force Protocol", "Perlin", "Tachyon Protocol", "Carry", "Metadium", "Phoenix Global", "Gifto", "Propy", "Factom", "FOAM", "CoinMetro Token", "QuickX Protocol", "BTSE", "Metaverse ETP", "Raiden Network Token", "BitForex Token", "Decentralized Vulnerability Platform", "Waltonchain", "yOUcash", "Constellation", "Seele-N", "AMO Coin", "Dimension Chain", "Precium", "Nxt", "Elamachain", "smARTOFGIVING", "CUTcoin", "LinkEye", "Safex Token", "Blocknet", "Maro", "FirmaChain", "PlatonCoin", "Aavegotchi", "Dynamic", "Insights Network", "Free Tool Box Coin", "Namecoin", "Vertcoin", "Swerve", "MixMarvel", "Alchemy Pay", "Selfkey", "Spendcoin", "Lightning Bitcoin", "FIBOS", "DMarket", "Unifi Protocol DAO", "apM Coin", "Exchange", "pNetwork", "LATOKEN", "1SG", "FirstBlood", "Cartesi", "Atomic Wallet Coin", "Global Digital Content", "Anchor Neural World", "VIDY", "Aladdin", "Telcoin", "Dune Network", "Santiment Network Token", "Egoras", "TenX", "Wing", "LiquidApps", "VITE", "Nestree", "UniLend", "Props Token", "TrustVerse", "Arcblock", "APIX", "SynchroBitcoin", "Hakka.Finance", "dKargo", "DEXTools", "LCX", "Cream Finance", "BoringDAO", "Grid+", "Minter Network", "Observer", "ZEON", "NEXT", "BnkToTheFuture", "Steem Dollars", "Dock", "PAC Global", "Dawn Protocol", "Burger Swap", "Time New Bank", "Skycoin", "RSK Smart Bitcoin", "Nuco.cloud", "ProximaX", "ROOBEE", "Global Cryptocurrency", "MAP Protocol", "ILCOIN", "Newton", "Peercoin", "FIO Protocol", "MetaHash", "Aleph.im", "OST", "Sentinel Protocol", "Effect.AI", "High Performance Blockchain", "CasinoCoin", "Qitmeer", "Ecoreal Estate", "GameCredits", "LockTrip", "Valor Token", "inSure", "NavCoin", "Endor Protocol", "Aeon", "Aidos Kuneen", "FOOD", "CyberMiles", "PEAKDEFI", "Wabi", "LikeCoin", "FarmaTrust", "Unitrade", "VideoCoin", "Spectre.ai Dividend Token", "IoT Chain", "Universa", "Orient Walt", "Eminer", "Tokamak Network", "Moss Coin", "Achain", "GoChain", "suterusu", "TOP", "OTOCASH", "SIRIN LABS Token", "Karatgold Coin", "Ubiq", "Safe Haven", "Leverj", "PCHAIN", "Dero", "POA", "UCA Coin", "Everex", "Wagerr", "Bread", "Electra", "FLETA", "KeeperDAO", "Neblio", "Aragon Court", "Morpheus Labs", "Digix Gold Token", "JD Coin", "Atari Token", "Sparkpoint", "qiibee", "BackPacker Coin", "Genesis Vision", "EUNO", "Krios", "Realio Network", "CoinEx Token", "DAOstack", "Dragon Coins", "HYCON", "RING X PLATFORM", "AppCoins", "Cashaa", "PlayChip", "Zano", "Metrix Coin", "ODEM", "REVV", "PolySwarm", "HUNT", "Wings", "CryptoFranc", "Robonomics.network", "Particl", "Emirex Token", "Tokenomy", "TokenClub", "Meme", "PumaPay", "DigitalBits", "USDQ", "Pluton", "MOAC", "Quiztok", "WePower", "OAX", "CyberFM", "Aryacoin", "Bezant", "Bibox Token", "Ferrum Network", "Feathercoin", "TronEuropeRewardCoin", "NaPoleonX", "dForce USDx", "Bitcoin Rhodium", "Viacoin", "ALQO", "Multi Channel Influencer Creater Cloud Funding Platform", "VeriDocGlobal", "PieDAO DOUGH v2", "Wowbit", "All Sports", "Nsure.Network", "SunContract", "ECC", "ColossusXT", "DEAPcoin", "Credit Tag Chain", "Blox", "MIR COIN", "Polybius", "BitMart Token", "Polis", "Robotina", "INLOCK", "Ternio", "Mithril", "QunQun", "CoTrader", "INT", "GridCoin", "YOYOW", "Sentinel", "XIO", "Noku", "SmartCash", "VNDC", "bitCNY", "BLOCKv", "Lamden", "SONM", "Callisto Network", "Origo", "Casino Betting Coin", "InflationCoin", "Ruff", "Gulden", "VIBE", "Cryptopay", "Phantasma", "Lykke", "HyperDAO", "Olive", "Kryll", "Telos", "Phore", "SpaceChain", "APY.Finance", "Airbloc", "NAGA", "PressOne", "EveryCoin", "SwftCoin", "OneRoot Network", "Safe", "Etheroll", "OS", "ChronoCoin", "Frontier", "Budbo", "Bitrue Coin", "Kambria", "DEX", "Mooncoin", "Burst", "Pillar", "Epic Cash", "Flash", "MicroBitcoin", "Rapidz", "Hubii Network", "Diamond Platform Token", "Agrocoin", "VeriBlock", "StakeCubeCoin", "GAPS", "SingularDTV", "Game.com", "JustLiquidity", "QLC Chain", "Diamond", "BIZZCOIN", "Burst", "Neumark", "SmartMesh", "PANTHEON X", "Wootrade", "Anyswap", "ShipChain", "Decentrahub Coin", "DigitalNote", "Safe", "LINA", "XTRABYTES", "Trade Token X", "Auctus", "Credits", "Swace", "SENSO", "SonoCoin", "Sense", "Egretia", "MediShares", "Idena", "Bitcore", "DiFy.Finance", "DODO", "Genaro Network", "AirWire", "Matrix AI Network", "DATA", "Artfinity", "Sylo", "ZIMBOCASH", "GeoDB", "DSLA Protocol", "Crust", "DDKoin", "XYO", "eBitcoin", "Blackmoon", "EXMO Coin", "ZrCoin", "Aitra", "TEMCO", "DECOIN", "SymVerse", "Rupiah Token", "YOU COIN", "Cred", "NIX", "XMax", "STATERA", "Clams", "Agrello", "LUKSO", "EasyFi", "Earneo", "Counterparty", "WeShow Token", "GMB", "Mobius", "BarnBridge", "LiteDoge", "Viberate", "Abyss", "GoCrypto Token", "Voise", "Dentacoin", "HEIDI", "Myriad", "Nucleus Vision", "Midas", "AIDUS TOKEN", "Zipper", "Lynx", "GET Protocol", "Monetha", "Merculet", "GHOST", "Hashshare", "UnlimitedIP", "Rotharium", "WPP TOKEN", "Edge", "Carboncoin", "PLANET", "Remme", "Credo", "MintCoin", "Vid", "Hydro Protocol", "FLO", "Atlas Protocol", "Network", "Acute Angle Cloud", "Shift", "Polyient Games Governance Token", "SaTT", "DOC.COM", "Fatcoin", "Zel", "Spartan Protocol", "EOSDT", "ONOToken", "CACHE Gold", "United Traders Token", "42-coin", "EDUCare", "Digital Asset Guarantee Token", "EDC Blockchain", "Databroker", "Cloudbric", "Jibrel Network", "DistX", "HoryouToken", "Stealth", "Ambrosus", "NextDAO", "LINKA", "PIBBLE", "Radium", "HitChain", "ScPrime", "BUX Platform Token", "Xaurum", "CryptoPing", "Compendia", "Change", "NuShares", "CommerceBlock", "Insight Protocol", "1World", "TRONCLASSIC", "Cryptocean", "Mysterium", "OKCash", "Esportbits", "BOLT", "Coineal Token", "BaaSid", "Ethereum Meta", "TERA", "Kingdom Game 4.0", "Skrumble Network", "Apex", "Geeq", "Tripio", "Rarible", "VNT Chain", "Bean Cash", "BitGreen", "UniLayer", "Raven Protocol", "SIX", "Holyheld", "IG Gold", "HTMLCOIN", "Cube", "Growth DeFi", "MB8 Coin", "Presearch", "LNX Protocol", "Electronic Energy Coin", "LOLTOKEN", "Spectre.ai Utility Token", "Global Social Chain", "Ivy", "Rubycoin", "Waves Community Token", "BitCapitalVendor", "Sphere", "Gulden", "Blockmason Credit Protocol", "DeFinition", "Constant", "TrueFlip", "Education Ecosystem", "Dimecoin", "MoonSwap", "DAPS Coin", "Xaya", "ContentBox", "Alias", "CargoX", "Winding Tree", "Jarvis Network", "Omni", "Bloom", "Defis Network", "Colu Local Network", "Ulord", "Bismuth"]
curr_filename = ""

def write_csv(filename):
	a = open(filename+".csv", "w", newline="")
	return csv.writer(a)


def call_url(ticker):
	a = requests.get("https://api.alternative.me/v2/ticker/" + str(ticker) + "/")
	# print(a.status_code)
	# print(a.content)
	if a.status_code == 200:
		return a.json()


def mod_string(ticker):
	ticker = str(ticker).lower().replace("/", "").replace("   ", "-").replace("  ", "-").replace(" ", "-")
	return ticker


def get_vals(dataset):
	a = []
	if dataset["metadata"]["error"] == "unknown id":
		return False
	else:
		for b in dataset["data"]:
			for c in dataset["data"][b]:
				# print(dataset["data"][b][c])
				if str(c) == "quotes":
					print(dataset["data"][b]["quotes"]["USD"])
					for d in dataset["data"][b]["quotes"]["USD"]:
						print(dataset["data"][b]["quotes"]["USD"][d])
						a.append(dataset["data"][b]["quotes"]["USD"][d])
				else:
					a.append(dataset["data"][b][c])
		# print("-"*50)
		print(a)
		return a


def init_collection():
	while True:	
		curr_filename 	= str(datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "-")
		high_ratio_log 	= write_csv("high_ratio_log--" + curr_filename) 
		high_ratio_log.writerow(["id", "name", "symbol", "website_slug", "rank", "circulating_supply", "total_supply", "max_supply", "price", "volume_24h", "market_cap", "percentage_change_1h", "percentage_change_24h", "percentage_change_7d", "last_updated"])
		
		for a in crypto_list:
			a = mod_string(a)
			b = call_url(a)
			c = get_vals(b)
			
			if c == False:
				high_ratio_log.writerow([a,c])
			else:
				c.append(get_ratio(c))
				high_ratio_log.writerow(c)
			time.sleep(1.02)
		time.sleep(5)

########################################################################
########################################################################

def read_csv(filename):
	a = open(filename+".csv", "r")
	b = csv.reader(a)
	return [c for c in b]

def get_ratio_csv(dataset):
	for b, a in enumerate(dataset):
		if b > 0:
			try:
				if float(a[9])/float(a[10]) > 0.3:
					print(a[2] + ":  " + str(float(a[9])/float(a[10])))
			except:
				pass

def get_ratio(dataset):
	# try:
	return float(dataset[9])/float(dataset[10])
	# except:
		# return False

########################################################################
########################################################################

def init():
	a = read_csv("high_ratio_log--2020-11-20_16-40-25-443318")
	get_ratio(a)
	print("-"*50)
	print("-"*50)
	a = read_csv("high_ratio_log--2020-11-20_18-09-03-225142")
	get_ratio(a)

########################################################################
########################################################################


init_collection()
# init()