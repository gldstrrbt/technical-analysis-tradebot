import os, json, requests, time, csv, matplotlib, mpl_finance
from Robinhood import Robinhood
import numpy as np
import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import matplotlib.font_manager as font_manager
from mpl_finance import candlestick2_ohlc
from mpl_finance import index_bar
from mpl_finance import plot_day_summary_oclh
import datetime as datetime
# import robin_stocks as r
# login = r.login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))
# shit = r.get_historicals("TSLA")
# print(shit)

####################################################################################################
####################################################################################################
####################################################################################################

# test 							= Robinhood()

tags 							= ["top-movers", "etf", "100-most-popular", "mutual-fund", "finance", "cap-weighted", "investment-trust-or-fund", "female-ceo", "loan", "real-estate", "entertainment", "manufacturing", "e-commerce", "retail", "kids", "satellite", "broadcasting", "wireless", "digital-television", "television", "electronics", "radio", "automotive", "transportation", "computer-networking", "telecommunications", "upcoming-earnings", "computer-hardware", "road-transportation", "internet", "material", "integrated-circuit", "asia-non-china", "engineering", "packaging", "metal", "us", "business-service", "north-america", "3xetf", "etf", "aerospace", "air-transportation", "professional-service", "investment-service", "cancer", "data-service", "outsourcing", "logistics", "most-popular-under-25", "sports", "consumer-product", "photovoltaic"]
rh_list 						= ["STBFY", "TCEHY", "NTDOY", "HEINY", "OGZPY", "CJPRY", "ACBFF", "WJRYY", "EJPRY", "MIELY", "SMFKY", "EZJ", "ESYJY", "KNBWY", "EADSY", "CABGY", "MITEY", "VOD", "ZTCOY"]
global_stocks 					= ['TCEHY', 'NTDOY', 'ADDYY', 'ACBFF', 'BMWYY', 'YAHOY', 'ZTCOY', 'VWAGY', 'NSRGY', 'SFTBY', 'NSANY', 'BAYRY', 'FUJHY', 'EADSY', 'PCRFY', 'RHHBY', 'SIEGY', 'VLVLY', 'PNGAY', 'BDRBF', 'MZDAY', 'GLNCY', 'DMLRY', 'POAHY', 'CZMWY', 'HYPMY', 'TKPYY', 'RYCEY', 'FUJIY', 'KNYJY', 'VWDRY', 'FANUY', 'HTHIY', 'RKUNY', 'HEINY', 'WIMHY', 'LUXTY', 'NPSNY', 'EXPGY', 'BYDDY', 'ASOMY', 'INVVY', 'SSEZY', 'GELYY', 'ESALY', 'BRDCY', 'SEOAY', 'AMADY', 'PDYPY', 'LUKOY', 'BURBY', 'TOELY', 'FRFHF', 'IMASY', 'SZKMY', 'OGZPY', 'SKYAY', 'SGSOY', 'IMBBY', 'TSCDY', 'IFNNY', 'SOUHY', 'WNGRF', 'OTSKY', 'HOCPY', 'ADRNY', 'RBGLY', 'SSDOY', 'SWGAY', 'NRBAY', 'ITVPY', 'LNSTY', 'KMTUY', 'MAURY', 'MRAAY', 'TTDKY', 'STBFY', 'HENOY', 'ZURVY', 'SMNNY', 'AWCMY', 'BAESY', 'DSDVY', 'NTTYY', 'SHZHY', 'CIBEY', 'CICHY', 'OMRNY', 'SEKEY', 'SGBLY', 'TTNDY', 'SUBCY', 'GKNLY', 'DNZOY', 'KAOOY', 'MKTAY', 'SMGZY', 'OCPNY', 'CHYHY', 'KNBWY', 'KYOCY', 'CFRUY', 'MEGEF', 'DTEGY', 'CIOXY', 'UMICY', 'ANZBY', 'SNPHY', 'SHCAY', 'TATYY', 'HCMLY', 'TRYIY', 'DKILY', 'SVNDY', 'SONVY', 'AACAY', 'GMXAY', 'RWEOY', 'WEICY', 'PSMMY', 'ONEXF', 'RIOCF', 'AMKBY', 'LZAGY', 'AMCRY', 'MAKSY', 'AGESY', 'AVVIY', 'WEGRY', 'SBRCY', 'COVTY', 'BCAUY', 'FRHLF', 'WTKWY', 'ATGFF', 'CPYYY', 'KGFHY', 'TELNY', 'NILSY', 'NJDCY', 'NHYDY', 'DPSGY', 'CMWAY', 'DNKEY', 'SOMMY', 'AHEXY', 'NDEKY', 'ESYJY', 'MURGY', 'EMRAF', 'LIMAF', 'SWRAY', 'IDCBY', 'CABGY', 'NCMGY', 'UNICY', 'SDVKY', 'CKHUY', 'PPERY', 'DSNKY', 'SGTPY', 'NTIOF', 'BKRKY', 'CSLLY', 'RDSMY', 'BDORY', 'FSUGY', 'GLPEY', 'SMFKY', 'KZMYY', 'ICAGY', 'SHECY', 'DLAKY', 'MIELY', 'CLLDY', 'CLPBY', 'EONGY', 'LLESY', 'SMCAY', 'WARFY', 'ACGBY', 'ORKLY', 'TLSNY', 'CMPGY', 'BNTGY', 'NVZMY', 'MITSY', 'SSUMY', 'CIFAF', 'GBOOY', 'TKOMY', 'AAGIY', 'HDELY', 'BACHY', 'KDDIY', 'HGKGY', 'SSMXY', 'FJTSY', 'CIHKY', 'VDMCY', 'ITOCY', 'BZLFY', 'SSREY', 'OVCHY', 'SCHYY', 'CTTAY', 'PBSFY', 'MHGVY', 'FRRVY', 'GVDNY', 'FQVLF', 'PEYUF', 'CRZBY', 'RTOKY', 'HVRRY', 'SWDBY', 'CLPHY', 'SGAPY', 'WTBDY', 'GZPFY', 'RTMVY', 'MDIBY', 'TMSNY', 'WOPEY', 'DCMYY', 'DSEEY', 'MTNOY', 'ASGLY', 'ESSYY', 'BXBLY', 'SOMLY', 'SAXPY', 'SYIEY', 'KCDMY', 'CSUAY', 'COIHY', 'MRWSY', 'SLLDY', 'NABZY', 'BTLCY', 'TEZNY', 'ACSAY', 'SUHJY', 'SVNLY', 'JAPAY', 'DBSDY', 'WFTBF', 'DBOEY', 'FUPBY', 'ROYMY', 'OISHY', 'SKHSY', 'MITEY', 'SCMWY', 'SPKKY', 'EBKDY', 'JMHLY', 'HKXCY', 'MONOY', 'DIFTY', 'DNHBY', 'UOVEY', 'APELY', 'SKFRY', 'RYKKY', 'SKHHY', 'MTZPY', 'KPCPY', 'KBCSY', 'UUGRY', 'NNGRY', 'RDEIY', 'CJPRY', 'EMLAF', 'DQJCY', 'CCOJY', 'QBIEY', 'PWCDF', 'POFNF', 'MSADY', 'DWAHY', 'MQBKY', 'WJRYY', 'JSHLY', 'EJPRY', 'CDNAF', 'SPXCY', 'IFJPY', 'JPXGY', 'FERGY']
watchlist 						= ["HGSH", "TWLO", "NDEKY", "NHYDY", "OMRNY"]
most_popular 					= ['FB', 'AAPL', 'F', 'AMD', 'GE', 'MSFT', 'FIT', 'GPRO', 'TWTR', 'NFLX', 'BABA', 'SNAP', 'CRON', 'AMZN', 'TSLA', 'NVDA', 'BAC', 'MU', 'DIS', 'SQ', 'SBUX', 'CHK', 'CGC', 'T', 'IQ', 'INTC', 'ZNGA', 'SIRI', 'GRPN', 'XXII', 'S', 'JD', 'PLUG', 'ATVI', 'RAD', 'BRK.B', 'PYPL', 'VOO', 'WMT', 'DBX', 'GOOGL', 'V', 'SHOP', 'SPY', 'NVAX', 'CSCO', 'GM', 'KO', 'CRM', 'PFE', 'APRN', 'INSY', 'GERN', 'VZ', 'GLUU', 'ROKU', 'AMAT', 'NKE', 'GOOG', 'SPOT', 'BA', 'UAA', 'AUY', 'VTI', 'TLRY', 'MJ', 'COST', 'TEVA', 'JCP', 'LUV', 'TRXC', 'BILI', 'BOTZ', 'JPM', 'CARA', 'ABBV', 'JNJ', 'P', 'VSLR', 'CRSP', 'ADBE', 'NOK', 'ENPH', 'HUYA', 'QQQ', 'CY', 'SNE', 'CRBP', 'UA', 'SPWR', 'TGT', 'RUN', 'BIDU', 'XOM', 'PG', 'BZUN', 'WFC', 'QCOM', 'KR', 'CMCSA']
bots_index 						= ["BOTZ"]
semiconductor_index 			= ["XSD"]
top_movers 						= ['BOX', 'WPRT', 'BLDP', 'MDXG', 'YRD', 'ACHN', 'UIS', 'ASRT', 'GKOS', 'MOV', 'SCVL', 'KPTI', 'BMA', 'METC', 'GGAL', 'BPI', 'SCSC', 'EDN', 'WINS', 'DGICB']
cap_weighted 					= ['VOO', 'SPY', 'VTI', 'QQQ', 'VWO', 'TQQQ', 'VNQ', 'VGT', 'NUGT', 'VEA', 'SCHD', 'IVV', 'FDN', 'VIG', 'SOXL', 'GDX', 'VT', 'VXUS', 'UPRO', 'MORL', 'SCHK', 'SCHB', 'FTEC', 'SQQQ', 'IWM', 'ICLN', 'ITOT', 'ITA', 'VEU', 'VGK', 'VB', 'XLE', 'INDA', 'FINX', 'MCHI', 'CQQQ', 'PPA', 'IBB', 'IJR', 'SCHH', 'YINN', 'IEMG', 'SMH', 'SOXX', 'DUST', 'SCHF', 'AMLP', 'EMQQ', 'TECL', 'XLU', 'CGW', 'SCHX', 'DFEN', 'SPXU', 'XLY', 'FAS', 'XLP', 'SCHA', 'VNQI', 'BRZU', 'VDE', 'SOCL', 'EWJ', 'SPXS', 'SSO', 'TZA', 'QCLN', 'EWZ', 'VYMI', 'FHLC', 'QLD', 'GDXJ', 'IYR', 'SH', 'FAZ', 'XLI', 'MGC', 'URA', 'EFA', 'PSCH', 'IEFA', 'INDY', 'TNA', 'SDS', 'TUR', 'VPU', 'VNM', 'REM', 'IYW', 'FNCL', 'EWY', 'GREK', 'VIOO', 'ITB', 'IJH', 'PNQI', 'ONEQ', 'IVOO', 'VOT', 'VCR', 'VDC', 'IGV', 'GXC', 'VSS', 'LMLP', 'ERX', 'RSX', 'SOXS', 'EWH', 'VV', 'BDCL', 'EWG', 'REET', 'IHI', 'MORT', 'SMIN', 'VPL', 'QQQC', 'SCHV', 'REML', 'VXF', 'IXUS', 'CHIQ', 'FENY', 'VIGI', 'SHE', 'FDIS', 'EDC', 'SCHM', 'XLRE', 'AFK', 'SPFF', 'AIQ', 'IWO', 'IPO', 'EWS', 'EZU', 'XLB', 'SBIO', 'DSI', 'SPSM', 'YANG', 'VOX', 'EWW', 'MLPA', 'MRRL', 'NGE', 'VTWO', 'IWV', 'KSA', 'XLC', 'VIS', 'EWA', 'FEZ', 'SLYG', 'SCIF', 'IGM', 'KBA', 'FREL', 'PAVE', 'SIL', 'BIB', 'EWC', 'EUFN', 'BJK', 'CURE', 'PAK', 'IXN', 'AMJ', 'QID', 'RING', 'ROM', 'RWR', 'ARGT', 'PGF', 'INXX', 'FM', 'TECS', 'VAW', 'PICK', 'MDY', 'ERUS', 'SLVP', 'USD', 'DRV', 'VONE', 'IVOG', 'GEX', 'RTH', 'RUSL', 'SPDW', 'COPX', 'EWQ', 'PSQ', 'EWZS', 'EWU', 'CXSE', 'URTY', 'KORU', 'ACWI', 'PGJ', 'ILF', 'AAXJ', 'SCZ', 'FIDU', 'IHF', 'IGF', 'DRN', 'SILJ', 'BIZD', 'IYF', 'INCO', 'EZA', 'EWM', 'FSTA', 'IEUR', 'TAO', 'NORW', 'SLY', 'IYE', 'IWB', 'SCHC', 'DAX', 'PSCT', 'CWB', 'RWX', 'SLYV', 'KOL', 'EWL', 'IFGL', 'EPOL', 'CRAK', 'EPHE', 'FPX', 'ENZL', 'EIDO', 'FRN', 'IXC', 'CATH', 'EWI', 'IYY', 'EDZ', 'IEV', 'EEMA', 'REZ', 'IYZ', 'FINU', 'ERY', 'PKW', 'EWGS', 'CARZ', 'ASEA', 'RUSS', 'ADRE', 'FUTY', 'IWP', 'UBIO', 'EFV', 'OEF', 'VRP', 'SRTY', 'IYH', 'IETC', 'RWO', 'SPMD', 'DBJP', 'VTHR', 'SLX', 'SRS', 'IWC', 'EWP', 'SGDM', 'SPLG', 'MDYG', 'GRID', 'QAT', 'GWX', 'MOO', 'JSML', 'SPAB', 'SOIL', 'MVV', 'BBH', 'IEO', 'IXJ', 'USRT', 'CHIX', 'VIOV', 'MIDU', 'BRF', 'IGE', 'EURL', 'EWD', 'ISRA', 'IYG', 'CNYA', 'FCOM', 'JSMD', 'BKF', 'FMAT', 'EGPT', 'YAO', 'HAO', 'TWM', 'EWO', 'RWM', 'IAI', 'CUT', 'GMF', 'SCJ', 'GXF', 'PFM', 'PLND', 'BZQ', 'WCHN', 'IXP', 'UAE', 'ACWX', 'EFG', 'NLR', 'EIRL', 'IPKW', 'SPUU', 'GDXX', 'EWX', 'IWL', 'EWN', 'LBJ', 'DBEU', 'BTEC', 'PSCU', 'EPU', 'IWR', 'FRI', 'PSCE', 'IJK', 'IDEV', 'AMJL', 'UYG', 'BBJP', 'IYC', 'WMCR', 'PPH', 'IPAC', 'CWI', 'REK', 'SHNY', 'DIG', 'CAPE', 'ENOR', 'ADRA', 'IYJ', 'OLD', 'GDXS', 'ECON', 'RXL', 'CNXT', 'REW', 'JKE', 'IEME', 'LBDC', 'EEMS', 'UWM', 'IDX', 'EWK', 'SKF', 'ZBIO', 'BIS', 'KBWP', 'IYK', 'KXI', 'IPOS', 'JXI', 'YXI', 'UBR', 'FINZ', 'LRET', 'IEUS', 'CHIE', 'CHIM', 'IDU', 'IHE', 'MIDZ', 'SPDN', 'UMDD', 'FEU', 'IXG', 'DYLS', 'MDYV', 'IGN', 'PFFR', 'EDEN', 'JKD', 'PSCC', 'FPXI', 'HEZU', 'XSOE', 'IYM', 'AMU', 'ADRU', 'BBEU', 'GII', 'MLPI', 'FLCH', 'SEF', 'IFEU', 'EWUS', 'MXI', 'SPXT', 'DXJF', 'EMIF', 'PSCI', 'URE', 'BBRC', 'SMDD', 'PSAU', 'FLIN', 'XLG', 'UGE', 'SPXV', 'IEZ', 'EXI', 'SSG', 'UCC', 'PAGG', 'UXI', 'ASHX', 'SPXN', 'CHII', 'FLKR', 'JKK', 'NFRA', 'TOK', 'PSCF', 'RXI', 'JKL', 'DBGR', 'SAA', 'EEB', 'CN', 'SPXE', 'SRVR', 'HDAW', 'DYB', 'XINA', 'FLRU', 'WPS', 'IEDI', 'SMLL', 'WREI', 'DDG', 'SCC', 'EPV', 'SDP', 'JKG', 'DBEM', 'FFR', 'RVRS', 'MYY', 'DPK', 'SMN', 'PSCD', 'MZZ', 'BBRE', 'HDEF', 'JKH', 'FLBR', 'UPV', 'SIJ', 'SBB', 'RTL', 'DBAP', 'XMX', 'FTAG', 'MLPO', 'RXD', 'IMLP', 'FLCA', 'FLAU', 'ROAM', 'SDD', 'UYM', 'DEFA', 'IECS', 'IEFN', 'DEZU', 'LTL', 'EZJ', 'JKF', 'DEWJ', 'CROP', 'AMUB', 'EFZ', 'FLGB', 'EURZ', 'FLTW', 'JKJ', 'FLSW', 'FLAX', 'GRI', 'FLJH', 'FLEE', 'SBM', 'WIL', 'URTH', 'FLEH', 'MLPB', 'ACIM', 'EFU', 'AMCA', 'EMEM', 'THD', 'CNHX', 'SZK', 'MEXX', 'PPDM', 'EMXC', 'EFNL', 'EIS', 'ECH', 'PPEM', 'PBEE', 'SMMD', 'ADRD', 'EPP', 'PEX', 'VEGI', 'PRID', 'AGT', 'BIBL', 'DBUK']
alcohol 						= ['KO', 'COST', 'MO', 'ROX', 'STZ', 'BUD', 'DG', 'BREW', 'TAP', 'NBEV', 'DEO', 'ABEV', 'FLWS', 'ACT', 'BF.B', 'BGS', 'REED', 'SAM', 'BJRI', 'SIVB', 'THST', 'BLL', 'HEINY', 'BORN', 'MSN', 'MGPI', 'AAC', 'WVVI', 'KNBWY', 'BF.A', 'BLMN', 'EGRX', 'CABGY', 'FFHL', 'BID', 'MIDD', 'CCU', 'WMK', 'TRC', 'CKH', 'BDL', 'STZ.B', 'SEB', 'LABL', 'TAP.A', 'WVVIP']
beer 							= ['COST', 'STZ', 'DG', 'BREW', 'TAP', 'DEO', 'ABEV', 'REED', 'SAM', 'BJRI', 'BLL', 'KNBWY', 'CABGY', 'CCU', 'WMK', 'BDL', 'STZ.B', 'TAP.A']
china 							= ['BIDU', 'BABA', 'IQ', 'BILI', 'HUYA', 'SOGO', 'SSC', 'YY', 'CPHI', 'RCON', 'TAL', 'FXI', 'SINA', 'XNET', 'ASX', 'VIPS', 'JKS', 'UXIN', 'KWEB', 'CNET', 'TAOP', 'SEED', 'RENN', 'MCHI', 'CQQQ', 'BSTI', 'YUMC', 'ALN', 'GLG', 'SORL', 'FTFT', 'NFEC', 'YINN', 'CJJD', 'CREG', 'KGJI', 'SSW', 'ZTO', 'EDU', 'CTRP', 'XIN', 'CBAK', 'YRD', 'BITA', 'HTHT', 'CHL', 'DQ', 'BSPM', 'ATAI', 'LEDS', 'KNDI', 'LKM', 'SKYS', 'SOL', 'CCIH', 'CGA', 'NCTY', 'ZKIN', 'HPJ', 'ASHR', 'BGNE', 'JMEI', 'SFUN', 'SMI', 'CMCM', 'NEW', 'WUBA', 'HMI', 'HIHO', 'CLDC', 'CWEB', 'AMCN', 'UTSI', 'MLCO', 'YECO', 'GXC', 'NOAH', 'EWH', 'CLWT', 'ATV', 'HGSH', 'CYOU', 'QQQC', 'JP', 'TYHT', 'CHIQ', 'LFC', 'ATHM', 'SNP', 'TCEHY', 'SOHU', 'CO', 'ABAC', 'CADC', 'FANH', 'SEII', 'CCCL', 'VNET', 'BORN', 'RYB', 'JMU', 'LEJU', 'YANG', 'PME', 'ZNH', 'OSN', 'GSUM', 'GURE', 'JT', 'CHU', 'TEDU', 'ITP', 'DSWL', 'HOLI', 'GDS', 'KBA', 'SHI', 'CHAU', 'ACH', 'LLIT', 'LITB', 'SVA', 'FENG', 'YIN', 'SGOC', 'CIFS', 'CHNR', 'GIGM', 'ZLAB', 'LX', 'CAF', 'CXSE', 'HX', 'JOBS', 'PGJ', 'PTR', 'JRJC', 'FFHL', 'CEA', 'TAO', 'KONE', 'WBAI', 'REDU', 'BNSO', 'HCM', 'CAAS', 'CXDC', 'PPDF', 'HNP', 'SECO', 'CCM', 'DSUM', 'CHA', 'CBPO', 'XRF', 'CHT', 'DL', 'EVK', 'APWC', 'CHAD', 'NTP', 'TOUR', 'CHIX', 'CNYA', 'YAO', 'HAO', 'GSH', 'AFTY', 'WCHN', 'CYB', 'KANG', 'ASHS', 'CEO', 'BCNA', 'COE', 'AMBO', 'EHIC', 'FHK', 'DXF', 'XPP', 'HLG', 'STG', 'CANG', 'CNXT', 'CHN', 'PEK', 'YXI', 'CHIM', 'CHIE', 'FXP', 'BEDU', 'ECNS', 'FLCH', 'GHG', 'KFYP', 'XCEM', 'CHII', 'ASHX', 'CBON', 'ONE', 'CN', 'FEDU', 'XINA', 'FCA', 'KALL', 'HAHA', 'FXCH', 'FLHK', 'JG', 'KCNY', 'DELT', 'HEBT', 'TMSR', 'KCCB', 'FORK', 'FAMI', 'CNHX', 'SSWN', 'KGRN', 'EMXC', 'KBSF', 'TKAT', 'SSWA', 'SSW-H', 'KURE', 'BCAC', 'DOGZ', 'PETZ', 'NEWA', 'BCACU', 'MOXC', 'BCACW', 'RETO', 'BRQS', 'CCRC', 'WINS', 'GRNQ', 'BCACR', 'SSLJ', 'TANH', 'LYL', 'CNTF', 'CYD']
asia 							= ['BABA', 'IQ', 'IGC', 'BILI', 'HUYA', 'SOGO', 'TSM', 'SSC', 'NSPR', 'YY', 'CPHI', 'LPL', 'RCON', 'RWLK', 'WIX', 'NTEC', 'TAL', 'INFY', 'TRPX', 'FXI', 'TTM', 'TM', 'SINA', 'SSYS', 'XNET', 'ASX', 'VIPS', 'SIFY', 'JKS', 'UXIN', 'KWEB', 'CNET', 'TAOP', 'SEED', 'ABIL', 'RENN', 'INDA', 'IBN', 'MCHI', 'CQQQ', 'BSTI', 'YUMC', 'ALN', 'NNDM', 'GLG', 'SORL', 'CRNT', 'FTFT', 'NFEC', 'YINN', 'CAMT', 'CJJD', 'CREG', 'KGJI', 'SSW', 'ZTO', 'EDU', 'CTRP', 'PLX', 'XIN', 'CBAK', 'YRD', 'FLEX', 'BITA', 'HTHT', 'KTOV', 'CYBR', 'CHL', 'DQ', 'CHEK', 'BSPM', 'ATAI', 'LEDS', 'KNDI', 'EWJ', 'LKM', 'SKYS', 'SOL', 'CCIH', 'CGA', 'WIT', 'MUFG', 'NCTY', 'ZKIN', 'GLMD', 'HPJ', 'ASHR', 'BGNE', 'JMEI', 'TSEM', 'SFUN', 'TUR', 'INDY', 'LN', 'SMI', 'CAJ', 'CMCM', 'VBLT', 'NEW', 'WUBA', 'VNM', 'HMI', 'NMR', 'HIHO', 'SE', 'ANFI', 'ICL', 'MLNX', 'EWY', 'CLDC', 'SODA', 'CWEB', 'ATTU', 'EPI', 'AMCN', 'UTSI', 'AUDC', 'MLCO', 'HDB', 'YECO', 'GXC', 'NOAH', 'FAX', 'RDHL', 'EWH', 'MFG', 'CLWT', 'ATV', 'HGSH', 'SMIN', 'CYOU', 'QQQC', 'JP', 'CHKP', 'TYHT', 'RDWR', 'SPCB', 'CHIQ', 'LFC', 'MMYT', 'KRNT', 'DXJ', 'ATHM', 'SNP', 'TCEHY', 'HQCL', 'SOHU', 'CO', 'ABAC', 'CADC', 'INDL', 'FANH', 'EWS', 'SEII', 'CCCL', 'VNET', 'BORN', 'RYB', 'JMU', 'LEJU', 'YANG', 'PME', 'ZNH', 'MGIC', 'NVMI', 'OSN', 'GSUM', 'SMFG', 'GURE', 'JT', 'KSA', 'CHU', 'TEDU', 'ITP', 'APOP', 'CGEN', 'DSWL', 'HOLI', 'GDS', 'NTTYY', 'KBA', 'SCIF', 'ORMP', 'SHI', 'TKC', 'CHAU', 'ACH', 'PAK', 'LLIT', 'LITB', 'KYOCY', 'ORBK', 'SVA', 'PIN', 'ITEQ', 'INXX', 'RDY', 'AIA', 'BLRX', 'FENG', 'FOMX', 'YIN', 'ESLT', 'SGOC', 'CIFS', 'CHNR', 'GIGM', 'NJDCY', 'ZLAB', 'LX', 'CAF', 'VNRX', 'IZRL', 'CXSE', 'HX', 'JOBS', 'KORU', 'URGN', 'PGJ', 'PTR', 'JRJC', 'AAXJ', 'FFHL', 'CEA', 'WNS', 'INCO', 'EWM', 'TAO', 'CYRN', 'ASLN', 'KONE', 'WBAI', 'EPHE', 'REDU', 'BNSO', 'IIJI', 'EIDO', 'HCM', 'IFN', 'KT', 'AZRE', 'OASI', 'STDY', 'EEMA', 'CAAS', 'IGLD', 'ASEA', 'HEWJ', 'SILC', 'SCIN', 'BVXV', 'CXDC', 'DFJ', 'ELTK', 'PPDF', 'HNP', 'NICE', 'SECO', 'DBJP', 'CCM', 'DSUM', 'CHA', 'CBPO', 'CEL', 'XRF', 'CSTE', 'CHT', 'FXY', 'DL', 'EVK', 'CANF', 'APWC', 'CHAD', 'NTP', 'TOUR', 'CHIX', 'RDCM', 'ISRA', 'CNYA', 'DCMYY', 'EGPT', 'YAO', 'HAO', 'BCOM', 'VEDL', 'GSH', 'WVE', 'AFTY', 'GRVY', 'GMF', 'SCJ', 'MDWD', 'WCHN', 'CYB', 'KANG', 'ASHS', 'CEO', 'TARO', 'BCNA', 'JPNL', 'BVXVW', 'COE', 'AMBO', 'IIF', 'BBJP', 'EHIC', 'JOF', 'PNTR', 'FHK', 'DXF', 'XPP', 'HLG', 'STG', 'CANG', 'ADRA', 'ITRN', 'TLK', 'KEN', 'CNXT', 'CHN', 'CALL', 'IDX', 'ICLK', 'DXJS', 'TWN', 'JPN', 'PEK', 'YXI', 'CHIM', 'CHIE', 'MDGS', 'FXP', 'ALLT', 'BEDU', 'IX', 'FRSX', 'ECNS', 'GSJY', 'FLCH', 'APF', 'JEQ', 'DXJF', 'CHEKW', 'FLIN', 'GHG', 'KFYP', 'PTNR', 'XCEM', 'SCIJ', 'CHII', 'ASHX', 'KB', 'FLKR', 'PKX', 'PHI', 'CBON', 'AXJV', 'ONE', 'CN', 'THFF', 'FEDU', 'JHDG', 'JPMV', 'HEWY', 'XINA', 'CLGN', 'FCA', 'AXJL', 'FTEO', 'FJP', 'DBAP', 'ALD', 'SCIX', 'FORTY', 'SHG', 'KALL', 'HAHA', 'FXCH', 'HFXJ', 'FLJP', 'FLHK', 'MNDO', 'JG', 'KCNY', 'EWV', 'FXSG', 'DEWJ', 'QJPN', 'PAF', 'RADA', 'EZJ', 'DDJP', 'WF', 'RFAP', 'FLTW', 'FLAX', 'FPA', 'FLJH', 'KEP', 'KTOVW', 'DELT', 'XTLB', 'PSTI', 'OTIV', 'HEBT', 'MAGS', 'TMSR', 'KCCB', 'DVYA', 'EMITF', 'FORK', 'FAMI', 'THD', 'CNHX', 'MDGSW', 'SSWN', 'BOSC', 'KGRN', 'EMXC', 'NFTY', 'KBSF', 'KMDA', 'EVGN', 'YTRA', 'TKAT', 'SSWA', 'SSW-H', 'ENTX', 'KURE', 'NSPR+B', 'CHEKZ', 'BCAC', 'EIS', 'NSPR+', 'DOGZ', 'PETZ', 'TATT', 'EWT', 'NEWA', 'BCACU', 'MOXC', 'BCACW', 'RETO', 'ORPN', 'ENTXW', 'FKO', 'BRQS', 'EPP', 'KLIC', 'MTSL', 'CCRC', 'WINS', 'APOPW', 'DBKO', 'SLGL', 'GZT', 'TISA', 'GILT', 'GRNQ', 'SKM', 'BCACR', 'SSLJ', 'TANH', 'LYL', 'WILC', 'ELLO', 'OBAS', 'CNTF', 'CYD']
r_and_d 						= ['GOOGL', 'GOOG', 'BA', 'TRXC', 'CARA', 'LMT', 'CLDX', 'GILD', 'GWPH', 'EKSO', 'CYTR', 'OLED', 'SGMO', 'RNN', 'BMY', 'ALT', 'OPK', 'APTO', 'ARRY', 'WPRT', 'SRNE', 'AUO', 'GALT', 'ABB', 'ACAD', 'AKAO', 'AGN', 'SEED', 'CLSN', 'IMMU', 'BTX', 'DMPI', 'DFFN', 'REGI', 'ARQL', 'IGT', 'CBAY', 'VSAR', 'SPEX', 'LPCN', 'CVM+', 'OVAS', 'WIT', 'TSRO', 'XBIO', 'ACHV', 'MYGN', 'VERU', 'ALRM', 'AIMT', 'GNMX', 'KLAC', 'SNSS', 'ALIM', 'PRAN', 'CNHI', 'PRTO', 'IDCC', 'UTHR', 'KURA', 'VICL', 'SNP', 'IMI', 'CBLI', 'IIVI', 'DYSL', 'NYMX', 'EFOI', 'TKPYY', 'REPH', 'IMTE', 'CGEN', 'CWBR', 'ORMP', 'RYAM', 'UBX', 'IFF', 'CDTX', 'WEICY', 'SELB', 'BHVN', 'ENTA', 'PTR', 'AZRX', 'TBIO', 'SEIC', 'HCM', 'NVZMY', 'JHX', 'CRL', 'OASM', 'FJTSY', 'CBT', 'NTP', 'DBVT', 'THRM', 'TRNO', 'ARPO', 'MSA', 'MDGS', 'OSIR', 'BTX+', 'GLPG', 'ARGX', 'UFPT', 'MOR', 'IMRN', 'NBRV', 'CLLS', 'RYAM-A', 'MDGSW', 'EVGN', 'EYEN', 'IMRNW']
electric_utilities 				= ['GE', 'SPWR', 'FSLR', 'DRYS', 'FCEL', 'CSIQ', 'HON', 'SO', 'PCG', 'PBR', 'DUK', 'NRG', 'CIG', 'PPL', 'NFEC', 'BW', 'EXC', 'XEL', 'AEP', 'FE', 'EIX', 'HES', 'NGG', 'EVA', 'PBR.A', 'AT', 'EBR', 'ORA', 'ADES', 'VWDRY', 'SSEZY', 'OGZPY', 'POR', 'HE', 'TAC', 'ETR', 'PWR', 'MKTAY', 'RWEOY', 'CMS', 'OGE', 'GVP', 'PAM', 'HNRG', 'CHRA', 'BKH', 'VVC', 'HNP', 'EBR.B', 'YPF', 'AXE', 'IDA', 'MGEE', 'VEDL', 'NWE', 'PNM', 'ANDE', 'EDN', 'ENIA', 'CEPU', 'CIG.C', 'KEP', 'ELLO', 'DUKH', 'EAE', 'TVC', 'CPL', 'EMP', 'EZT', 'EAI', 'CMSA', 'TVE', 'EAB', 'BKHU']
renewables 						= ['RGSE', 'PEGI', 'CPST', 'OPTT', 'SO', 'BEP', 'DUK', 'TAN', 'TERP', 'ENB', 'VLO', 'JKS', 'AES', 'AQN', 'HASI', 'CVA', 'JE', 'NFEC', 'REGI', 'CREG', 'FAN', 'NEP', 'DQ', 'BW', 'MTZ', 'SOL', 'AETI', 'AY', 'MXIM', 'BAM', 'AGX', 'TPIC', 'AMSC', 'EIX', 'HYGS', 'VVPR', 'CZZ', 'EVA', 'PBR.A', 'AT', 'AMRC', 'ORA', 'HQCL', 'SIEGY', 'DAR', 'VWDRY', 'SEII', 'SRE', 'TAC', 'ACH', 'ORBK', 'RWEOY', 'ATGFF', 'AGR', 'NHYDY', 'TEX', 'NTGN', 'PCH', 'AZRE', 'ROCK', 'ALE', 'MMAC', 'VMI', 'PW', 'CMCO', 'HNI', 'ATNI', 'FUE', 'KEP', 'DUKH', 'JE-A', 'PW-A', 'EVGN', 'SOJB', 'IEA', 'IEAWW', 'SOJA', 'TANH', 'ENBA', 'SOJC']
female_ceo 						= ['AMD', 'GM', 'BILI', 'IBM', 'EDIT', 'LMT', 'SFIX', 'JAGX', 'AVP', 'NDAQ', 'SYF', 'MBII', 'MAT', 'SNES', 'WTW', 'PCG', 'GSK', 'DUK', 'TELL', 'AWK', 'WPRT', 'LTC', 'KSS', 'TRVN', 'CATB', 'GD', 'ISR', 'CAPR', 'DARE', 'VTR', 'IBN', 'ULTA', 'NNA', 'ALN', 'YUMC', 'KEY', 'EYPT', 'PGR', 'YOGA', 'ROST', 'SNR', 'MYL', 'HTZ', 'CTRP', 'PTI', 'NM', 'YRD', 'NE', 'HSY', 'ACST', 'AJRD', 'IOVA', 'HTHT', 'ACLS', 'LNTH', 'JILL', 'BW', 'SKYS', 'DS', 'KERX', 'NAP', 'HALO', 'OXY', 'AXGN', 'PRLB', 'ADVM', 'NMM', 'NTRI', 'SIG', 'BL', 'WMC', 'CALA', 'EVFM', 'BKD', 'DLTH', 'TOO', 'SBS', 'TCS', 'WSM', 'USG', 'TUP', 'ASNS', 'CVIA', 'CRCM', 'BWEN', 'SES', 'ANTM', 'AKCA', 'SQBG', 'CMC', 'AGTC', 'CBK', 'TYHT', 'RRGB', 'VRML', 'DEST', 'UTHR', 'CBRL', 'CHS', 'BBW', 'ISIG', 'SCHN', 'CO', 'AMN', 'JTPY', 'SYBX', 'GLYC', 'GHDX', 'REPH', 'CTHR', 'MSGN', 'WOW', 'RYB', 'POR', 'HE', 'LWAY', 'TAC', 'WTTR', 'CGEN', 'ITCI', 'VEON', 'VRS', 'CMRX', 'LLIT', 'STAA', 'CODA', 'REV', 'PLCE', 'BLMN', 'SYRS', 'FENG', 'OIS', 'LNT', 'RLJ', 'XENT', 'ZLAB', 'MGTX', 'ARTNA', 'VCYT', 'ACIU', 'JOUT', 'MYOV', 'MRSN', 'FSS', 'PFMT', 'CMS', 'TR', 'ST', 'PLXP', 'BBGI', 'ARTW', 'UTI', 'SNBR', 'ARCB', 'HHS', 'ASIX', 'CLW', 'ATXI', 'EGL', 'CIT', 'TMHC', 'ELS', 'TRTX', 'CLRO', 'ATGE', 'ELMD', 'SSD', 'CMTA', 'EXPO', 'NVT', 'WEX', 'CANF', 'PINC', 'GSH', 'GTLS', 'VISI', 'CAL', 'OMN', 'NCI', 'SR', 'ITT', 'PSB', 'FLXS', 'COE', 'EMO', 'PNM', 'CGG', 'CVG', 'CTBI', 'EE', 'HYI', 'FUNC', 'RDI', 'CEM', 'AMSF', 'RGA', 'VRTV', 'CPF', 'BYSI', 'ISCA', 'CLFD', 'CSTR', 'TLF', 'GM+B', 'IPHS', 'BCTF', 'INSW', 'HBMD', 'NPK', 'HMN', 'LNDC', 'ONE', 'SFBC', 'HMTA', 'BKJ', 'GBLI', 'CABO', 'MNDO', 'HEBT', 'ZEAL', 'RZA', 'DUKH', 'EAE', 'DS-C', 'KBLM', 'NINE', 'TKAT', 'PSB-W', 'CMS-B', 'KEY-I', 'DS-D', 'KBLMR', 'NM-G', 'IPL-D', 'RZB', 'RDIB', 'ORGS', 'KBLMU', 'OPBK', 'KBLMW', 'PSB-U', 'RLM', 'EZT', 'ORPN', 'EAI', 'CMSA', 'NM-H', 'DS-B', 'RLJ-A', 'EAB', 'PSB-V', 'PSB-X', 'FAMI']
loan = []  # large inline historical test dataset removed
real_estate = []  # large inline historical test dataset removed
kids 							= ['ATVI', 'GOOS', 'NWL', 'SKX', 'HBI', 'KSS', 'HAS', 'FL', 'GPS', 'VIPS', 'ASNA', 'ANF', 'CROX', 'DSW', 'GNMX', 'GES', 'SEAS', 'WSM', 'VOXX', 'SUMR', 'DHXM', 'BIG', 'BKE', 'JAKK', 'SCVL', 'CBRL', 'EDUC', 'CRWS', 'PLCE', 'WWW', 'WCG', 'ACHC', 'GNUS', 'THS', 'CRI', 'DDS', 'SHOO', 'KIDS', 'SCHL', 'CSS', 'WEYS', 'BURBY', 'MMS', 'EPC', 'RBGLY']
entertainment 					= ['MSFT', 'NFLX', 'BABA', 'AMZN', 'NVDA', 'DIS', 'T', 'IQ', 'ZNGA', 'SIRI', 'ATVI', 'VZ', 'GLUU', 'COST', 'BILI', 'SNE', 'CMCSA', 'WB', 'TTWO', 'EA', 'HEAR', 'GME', 'AMC', 'IRM', 'WWE', 'NTDOY', 'BBY', 'MGM', 'LLNW', 'AMMA', 'PIR', 'YY', 'XGTI', 'MAT', 'GOGO', 'WYNN', 'FOXA', 'CZR', 'CRUS', 'MDXG', 'NTES', 'NETE', 'MEET', 'ADSK', 'TTM', 'GAMR', 'MANU', 'HAS', 'ICON', 'FOX', 'EVRI', 'DKS', 'COKE', 'KCAP', 'VIAB', 'LVS', 'CTSH', 'BGFV', 'EPR', 'MB', 'CTRL', 'YOGA', 'LYV', 'MARK', 'PLAY', 'DDE', 'FUN', 'VFC', 'FIVE', 'IEP', 'CBS', 'IGT', 'SIX', 'NCMI', 'PENN', 'TSG', 'LEDS', 'BYD', 'DS', 'VSI', 'CCIH', 'SIGM', 'ENT', 'IMMR', 'EVC', 'VSTO', 'SGMS', 'IMAX', 'MGP', 'CMCM', 'HIBB', 'EROS', 'TIVO', 'RICK', 'UWN', 'SE', 'SEAS', 'LGF.A', 'SMSI', 'RACE', 'SBGI', 'DAKT', 'TA', 'VOXX', 'MLCO', 'DHXM', 'SYNA', 'SKIS', 'CHTR', 'GAIA', 'IPG', 'CYOU', 'CNK', 'JASNW', 'QRTEA', 'FLL', 'NWSA', 'MAS', 'VIA', 'IPIC', 'RLJE', 'BBW', 'ARMK', 'TWMC', 'SOHU', 'ERI', 'CCE', 'MBUU', 'JASN', 'TPVG', 'ZUMZ', 'CLUB', 'CLCT', 'MSGN', 'BATRA', 'CSSE', 'XLC', 'RTIX', 'NWS', 'TKC', 'COT', 'OUT', 'LGF.B', 'CNTY', 'DLB', 'CIDM', 'RRR', 'EPAM', 'DVD', 'MCFT', 'XOXO', 'LLIT', 'LOB', 'TZOO', 'MSG', 'FWONA', 'CHDN', 'QUAD', 'ASCMA', 'GDEN', 'GIGM', 'ZBH', 'ARRS', 'CETV', 'TPC', 'GNUS', 'YGYI', 'SNN', 'AAWW', 'RLH', 'DECK', 'RNWK', 'TTC', 'FWONK', 'LSXMA', 'OBCI', 'HHS', 'WBAI', 'PCRFY', 'MCS', 'DYNT', 'CBB', 'CLS', 'KT', 'DOX', 'PNK', 'BATRK', 'LSXMK', 'FANZ', 'RHP', 'LZB', 'TRK', 'MCRI', 'NYNY', 'TSQ', 'CCU', 'TRCO', 'DLPN', 'GPIC', 'DMRC', 'LCA', 'VICI', 'NTN', 'GRVY', 'USPH', 'GCO', 'SVVC', 'HOFT', 'WHLM', 'CSWC', 'CPHC', 'PEJ', 'RCI', 'LIVX', 'WIMHY', 'TRC', 'KF', 'HPP', 'RDI', 'BTN', 'IEME', 'WINA', 'INSE', 'ODC', 'ESL', 'BWL.A', 'ISCA', 'RELV', 'SPLP', 'NPSNY', 'CBS.A', 'SPLP-A', 'QRTEB', 'STRS', 'PDYPY', 'CMLS', 'CABO', 'LSXMB', 'PBSFY', 'TEF', 'SCHYY', 'ITVPY', 'KAP', 'TANNL', 'CBB-B', 'DS-C', 'LCAHW', 'CSWCL', 'DS-D', 'RDIB', 'LCAHU', 'TANNZ', 'MOXC', 'DLPNW', 'CSSEP', 'TBB', 'DS-B', 'EPR-C', 'KCAPL', 'TANNI', 'EMITF', 'EPR-E', 'TPVY']
manufacturing = []  # large inline historical test dataset removed
e_commerce 						= ['BABA', 'AMZN', 'GRPN', 'JD', 'SHOP', 'APRN', 'BIDU', 'BZUN', 'EBAY', 'OSTK', 'MYSZ', 'SSC', 'ODP', 'PDD', 'PIR', 'GOOS', 'CVNA', 'SKX', 'FDX', 'MAT', 'EVLV', 'WIX', 'W', 'NTES', 'NETE', 'JWN', 'VIPS', 'MELI', 'SIFY', 'COOL', 'PBI', 'ELF', 'VSI', 'CCIH', 'MKC', 'CLNY', 'SFUN', 'DGSE', 'BGI', 'YNDX', 'GES', 'SE', 'MAMS', 'WSM', 'RCKY', 'NHTC', 'PRTY', 'QRTEA', 'SFTBY', 'BBW', 'TWMC', 'PRSS', 'VNCE', 'TPVG', 'XWEB', 'BNED', 'LEJU', 'EIGI', 'XSPL', 'SPAR', 'ECOM', 'MLHR', 'LE', 'LQDT', 'AMSWA', 'EBIX', 'SYX', 'HZN', 'CRI', 'GGAL', 'RMBL', 'SECO', 'RKUNY', 'YAHOY', 'BVSN', 'CAL', 'GCO', 'PERY', 'PSMT', 'MKC.V', 'IRCP', 'QRTEB', 'CRTO', 'ADRNY', 'ILPT', 'CCRC', 'TPVY']
retail = []  # large inline historical test dataset removed
satellite 						= ['T', 'SIRI', 'BA', 'CMCSA', 'LMT', 'KTOS', 'GSAT', 'NOC', 'RHT', 'GOGO', 'FOXA', 'EVLV', 'HLIT', 'I', 'IRDM', 'FOX', 'ABIL', 'DISH', 'SJR', 'BDR', 'SPEX', 'MTZ', 'ENT', 'HEI', 'VOXX', 'IDSY', 'EMKR', 'CMTL', 'VSAT', 'MXL', 'FWONA', 'HEI.A', 'LBTYA', 'FWONK', 'LSXMA', 'SATS', 'KT', 'TNAV', 'LSXMK', 'LBTYK', 'TDY', 'HALL', 'BCOM', 'LORL', 'LILA', 'CVG', 'TLK', 'BDC', 'TV', 'KVHI', 'IMASY', 'MIELY', 'LSXMB', 'IRDMB', 'LBTYB', 'BDC-B', 'GILT']
broadcasting 					= ['NFLX', 'AMZN', 'DIS', 'T', 'IQ', 'SIRI', 'ATVI', 'ROKU', 'VZ', 'BILI', 'P', 'SNE', 'CMCSA', 'SONO', 'WWE', 'SSC', 'UMC', 'YY', 'MCHP', 'FOXA', 'LPL', 'EVLV', 'AAOI', 'PRKR', 'HLIT', 'BIP', 'MANU', 'HAS', 'FOX', 'WIN', 'PI', 'CNET', 'KCAP', 'VIAB', 'ERIC', 'AMT', 'PETS', 'DISCA', 'VOD', 'GDDY', 'CRNT', 'DISH', 'CAMT', 'VSH', 'CCI', 'SJR', 'BDR', 'CBS', 'SEAC', 'FLEX', 'ADI', 'CHL', 'SPEX', 'CREE', 'RESN', 'SIGM', 'EVC', 'CNSL', 'QRVO', 'OSK', 'SIMO', 'EROS', 'TIVO', 'TCCO', 'HRS', 'LGF.A', 'UONE', 'SBGI', 'AMCN', 'VOXX', 'ATUS', 'IDSY', 'DHXM', 'DISCK', 'KMX', 'SQNS', 'CHTR', 'AMCX', 'VRSN', 'UONEK', 'ETM', 'NWSA', 'VIA', 'RLJE', 'BT', 'TGNA', 'ULBI', 'SALM', 'AHC', 'MSN', 'XPER', 'NLS', 'WOW', 'KEYS', 'GSUM', 'BATRA', 'MXL', 'CSSE', 'GTN', 'TU', 'ROP', 'NWS', 'MDP', 'LGF.B', 'CIDM', 'VEON', 'XOXO', 'MSG', 'INVE', 'FWONA', 'VIV', 'MTSI', 'WTT', 'FENG', 'NOVT', 'ARRS', 'CETV', 'COMM', 'DGII', 'AKTS', 'BCE', 'LBTYA', 'CALX', 'MRCY', 'BBGI', 'FWONK', 'LSXMA', 'SBAC', 'HCHC', 'CBB', 'KT', 'BATRK', 'LSXMK', 'FANZ', 'LBTYK', 'SSP', 'TRK', 'NNI', 'TSQ', 'AEY', 'TRCO', 'OTEL', 'LILAK', 'NXST', 'CNO', 'BKTI', 'EMMS', 'NTN', 'AVT', 'GRVY', 'BCOM', 'LORL', 'LILA', 'HMTV', 'RCI', 'LIVX', 'PKE', 'PNTR', 'TLK', 'TV', 'BDC', 'KVHI', 'ISCA', 'AMX', 'REX', 'UEIC', 'GHC', 'NPSNY', 'CBS.A', 'DISCB', 'MIELY', 'TLSNY', 'PDYPY', 'CMLS', 'SGA', 'AMOV', 'CABO', 'SMGZY', 'LSXMB', 'SGAPY', 'AACAY', 'SCMWY', 'PBSFY', 'MBT', 'TEF', 'SKYAY', 'ORAN', 'ITVPY', 'TELNY', 'KAP', 'LBTYB', 'GTN.A', 'CSSEP', 'KCAPL', 'BDC-B', 'OIBR.C']
wireless 						= ['FIT', 'T', 'INTC', 'S', 'CSCO', 'VZ', 'CY', 'QCOM', 'TMUS', 'BB', 'SONO', 'AVGO', 'WATT', 'TSM', 'GSAT', 'XGTI', 'GOGO', 'HON', 'ON', 'AAOI', 'PRKR', 'NIHD', 'I', 'IRDM', 'WSTL', 'EXTR', 'FNSR', 'SWIR', 'AMT', 'SUN', 'VOD', 'RSYS', 'CRNT', 'TER', 'DISH', 'CCI', 'SJR', 'FLEX', 'UBNT', 'HIVE', 'CHL', 'BEAT', 'SPEX', 'MTZ', 'SCON', 'RBBN', 'ALRM', 'CNSL', 'QRVO', 'LSCC', 'WIFI', 'RFIL', 'HRS', 'SMSI', 'UTSI', 'VOXX', 'IDSY', 'IDTI', 'ZAYO', 'QTNA', 'SQNS', 'CHTR', 'TCX', 'IDCC', 'EMKR', 'AIRG', 'PCTI', 'TPVG', 'ZTCOY', 'LMRK', 'ORBC', 'SIEB', 'MXL', 'TU', 'TRMB', 'TKC', 'SLAB', 'VECO', 'VEON', 'LLIT', 'SMTC', 'WTT', 'ARRS', 'COMM', 'DGII', 'BCE', 'KONE', 'SBAC', 'BNSO', 'DCMYY', 'CBB', 'TESS', 'CLS', 'KT', 'TNAV', 'OCC', 'ARCW', 'EVOL', 'TSU', 'LILAK', 'CEL', 'SCSC', 'GLIBA', 'TDY', 'SHEN', 'BKTI', 'SPOK', 'GEOS', 'AGYS', 'TDS', 'LILA', 'RCI', 'KYOCY', 'KF', 'DSPG', 'ITRN', 'VMI', 'USM', 'AMX', 'PDVW', 'AVNW', 'IMASY', 'MTNOY', 'ATNI', 'PTNR', 'PHI', 'MIELY', 'VDMCY', 'AMOV', 'GLIBP', 'CABO', 'MNDO', 'KDDIY', 'MBT', 'VZA', 'TDE', 'UZC', 'MAGS', 'CTY', 'CNTF', 'CBB-B', 'UZA', 'BOSC', 'CTDD', 'CTAA', 'UZB', 'LMRKN', 'LMRKO', 'TDA', 'CTZ', 'TDJ', 'TDI', 'BRQS', 'TBB', 'LMRKP', 'CCI-A', 'SKM', 'TPVY', 'CTBB', 'IRDMB', 'CTV']
digital_television 				= ['T', 'VZ', 'WIN', 'VOD', 'CHL', 'CNSL', 'AMCN', 'VOXX', 'BT', 'BCE', 'KT', 'RCI', 'AMX', 'AMOV', 'TEF', 'ORAN']
television 						= ['AAPL', 'NFLX', 'AMZN', 'DIS', 'T', 'IQ', 'ROKU', 'VZ', 'SNE', 'CMCSA', 'GLW', 'WWE', 'SSC', 'OLED', 'FOXA', 'LPL', 'EVLV', 'AAOI', 'HLIT', 'HAS', 'FOX', 'WIN', 'CNET', 'VIAB', 'ERIC', 'PETS', 'DISCA', 'VOD', 'GDDY', 'DISH', 'SJR', 'BDR', 'CBS', 'SEAC', 'CHL', 'SIGM', 'EVC', 'CNSL', 'OSK', 'EROS', 'TIVO', 'LGF.A', 'UONE', 'SBGI', 'AMCN', 'VOXX', 'ATUS', 'DHXM', 'DISCK', 'KMX', 'CHTR', 'AMCX', 'VRSN', 'UONEK', 'VIA', 'RLJE', 'BT', 'TGNA', 'NLS', 'WOW', 'GSUM', 'BATRA', 'CSSE', 'GTN', 'TU', 'MDP', 'LGF.B', 'CIDM', 'VEON', 'XOXO', 'FWONA', 'VIV', 'FENG', 'ARRS', 'CETV', 'COMM', 'BCE', 'LBTYA', 'CALX', 'FWONK', 'LSXMA', 'HCHC', 'CBB', 'KT', 'BATRK', 'LSXMK', 'LBTYK', 'SSP', 'NNI', 'AEY', 'TRCO', 'OTEL', 'LILAK', 'NXST', 'CNO', 'GRVY', 'BCOM', 'LORL', 'LILA', 'HMTV', 'RCI', 'TLK', 'TV', 'BDC', 'KVHI', 'AMX', 'REX', 'GHC', 'NPSNY', 'CBS.A', 'DISCB', 'MIELY', 'SGA', 'AMOV', 'CABO', 'LSXMB', 'SGAPY', 'SCMWY', 'PBSFY', 'MBT', 'TEF', 'SKYAY', 'ORAN', 'ITVPY', 'LBTYB', 'GTN.A', 'CSSEP', 'BDC-B', 'OIBR.C']
electronics = []  # large inline historical test dataset removed
radio 							= ['SIRI', 'P', 'SONO', 'UMC', 'MCHP', 'PRKR', 'PI', 'ERIC', 'AMT', 'CRNT', 'CAMT', 'VSH', 'CBS', 'FLEX', 'ADI', 'SPEX', 'CREE', 'RESN', 'EVC', 'QRVO', 'SIMO', 'TCCO', 'HRS', 'UONE', 'SBGI', 'VOXX', 'IDSY', 'SQNS', 'UONEK', 'ETM', 'ULBI', 'SALM', 'MSN', 'XPER', 'KEYS', 'MXL', 'ROP', 'MSG', 'INVE', 'FWONA', 'MTSI', 'WTT', 'NOVT', 'DGII', 'AKTS', 'BCE', 'MRCY', 'BBGI', 'FWONK', 'LSXMA', 'SBAC', 'LSXMK', 'SSP', 'TRK', 'TSQ', 'LILAK', 'BKTI', 'EMMS', 'AVT', 'BCOM', 'LILA', 'RCI', 'LIVX', 'PKE', 'PNTR', 'TV', 'ISCA', 'REX', 'UEIC', 'CBS.A', 'CMLS', 'SGA', 'SMGZY', 'LSXMB', 'AACAY']
automotive 						= ['F', 'GE', 'TSLA', 'NVDA', 'MU', 'BRK.B', 'GM', 'CY', 'FCAU', 'BP', 'STM', 'HMC', 'HON', 'ON', 'MVIS', 'ALLY', 'CRUS', 'ARNC', 'KEM', 'WPRT', 'TM', 'TTM', 'APTV', 'WKHS', 'SINA', 'UQM', 'GGB', 'GT', 'HBAN', 'NEON', 'SWIR', 'KCAP', 'DLPH', 'CDTI', 'RENN', 'SORL', 'CVGI', 'CMI', 'HTZ', 'IEP', 'FLEX', 'FITB', 'UNP', 'TRUE', 'MET', 'GNTX', 'JCI', 'HUN', 'ITW', 'IMMR', 'CARG', 'CPRT', 'MXIM', 'XONE', 'MMLP', 'OSK', 'KIQ', 'TSEM', 'TRV', 'MGA', 'LSCC', 'XCRA', 'ICL', 'AVX', 'POAHY', 'FAST', 'BWA', 'RACE', 'VWAGY', 'VOXX', 'LKQ', 'IDTI', 'SHW', 'JBL', 'CNI', 'CZZ', 'PII', 'WGO', 'AAP', 'PRTS', 'LEG', 'DAN', 'BMWYY', 'QRHC', 'CLMT', 'JASNW', 'BBDC', 'NSC', 'MTOR', 'JEC', 'SRI', 'JEF', 'ATHM', 'GPN', 'GPC', 'LEA', 'LAD', 'JASN', 'SNA', 'FUJHY', 'AXL', 'XPER', 'KEYS', 'NAV', 'CTB', 'PPG', 'TEL', 'AN', 'VLY', 'CARS', 'ALV', 'CASY', 'SLAB', 'ADNT', 'CECE', 'MOD', 'PAG', 'ORLY', 'OIIM', 'MPWR', 'AZO', 'VVV', 'HIG', 'AUTO', 'CPSH', 'FHB', 'INFO', 'MPAA', 'KINS', 'HZN', 'WNS', 'MCY', 'PAHC', 'GSIT', 'UTI', 'OBCI', 'HHS', 'NSANY', 'LINC', 'ATLC', 'TEN', 'MEI', 'UFAB', 'CAAS', 'LFUS', 'SYPR', 'TNAV', 'VC', 'KAR', 'ESND', 'GTS', 'CXDC', 'VNE', 'CACC', 'CDK', 'NGVT', 'FOE', 'NNBR', 'VLVLY', 'RYCEY', 'KALU', 'WOR', 'AIT', 'CPSS', 'AMOT', 'ROG', 'SUP', 'NGHC', 'CATY', 'SYNL', 'CTS', 'AFH', 'ALOT', 'ITT', 'SHLO', 'GATX', 'SMP', 'SAH', 'THRM', 'THG', 'FNHC', 'PFIN', 'PNTR', 'CRMT', 'KMPR', 'KFS', 'CANG', 'WFC-J*', 'KRA', 'PTSI', 'FCB', 'SLGN', 'NICK', 'ASH', 'TG', 'ODC', 'QADA', 'CMT', 'GPI', 'TOWR', 'ABG', 'IX', 'BRDCY', 'GM+B', 'FRSX', 'GKNLY', 'WBC', 'DORM', 'LDL', 'CPS', 'ACNB', 'GELYY', 'STRT', 'HMN', 'MNRO', 'IBOC', 'EML', 'LAWS', 'UFPT', 'VLY+', 'WFC+', 'PKOH', 'PTVCA', 'QADB', 'RM', 'IOSP', 'MIELY', 'PTVCB', 'KE', 'TS', 'PBSK', 'WEICY', 'DIT', 'GLBZ', 'CNFR', 'ALD', 'SIM', 'DNZOY', 'CTTAY', 'BCAUY', 'CFFI', 'IFNNY', 'APELY', 'FMBH', 'CDNAF', 'BRK.A', 'NODK', 'KAP', 'GMTA', 'VLY-A', 'CATYW', 'HBK', 'ARNC-', 'WFC-N', 'WFC-P', 'WFC-O', 'HBANN', 'MET-A', 'WFC-Q', 'CSTM', 'WFC-V', 'THGA', 'WFC-T', 'NGHCZ', 'HGH', 'WFC-R', 'LIMAF', 'WFC-W', 'NGHCO', 'BAP', 'WFC-X', 'FITBI', 'NGHCN', 'KCAPL', 'KMPA', 'NGHCP', 'JMHLY', 'WFC-Y', 'LIQT', 'HIG+', 'VLY-B', 'HBANO']
transportation = []  # large inline historical test dataset removed
computer_networking 			= ['MU', 'INTC', 'CSCO', 'ANET', 'PANW', 'EXTR', 'FNSR', 'NEON', 'ERIC', 'FTNT', 'HIVE', 'JNPR', 'INFN', 'SMCI', 'LTRX', 'INSG', 'NTGR', 'CIEN', 'RDWR', 'PCTI', 'FFIV', 'DGII', 'SNX', 'ELON', 'ADTN', 'SILC', 'AEY', 'AVT', 'ALLT', 'BOSC']
telecommunications 				= ['AAPL', 'NFLX', 'T', 'INTC', 'SIRI', 'S', 'CSCO', 'VZ', 'NOK', 'SNE', 'CY', 'QCOM', 'CMCSA', 'TMUS', 'LMT', 'BB', 'SONO', 'CTL', 'AVGO', 'FTR', 'WATT', 'TEUM', 'TSM', 'KTOS', 'GSAT', 'XGTI', 'NOC', 'RHT', 'GOGO', 'HON', 'ON', 'SO', 'FOXA', 'BBOX', 'EVLV', 'GLOW', 'LPTH', 'OHGI', 'SGH', 'AAOI', 'SWCH', 'UNIT', 'PRKR', 'NIHD', 'HLIT', 'I', 'TM', 'IRDM', 'FOX', 'WIN', 'WSTL', 'GRMN', 'EXTR', 'FNSR', 'CIG', 'IPGP', 'SWIR', 'ABIL', 'KCAP', 'LUNA', 'ERIC', 'AMT', 'LITE', 'SUN', 'VOD', 'RSYS', 'CRNT', 'TER', 'DISH', 'CCI', 'SJR', 'VG', 'BDR', 'SEAC', 'FLEX', 'UBNT', 'HIVE', 'CHL', 'BEAT', 'SPEX', 'MTZ', 'CCIH', 'AETI', 'CPAH', 'ENT', 'ACIA', 'MXIM', 'SCON', 'RBBN', 'ALRM', 'INFN', 'CNSL', 'CASA', 'QRVO', 'HEI', 'APTI', 'LSCC', 'CONE', 'TCCO', 'WIFI', 'RFIL', 'HRS', 'SMSI', 'MLNX', 'NTIP', 'GECC', 'SBGI', 'ALSK', 'UTSI', 'VOXX', 'ATUS', 'RMGN', 'AUDC', 'IDSY', 'IDTI', 'JBL', 'ZAYO', 'MSI', 'QTNA', 'CIEN', 'SQNS', 'CHTR', 'TCX', 'CHKP', 'VRSN', 'KN', 'IDCC', 'GTT', 'EMKR', 'SFTBY', 'APH', 'BT', 'DY', 'AIRG', 'PCTI', 'ITI', 'TPVG', 'CMTL', 'VSAT', 'ZTCOY', 'MITL', 'LMRK', 'MAXR', 'WOW', 'ORBC', 'FSNN', 'SIEB', 'BATRA', 'MXL', 'TEO', 'CHU', 'ELP', 'TU', 'TRMB', 'PWR', 'TKC', 'SLAB', 'VECO', 'VEON', 'EPAM', 'LLIT', 'SMTC', 'FWONA', 'VIV', 'WTT', 'OOMA', 'ARRS', 'HEI.A', 'COMM', 'DGII', 'AKTS', 'IDT', 'CPSH', 'BCE', 'LBTYA', 'CALX', 'JCS', 'KONE', 'FWONK', 'LSXMA', 'SBAC', 'SATS', 'HCHC', 'BNSO', 'DCMYY', 'MEI', 'CBB', 'TESS', 'CLS', 'KT', 'IGLD', 'EXFO', 'IYZ', 'TNAV', 'BATRK', 'LSXMK', 'TGS', 'OCC', 'PLT', 'FTNW', 'ADTN', 'RNET', 'LBTYK', 'ARCW', 'VCRA', 'ENS', 'NNI', 'CLRO', 'AGM', 'EVOL', 'AEY', 'CHA', 'TSU', 'OTEL', 'LILAK', 'CEL', 'SCSC', 'CHT', 'NXST', 'GLIBA', 'AXE', 'TDY', 'APWC', 'LOOP', 'HALL', 'SHEN', 'BKTI', 'AVYA', 'NTCT', 'BCOM', 'IEX', 'DZSI', 'CCOI', 'LORL', 'IXP', 'SPOK', 'GEOS', 'ALOT', 'CSWC', 'AGYS', 'LBRDK', 'TDS', 'HUBB', 'LILA', 'RCI', 'KYOCY', 'CVG', 'PNTR', 'KF', 'DSPG', 'ITRN', 'TLK', 'VMI', 'GPX', 'TV', 'BDC', 'USM', 'KVHI', 'DAVA', 'NTTYY', 'AMX', 'PDVW', 'AVNW', 'DTEGY', 'IMASY', 'HTHIY', 'MTNOY', 'ATNI', 'AVAL', 'LBRDA', 'PTNR', 'PHI', 'MIELY', 'CKHUY', 'PLPC', 'TLSNY', 'VDMCY', 'AMOV', 'GLIBP', 'CABO', 'SUHJY', 'MNDO', 'LTL', 'LSXMB', 'SGAPY', 'SPKKY', 'AGM.A', 'CIG.C', 'SCMWY', 'KDDIY', 'MBT', 'TEF', 'VZA', 'SKYAY', 'TDE', 'UZC', 'ORAN', 'MAGS', 'TELNY', 'CTY', 'TI.A', 'CNTF', 'KAP', 'CBB-B', 'UZA', 'BOSC', 'AGM-C', 'AGM-B', 'CSWCL', 'CTDD', 'LBTYB', 'CTAA', 'UZB', 'LMRKN', 'LMRKO', 'AGM-A', 'TI', 'GECCL', 'TDA', 'SOMLY', 'CTZ', 'TDJ', 'TDI', 'BRQS', 'TBB', 'MTSL', 'LMRKP', 'NVMM', 'CCI-A', 'KCAPL', 'BDC-B', 'GILT', 'OIBR.C', 'SKM', 'TPVY', 'GECCM', 'CTBB', 'IRDMB', 'CTV']
upcoming_earnings 				= ['YEXT', 'NTNX', 'AOBC', 'LULU', 'PDD', 'ZUO', 'DG', 'AMBA', 'DLTR', 'ULTA', 'CPB', 'ANF', 'TD', 'SIG', 'MIK', 'BURL', 'BIG', 'CIEN', 'PDCO', 'TECD', 'ZLAB', 'GOGL', 'RUBY', 'TITN', 'GMS', 'MEI', 'COO', 'HOFT', 'EHIC', 'PERY', 'CANG', 'KEN', 'ITRN', 'BFRA', 'PAGS']
computer_hardware 				= ['AAPL', 'MSFT', 'SNE', 'HPQ', 'ORCL', 'IRM', 'WDC', 'HPE', 'STX', 'LOGI', 'PSTG', 'ITUS', 'QTM', 'NTAP', 'DVMT', 'COOL', 'AVID', 'IMMR', 'BCLI', 'SYNA', 'CHKP', 'NCR', 'ITI', 'ZBRA', 'VECO', 'QBAK', 'CRAY', 'TECD', 'PCMI', 'TDC', 'DGII', 'PAR', 'SCKT', 'ESND', 'QUMU', 'LINK', 'EFII', 'ICAD', 'SANM', 'CSPI', 'ALOT', 'OSS']
road_transportation 			= ['F', 'TSLA', 'PLUG', 'BRK.B', 'GM', 'CAT', 'FCAU', 'HMC', 'HON', 'XPO', 'MVIS', 'ALLY', 'CRUS', 'ARNC', 'CSX', 'TM', 'TTM', 'APTV', 'WKHS', 'SINA', 'UQM', 'GGB', 'DE', 'GT', 'HBAN', 'NEON', 'SWIR', 'KCAP', 'DLPH', 'CDTI', 'RENN', 'HOG', 'BKEP', 'SORL', 'CVGI', 'CMI', 'HTZ', 'IEP', 'FLEX', 'FITB', 'UNP', 'TRUE', 'MET', 'GNTX', 'KNDI', 'JCI', 'HUN', 'SINO', 'ITW', 'IMMR', 'CARG', 'CPRT', 'MXIM', 'XONE', 'FUV', 'MMLP', 'OSK', 'KIQ', 'TSEM', 'KNX', 'CEQP', 'TRV', 'MGA', 'LSCC', 'XCRA', 'ICL', 'CAR', 'AVX', 'POAHY', 'FAST', 'BWA', 'RACE', 'VWAGY', 'VOXX', 'SNDR', 'LKQ', 'IDTI', 'SHW', 'JBL', 'CNI', 'CZZ', 'PII', 'WGO', 'AAP', 'PRTS', 'LEG', 'DAN', 'BMWYY', 'QRHC', 'DSKE', 'CLMT', 'JASNW', 'BBDC', 'NSC', 'MTOR', 'JEC', 'USX', 'SRI', 'JEF', 'ATHM', 'GPN', 'YRCW', 'GPC', 'LEA', 'LAD', 'JASN', 'SNA', 'FUJHY', 'ODFL', 'AXL', 'JBHT', 'BAS', 'MZDAY', 'XPER', 'KEYS', 'NAV', 'CTB', 'PPG', 'TEL', 'AN', 'VLY', 'CARS', 'ALV', 'CELP', 'CASY', 'SLAB', 'ADNT', 'CECE', 'MOD', 'PAG', 'ORLY', 'ANDX', 'REVG', 'OIIM', 'MPWR', 'WERN', 'AZO', 'VVV', 'HIG', 'AUTO', 'USAK', 'CPSH', 'FHB', 'CVTI', 'INFO', 'MPAA', 'KINS', 'HZN', 'WNS', 'MCY', 'PAHC', 'GSIT', 'UTI', 'ARCB', 'OBCI', 'SRLP', 'HHS', 'NSANY', 'LINC', 'ATLC', 'TEN', 'MEI', 'UFAB', 'CAAS', 'LFUS', 'SYPR', 'TNAV', 'VC', 'MRTN', 'KAR', 'ESND', 'GTS', 'DMLRY', 'CXDC', 'VNE', 'SBNY', 'CACC', 'CDK', 'EEQ', 'NGVT', 'FOE', 'NNBR', 'VLVLY', 'RYCEY', 'KALU', 'WOR', 'AIT', 'ULH', 'CPSS', 'AMOT', 'ROG', 'LSTR', 'SUP', 'RUSHA', 'NGHC', 'CATY', 'SYNL', 'CTS', 'AFH', 'HTLD', 'ALOT', 'ITT', 'SHLO', 'GATX', 'SMP', 'SAIA', 'SAH', 'THRM', 'THG', 'FNHC', 'PFIN', 'PNTR', 'CRMT', 'KMPR', 'KFS', 'CANG', 'WFC-J*', 'KRA', 'PTSI', 'FCB', 'AMSF', 'SLGN', 'CMCO', 'NICK', 'ASH', 'TG', 'ODC', 'QADA', 'CMT', 'PARR', 'GPI', 'TOWR', 'ABG', 'IX', 'BRDCY', 'GM+B', 'FRSX', 'GKNLY', 'WBC', 'DORM', 'BH', 'LDL', 'CPS', 'ACNB', 'GELYY', 'STRT', 'HMN', 'MNRO', 'IBOC', 'EML', 'LAWS', 'UFPT', 'VLY+', 'WFC+', 'PKOH', 'PTVCA', 'QADB', 'RM', 'IOSP', 'MIELY', 'PTVCB', 'KE', 'TS', 'PBSK', 'WEICY', 'DIT', 'GLBZ', 'CNFR', 'ALD', 'SIM', 'CTTAY', 'RUSHB', 'SZKMY', 'BCAUY', 'CFFI', 'DSDVY', 'FMBH', 'BRK.A', 'NODK', 'KAP', 'GMTA', 'VLY-A', 'BH.A', 'SOLOW', 'SBNYW', 'CATYW', 'BKEPP', 'HBK', 'ARNC-', 'WFC-N', 'WFC-P', 'WFC-O', 'HBANN', 'MET-A', 'WFC-Q', 'CSTM', 'WFC-V', 'THGA', 'WFC-T', 'NGHCZ', 'DSKEW', 'HGH', 'WFC-R', 'LIMAF', 'WFC-W', 'NGHCO', 'BAP', 'WFC-X', 'FITBI', 'NGHCN', 'KCAPL', 'KMPA', 'NGHCP', 'JMHLY', 'WFC-Y', 'PATI', 'LIQT', 'HIG+', 'VLY-B', 'HBANO']
internet 						= ['FB', 'MSFT', 'TWTR', 'NFLX', 'BABA', 'SNAP', 'AMZN', 'T', 'IQ', 'INTC', 'S', 'JD', 'GOOGL', 'SHOP', 'CSCO', 'ROKU', 'VZ', 'GOOG', 'SPOT', 'BILI', 'P', 'BIDU', 'BZUN', 'CMCSA', 'WB', 'SONO', 'MTCH', 'EBAY', 'EA', 'NXTD', 'SOGO', 'CTL', 'FTR', 'OSTK', 'YEXT', 'TEUM', 'SSC', 'MOMO', 'TDOC', 'LLNW', 'YY', 'TCEHY', 'GRUB', 'APPS', 'GOGO', 'FDN', 'TRVG', 'FOXA', 'YELP', 'OHGI', 'MOSY', 'EGAN', 'AAOI', 'ZIXI', 'WIX', 'W', 'NTES', 'NETE', 'UNIT', 'MEET', 'HLIT', 'FOX', 'SINA', 'WIN', 'ZS', 'XNET', 'VIPS', 'MELI', 'SWIR', 'SIFY', 'UXIN', 'KWEB', 'CNET', 'TAOP', 'ERIC', 'RENN', 'MB', 'VOD', 'GDDY', 'TPR', 'SJR', 'VG', 'EMQQ', 'YRD', 'AKAM', 'SNSR', 'CBS', 'BITA', 'TD', 'STMP', 'CHL', 'TRUE', 'CAMP', 'FLWS', 'LKM', 'CCIH', 'RUBI', 'AMTD', 'OGIG', 'ENT', 'CARG', 'CPRT', 'SFUN', 'NTRI', 'CNSL', 'QRVO', 'LTRX', 'STCN', 'IAC', 'JMEI', 'SITO', 'CMCM', 'YNDX', 'VHC', 'RYAAY', 'WUBA', 'TTGT', 'WIFI', 'HES', 'SE', 'ALL', 'PTC', 'LOGM', 'SMSI', 'CWEB', 'ALSK', 'EVBG', 'RMBS', 'PNQI', 'AUDC', 'IDTI', 'EQIX', 'BUZ', 'NOAH', 'NTGR', 'DHX', 'ATV', 'ANGI', 'PRTS', 'CHTR', 'CYOU', 'TCX', 'INUV', 'CHKP', 'VRSN', 'PFSW', 'GTT', 'MMYT', 'BAND', 'SFTBY', 'ATHM', 'EGHT', 'BT', 'SOHU', 'PRSS', 'GWW', 'PCTI', 'CDLX', 'ZION', 'VSAT', 'NXTDW', 'VNET', 'MBTF', 'EVER', 'XWEB', 'NLS', 'WOW', 'SHSP', 'KEYS', 'FSNN', 'LEJU', 'TEO', 'EGOV', 'CHU', 'GTN', 'LPSN', 'SFLY', 'SPRT', 'CARS', 'IPDN', 'TU', 'FTD', 'EDUC', 'SLAB', 'VEON', 'LEAF', 'XOXO', 'LOB', 'LITB', 'TZOO', 'SOFO', 'INAP', 'VIV', 'MTSI', 'DTRM', 'FENG', 'ECOM', 'OOMA', 'CIFS', 'ARRS', 'CEVA', 'DGII', 'JOBS', 'CPSH', 'YGYI', 'BCE', 'LE', 'LBTYA', 'SSTK', 'MTB', 'JCOM', 'RNWK', 'CYRN', 'BCOV', 'CSGP', 'BCOR', 'SEIC', 'HCHC', 'IIJI', 'CBB', 'KT', 'IGLD', 'MCHX', 'DOX', 'ELON', 'RNET', 'LBTYK', 'NNI', 'CHA', 'SECO', 'TSU', 'OTEL', 'LILAK', 'CEL', 'FCF', 'CHT', 'XRF', 'RKUNY', 'OMF', 'EHTH', 'CNO', 'CSFL', 'YAHOY', 'MSTR', 'BVSN', 'RFL', 'SHEN', 'INBK', 'LCUT', 'EDGW', 'WEB', 'GRVY', 'BCOM', 'HOFT', 'MCBC', 'GEC', 'WHLM', 'CCOI', 'PRFT', 'JG', 'FIBK', 'COE', 'LILA', 'RCI', 'LIVX', 'AMBO', 'CNXN', 'KF', 'BKSC', 'TLK', 'EXPGY', 'BDC', 'USM', 'TRCB', 'KVHI', 'LBAI', 'NTTYY', 'FBK', 'AMX', 'PPBI', 'PKBK', 'HBMD', 'RBCAA', 'MTNOY', 'PTNR', 'FGBI', 'NPSNY', 'PGC', 'WASH', 'MBWM', 'CBS.A', 'ASOMY', 'PHI', 'PB', 'AMOV', 'MSL', 'CRTO', 'CABO', 'HWBK', 'MNDO', 'ZIONW', 'ZIONZ', 'SPKKY', 'MBT', 'TEF', 'UZC', 'ORAN', 'RTMVY', 'BRK.A', 'TI.A', 'ZB-G', 'CBB-B', 'UZA', 'ALL-D', 'ALL-E', 'TKAT', 'ALL-B', 'ZB-H', 'MTB+', 'LBTYB', 'MTB-C', 'ZB-A', 'ZBK', 'UZB', 'MTB-', 'TI', 'GTN.A', 'MOXC', 'ALL-A', 'TBB', 'CCRC', 'ALL-C', 'BDC-B', 'ALL-F', 'GILT', 'OIBR.C', 'SKM', 'HES-A', 'INBKL']
material = []  # large inline historical test dataset removed
integrated_circuit 				= ['INTC', 'AMAT', 'QCOM', 'LRCX', 'STM', 'TXN', 'TSM', 'HIMX', 'MRVL', 'ON', 'KEM', 'ASX', 'KLAC', 'TTMI', 'XPER', 'NAV', 'INVE', 'VSM', 'CCMP', 'RUSHA', 'KEN', 'RUSHB', 'NAV-D', 'MX']
asia_non_china 					= ['IGC', 'TSM', 'NSPR', 'LPL', 'RWLK', 'WIX', 'NTEC', 'INFY', 'TRPX', 'TM', 'TTM', 'SSYS', 'SIFY', 'ABIL', 'INDA', 'IBN', 'NNDM', 'CRNT', 'CAMT', 'PLX', 'FLEX', 'CYBR', 'KTOV', 'CHEK', 'EWJ', 'WIT', 'MUFG', 'GLMD', 'TSEM', 'INDY', 'LN', 'CAJ', 'TUR', 'VBLT', 'VNM', 'NMR', 'ICL', 'SE', 'ANFI', 'EWY', 'ATTU', 'MLNX', 'SODA', 'EPI', 'HDB', 'AUDC', 'RDHL', 'MFG', 'SMIN', 'CHKP', 'KRNT', 'RDWR', 'SPCB', 'MMYT', 'DXJ', 'HQCL', 'INDL', 'EWS', 'MGIC', 'NVMI', 'SMFG', 'KSA', 'APOP', 'CGEN', 'TKC', 'SCIF', 'ORMP', 'PAK', 'ORBK', 'ITEQ', 'PIN', 'BLRX', 'INXX', 'RDY', 'FOMX', 'ESLT', 'IZRL', 'VNRX', 'KORU', 'URGN', 'AAXJ', 'INCO', 'WNS', 'EWM', 'CYRN', 'ASLN', 'EPHE', 'EIDO', 'IIJI', 'DCMYY', 'IFN', 'KT', 'AZRE', 'IGLD', 'STDY', 'HEWJ', 'SCIN', 'SILC', 'DFJ', 'BVXV', 'ELTK', 'NICE', 'DBJP', 'CEL', 'FXY', 'CSTE', 'CANF', 'RDCM', 'ISRA', 'VEDL', 'EGPT', 'GRVY', 'BCOM', 'WVE', 'SCJ', 'MDWD', 'JPNL', 'TARO', 'BVXVW', 'IIF', 'KYOCY', 'BBJP', 'JOF', 'PNTR', 'KEN', 'ITRN', 'TLK', 'CALL', 'IDX', 'JPN', 'DXJS', 'TWN', 'NTTYY', 'ALLT', 'MDGS', 'IX', 'FRSX', 'GSJY', 'JEQ', 'DXJF', 'CHEKW', 'FLIN', 'PTNR', 'SCIJ', 'KB', 'FLKR', 'THFF', 'AXJV', 'PKX', 'NJDCY', 'PHI', 'JHDG', 'JPMV', 'HEWY', 'CLGN', 'FORTY', 'AXJL', 'FTEO', 'FJP', 'DBAP', 'SCIX', 'SHG', 'FLJP', 'MNDO', 'HFXJ', 'RADA', 'EZJ', 'EWV', 'FXSG', 'DEWJ', 'QJPN', 'PAF', 'DDJP', 'WF', 'FLTW', 'FLAX', 'FPA', 'FLJH', 'KEP', 'KTOVW', 'XTLB', 'PSTI', 'OTIV', 'MAGS', 'OBAS', 'CYD', 'THD', 'MDGSW', 'BOSC', 'NFTY', 'KMDA', 'EVGN', 'YTRA', 'ENTX', 'NSPR+B', 'CHEKZ', 'EIS', 'NSPR+', 'TATT', 'EWT', 'ORPN', 'ENTXW', 'FKO', 'EPP', 'KLIC', 'MTSL', 'APOPW', 'DBKO', 'SLGL', 'GZT', 'TISA', 'GILT', 'SKM', 'WILC', 'EMITF', 'ELLO']
engineering = []  # large inline historical test dataset removed
packaging 						= ['JNJ', 'PG', 'KODK', 'MMM', 'UPS', 'NWL', 'DWDP', 'FDX', 'ARNC', 'ASX', 'IP', 'KCAP', 'CAMT', 'CDMO', 'IEP', 'LCI', 'DEO', 'DSS', 'KOPN', 'ITW', 'GPK', 'MMLP', 'CYRX', 'STKL', 'SMI', 'WRK', 'HFC', 'KLAC', 'FAST', 'NANO', 'PETQ', 'SHW', 'JBL', 'PKG', 'BLL', 'AVY', 'XPER', 'PPG', 'ITP', 'AMKR', 'PAH', 'VECO', 'XSPL', 'QUAD', 'SON', 'SEE', 'BERY', 'OMCL', 'OI', 'FFHL', 'FN', 'IMOS', 'UFPI', 'ASIX', 'CLW', 'CCK', 'CTLT', 'KS', 'UFS', 'NDSN', 'DMRC', 'BMS', 'ECOL', 'EFII', 'LOOP', 'ALOT', 'GCP', 'INWK', 'GEF', 'MTD', 'CLH', 'POL', 'MYE', 'WST', 'KRA', 'MTRN', 'MLAB', 'SLGN', 'VRTV', 'TG', 'ATR', 'SPLP', 'FORR', 'NP', 'LNDC', 'UFPT', 'TRS', 'SPLP-A', 'UNF', 'SENEA', 'KE', 'SEOAY', 'AMCRY', 'GEF.B', 'SMFKY', 'CDMOP', 'KAP', 'ARNC-', 'CYRXW', 'CSTM', 'ARD', 'SENEB', 'NDEKY', 'KLIC', 'KCAPL']
metal 							= ['IGC', 'AUY', 'NAK', 'JNUG', 'AKS', 'X', 'DRYS', 'KGC', 'LODE', 'GLD', 'NUGT', 'IIPR', 'ABX', 'FCX', 'EGO', 'SLV', 'IAU', 'CLF', 'PLM', 'HL', 'GDX', 'AG', 'PCG', 'TMQ', 'PLG', 'WWR', 'TRX', 'ARNC', 'VALE', 'KEM', 'BTG', 'GSS', 'CGNX', 'TGB', 'UAMY', 'YUM', 'VGZ', 'GPL', 'AUMN', 'NUE', 'WSTL', 'GGB', 'GLBS', 'WRN', 'AKG', 'ENSV', 'GG', 'HMY', 'NGD', 'KCAP', 'ACN', 'USAU', 'AA', 'GSV', 'WPM', 'MUX', 'AQMS', 'DISCA', 'DNN', 'UEC', 'IAG', 'SBGL', 'CME', 'CREG', 'KGJI', 'UUUU', 'SUPV', 'DUST', 'CCJ', 'CENX', 'RGR', 'GOLD', 'NM', 'STLD', 'SAND', 'URG', 'CBAK', 'IEP', 'EXK', 'EGI', 'NEM', 'FSM', 'SGBX', 'GMO', 'GCAP', 'TRQ', 'CC', 'DS', 'DF', 'PAAS', 'SXCP', 'THM', 'RIO', 'EW', 'TIF', 'ALO', 'JDST', 'GDXJ', 'NSU', 'SID', 'CDE', 'UGLD', 'ZKIN', 'TAHO', 'URI', 'URA', 'STCN', 'DGSE', 'AU', 'VHI', 'RICK', 'UWN', 'GORO', 'NG', 'AGI', 'AIRI', 'ATI', 'AAU', 'AGG', 'TECK', 'MT', 'HBM', 'BHP', 'PPC', 'ATTU', 'UONE', 'ASM', 'PZG', 'REMX', 'KL', 'CNI', 'FLR', 'MICR', 'DISCK', 'FNV', 'BWEN', 'RGLD', 'SSRM', 'SLVO', 'CMC', 'LEG', 'GFI', 'SBLK', 'UONEK', 'BBDC', 'UTHR', 'FLL', 'GLDI', 'PATK', 'JEF', 'RLJE', 'BLL', 'FRTA', 'AXU', 'DY', 'ERI', 'PVG', 'USAS', 'KPTI', 'SCHN', 'BGG', 'PGLC', 'AEM', 'TRN', 'MSB', 'BYFC', 'SABR', 'SIVR', 'XME', 'OUNZ', 'PME', 'RMCF', 'SCCO', 'OSN', 'BC', 'NCS', 'BBL', 'SIL', 'CECE', 'PSLV', 'ACH', 'EMX', 'RING', 'TMST', 'HSC', 'PICK', 'SLVP', 'RS', 'EAF', 'SON', 'OR', 'SA', 'COPX', 'MAG', 'RYI', 'ZBH', 'SGOL', 'CHNR', 'TPC', 'COMM', 'FBHS', 'GNK', 'GLDM', 'ZEUS', 'KZMYY', 'FDP', 'GIL', 'SILJ', 'CALX', 'AGQ', 'PAHC', 'IMOS', 'IDSA', 'APOG', 'HCHC', 'JELD', 'GMS', 'MEI', 'GLTR', 'FRD', 'BRSS', 'KMT', 'IGLD', 'SYPR', 'LEU', 'GNT', 'CPER', 'OCC', 'NWPX', 'NXE', 'SLX', 'DBB', 'GOAU', 'SGDM', 'FOE', 'DSLV', 'WSO', 'ECOL', 'KALU', 'WOR', 'VEDL', 'AMRK', 'UGL', 'GOEX', 'GUNR', 'MTRX', 'USAP', 'SUP', 'IEX', 'SYNL', 'MOG.A', 'LII', 'NLR', 'INTL', 'HAYN', 'GDXX', 'SHLO', 'GATX', 'AP', 'GEF', 'CRS', 'KEQU', 'SGDJ', 'DZZ', 'SOUHY', 'DGLD', 'HELE', 'DGP', 'AZZ', 'SHNY', 'EE', 'KF', 'TX', 'VMI', 'GPX', 'LNN', 'MLI', 'GDXS', 'MTRN', 'GIFI', 'SLGN', 'IIIN', 'CMCO', 'TG', 'WIRE', 'DYY', 'CIX', 'NPO', 'GLNCY', 'BAR', 'SPLP', 'NHYDY', 'PLLL', 'LXFR', 'AWCMY', 'DGL', 'PSAU', 'NPK', 'FSUGY', 'DBP', 'RBC', 'BDD', 'OFLX', 'TRS', 'PKOH', 'SPLP-A', 'MTL-', 'PKX', 'BVN', 'DISCB', 'ZSL', 'DGZ', 'PLPC', 'EFFE', 'NILSY', 'UMICY', 'TS', 'GLL', 'SQM', 'SMN', 'IAUF', 'DBS', 'PMPT', 'RJZ', 'SIM', 'UYM', 'TTDKY', 'BOM', 'MTL', 'GEF.B', 'SLT', 'BOS', 'USV', 'NCMGY', 'UBG', 'FQVLF', 'SBM', 'DRD', 'HEBT', 'USLM', 'ITOCY', 'SVM', 'WSO.B', 'KAP', 'GMTA', 'JJPB', 'DS-C', 'JJMB', 'JJUB', 'SMTS', 'MS-F', 'MS-A', 'ARNC-', 'DS-D', 'MS-I', 'MS-K', 'DEENF', 'CSTM', 'ARD', 'TGLS', 'DDP', 'KMI-A', 'HL-B', 'MOG.B', 'MITSY', 'DS-B', 'UUUU+', 'KCAPL', 'NEXA', 'MS-G', 'JJCB']
us = []  # large inline historical test dataset removed
business_service = []  # large inline historical test dataset removed
north_america = []  # large inline historical test dataset removed
etf = []  # large inline historical test dataset removed
three_x_etf 					= ['JNUG', 'TQQQ', 'NUGT', 'SPXL', 'SOXL', 'DGAZ', 'UPRO', 'SQQQ', 'UDOW', 'DRIP', 'USLV', 'DWT', 'LABU', 'UWT', 'YINN', 'DUST', 'GUSH', 'TECL', 'SPXU', 'FAS', 'BRZU', 'SPXS', 'TZA', 'JDST', 'SDOW', 'FAZ', 'UGLD', 'TNA', 'LABD', 'GREK', 'CWEB', 'ERX', 'SOXS', 'GASL', 'NAIL', 'EDC', 'INDL', 'YANG', 'NGE', 'CURE', 'PAK', 'PSP', 'TECS', 'TMF', 'DRV', 'CORN', 'RUSL', 'GXG', 'TMV', 'URTY', 'KORU', 'DRN', 'SLY', 'SLYV', 'GASX', 'NIB', 'EDZ', 'RETL', 'UBOT', 'UDN', 'FINU', 'ERY', 'GVAL', 'RUSS', 'UBIO', 'SRTY', 'MDYG', 'DSLV', 'MIDU', 'EURL', 'WTIU', 'TYO', 'WCHN', 'JPNL', 'LBJ', 'YMLP', 'GMOM', 'DPST', 'DGLD', 'TTT', 'REK', 'PZI', 'VAMO', 'FINZ', 'CHIM', 'MIDZ', 'SPDN', 'UMDD', 'MDYV', 'FYLD', 'PHDG', 'GSSC', 'DZK', 'DNO', 'SMDD', 'KFYP', 'DBGR', 'SOVB', 'EWSC', 'TYD', 'UNL', 'WDRW', 'DPK', 'FUE', 'MLTI', 'OILX', 'CROP', 'WLDR', 'OVLU', 'EMBU', 'KURE', 'RODI']
aerospace 						= ['GE', 'BRK.B', 'BA', 'LMT', 'RTN', 'AAL', 'KTOS', 'NOC', 'GOGO', 'HON', 'ON', 'SGH', 'ARNC', 'UAL', 'KEM', 'IRDM', 'UQM', 'IEC', 'GD', 'PSX', 'GRMN', 'ITA', 'KCAP', 'UTX', 'PPA', 'RSYS', 'XAR', 'TER', 'TXT', 'IEP', 'AJRD', 'FLEX', 'DFEN', 'MIC', 'ABDC', 'WING', 'GNTX', 'ERJ', 'MICT', 'XONE', 'QRVO', 'HEI', 'ETN', 'AIRI', 'ATI', 'HRS', 'LLL', 'JBL', 'DK', 'LEG', 'RAVN', 'KN', 'FLL', 'SPR', 'JEC', 'BLL', 'COL', 'SNA', 'PH', 'HXL', 'ZNH', 'KEYS', 'PPG', 'TEL', 'OSIS', 'EADSY', 'TDG', 'BRS', 'NSYS', 'FTAI', 'TIK', 'CECE', 'MOC', 'WNC', 'ABM', 'AIR', 'AER', 'CVV', 'ESLT', 'CAE', 'HEI.A', 'CPSH', 'INFO', 'AAWW', 'CW', 'WAIR', 'INT', 'MEI', 'CLS', 'TGI', 'KMT', 'ENS', 'ATRO', 'AXS', 'TDY', 'AHL', 'NNBR', 'CSL', 'HALL', 'KALU', 'DCI', 'CR', 'RE', 'WSCI', 'AMOT', 'KLXI', 'RXN', 'ROG', 'GFF', 'IEX', 'DCO', 'WWD', 'MOG.A', 'CTS', 'ALOT', 'B', 'ITT', 'HAYN', 'CRS', 'ACGL', 'THG', 'ACY', 'BAESY', 'KAMN', 'GPX', 'FCB', 'AIN', 'ESL', 'SXI', 'PLXS', 'GKNLY', 'ESE', 'AIRT', 'TAYD', 'ROLL', 'RBC', 'IMASY', 'IKNX', 'SIF', 'UFPT', 'VSEC', 'TRS', 'CIR', 'ATRI', 'ALD', 'RADA', 'BRK.A', 'KAP', 'ACGLO', 'BOSC', 'RXN-A', 'ARNC-', 'CSTM', 'ACGLP', 'THGA', 'TATT', 'MOG.B', 'NVMM', 'KCAPL', 'AXS-E', 'IRDMB']
air_transportation 				= ['GE', 'BRK.B', 'BA', 'LUV', 'LMT', 'DAL', 'JBLU', 'RTN', 'BP', 'MYSZ', 'AAL', 'UPS', 'ALK', 'NOC', 'FDX', 'GOGO', 'HON', 'TRIP', 'SGH', 'ARNC', 'UAL', 'IRDM', 'UQM', 'IEC', 'GD', 'PSX', 'GRMN', 'ITA', 'KCAP', 'SAVE', 'UTX', 'PPA', 'RSYS', 'XSPA', 'XAR', 'TER', 'TXT', 'IEP', 'AJRD', 'BPL', 'FLEX', 'DFEN', 'MIC', 'ABDC', 'WING', 'GNTX', 'ERJ', 'HA', 'ENT', 'MICT', 'XONE', 'QRVO', 'OSK', 'RYAAY', 'HEI', 'WIFI', 'ETN', 'AIRI', 'ATI', 'GOL', 'HRS', 'SODA', 'DAKT', 'LLL', 'IDSY', 'JBL', 'SKYW', 'DK', 'LEG', 'RAVN', 'KN', 'H', 'JETS', 'FLL', 'SPR', 'JEC', 'ATSG', 'BLL', 'AL', 'COL', 'SNA', 'PH', 'AZUL', 'SABR', 'HXL', 'ZNH', 'KEYS', 'PPG', 'TEL', 'OSIS', 'EADSY', 'GVA', 'TDG', 'BRS', 'NSYS', 'FTAI', 'TIK', 'CECE', 'MOC', 'WNC', 'ANDX', 'CCO', 'ABM', 'AIR', 'AER', 'CVV', 'ESLT', 'CAE', 'HEI.A', 'ALGT', 'CPSH', 'BDRBF', 'INFO', 'AAWW', 'CEA', 'CW', 'CPA', 'WAIR', 'LAMR', 'INT', 'MEI', 'CLS', 'TGI', 'JBT', 'KMT', 'AVH', 'ENS', 'LTM', 'ATRO', 'AXS', 'VLRS', 'TDY', 'AHL', 'NNBR', 'CSL', 'HALL', 'KALU', 'DCI', 'CR', 'RE', 'WSCI', 'AMOT', 'KLXI', 'RXN', 'ROG', 'GFF', 'IEX', 'DCO', 'WWD', 'MOG.A', 'CTS', 'ALOT', 'B', 'ITT', 'HAYN', 'CRS', 'ACGL', 'PAC', 'THG', 'ACY', 'PRIM', 'BAESY', 'KAMN', 'GPX', 'FCB', 'AIN', 'ESL', 'SXI', 'PLXS', 'GKNLY', 'OMAB', 'ESE', 'AIRT', 'TAYD', 'ROLL', 'RBC', 'IKNX', 'SIF', 'UFPT', 'VSEC', 'TRS', 'ESYJY', 'CIR', 'DLAKY', 'ASR', 'ATRI', 'ALD', 'RADA', 'ICAGY', 'BRK.A', 'KAP', 'ACGLO', 'BOSC', 'YTRA', 'RXN-A', 'ARNC-', 'CSTM', 'ACGLP', 'THGA', 'TATT', 'CAAP', 'MOG.B', 'NVMM', 'KCAPL', 'JMHLY', 'AXS-E', 'IRDMB']
professional_service 			= ['OKTA', 'RTN', 'KODK', 'SYMC', 'ACN', 'SAIL', 'ACM', 'MCO', 'HII', 'PTC', 'LYTS', 'SCI', 'AUDC', 'ZAYO', 'ANGI', 'ENG', 'PFSW', 'JEC', 'GPN', 'TTEK', 'MGIC', 'UPLD', 'DRE', 'AZPN', 'MDRX', 'IQV', 'RHI', 'PDFS', 'HCSG', 'CACI', 'KFY', 'JLL', 'MMC', 'ASGN', 'EVTC', 'QSII', 'G', 'AON', 'FCN', 'STN', 'NCI', 'ICFI', 'CVG', 'PRO', 'FCB', 'ALLT', 'FORTY', 'FTEO', 'GILT']
investment_service = []  # large inline historical test dataset removed
cancer_prevention 				= ['GERN', 'INSY', 'ABBV', 'CELG', 'TDOC', 'CYTR', 'AVEO', 'IMUC', 'ATOS', 'EXEL', 'VSTM', 'IMGN', 'SRRA', 'SESN', 'IDXG', 'RNN', 'HEB', 'PRPO', 'CVM', 'ALT', 'AMGN', 'APTO', 'ARRY', 'AGEN', 'SRNE', 'HTBX', 'NVTA', 'CGIX', 'DVAX', 'PGNX', 'ONTX', 'AFMD', 'GALT', 'ISR', 'AEZS', 'GNCA', 'GENE', 'INO', 'EXAS', 'ITUS', 'VRTX', 'CLSN', 'IMMU', 'PIRS', 'SLS', 'AZN', 'BLUE', 'BTX', 'DMPI', 'MTP', 'DFFN', 'MEIP', 'ADXS', 'ONCS', 'INFI', 'NVCR', 'ZIOP', 'VTVT', 'HRTX', 'ECYT', 'IOVA', 'AEMD', 'KTOV', 'CHEK', 'MACK', 'FATE', 'CVM+', 'AGLE', 'CLRB', 'XBIO', 'CASI', 'ADAP', 'CYCC', 'SNDX', 'PBYI', 'AST', 'NLNK', 'BGNE', 'RCKT', 'BDX', 'TYME', 'CALA', 'VBLT', 'CLVS', 'NK', 'ADRO', 'IMMP', 'LOXO', 'MRTX', 'BTAI', 'NEO', 'RDHL', 'MGEN', 'CNCR', 'NH', 'IMDZ', 'UNM', 'TCON', 'SGEN', 'COLL', 'TPIV', 'KURA', 'TOCA', 'XBIT', 'RDUS', 'DGX', 'OCX', 'KPTI', 'OMED', 'NYMX', 'GHDX', 'GTXI', 'TRIL', 'CWBR', 'KZIA', 'FPRX', 'AGIO', 'ATNX', 'SYRS', 'CCXI', 'ALPN', 'CKPT', 'CTMX', 'VNRX', 'CSBR', 'GTHX', 'VCYT', 'URGN', 'XNCR', 'MRSN', 'MGNX', 'CBMG', 'RUBY', 'NTGN', 'CRVS', 'VAR', 'SURF', 'FTSV', 'ASLN', 'MBIO', 'DCPH', 'OASM', 'CANF', 'UMRX', 'CNST', 'CELC', 'ICAD', 'REPL', 'ODT', 'BYSI', 'OSIR', 'CLRBW', 'BTX+', 'NCNA', 'AUTL', 'ARGX', 'CHEKW', 'IMV', 'EDAP', 'ADXSW', 'ERYP', 'CLLS', 'KTOVW', 'ONTXW', 'GMXAY', 'UNMA', 'BDXA', 'CHEKZ', 'IMUC+', 'CYCCP', 'CLRBZ', 'CELGZ', 'EPIX']
data_service 					= ['INTC', 'DBX', 'VZ', 'TMUS', 'CTL', 'AVGO', 'IRM', 'PVTL', 'BBOX', 'VMW', 'FDC', 'AAOI', 'SWCH', 'ZEN', 'OCLR', 'EXTR', 'SIFY', 'CNET', 'LITE', 'NTAP', 'DLR', 'PMTS', 'CME', 'ADP', 'DXC', 'INFN', 'AQ', 'QRVO', 'PAYX', 'WYY', 'CONE', 'TRHC', 'FISV', 'CSLT', 'ZAYO', 'CIEN', 'NH', 'GPN', 'JTPY', 'QIWI', 'VNET', 'TSS', 'QTS', 'FIS', 'CDW', 'ATEN', 'TECD', 'TNET', 'ADS', 'EVTC', 'SNX', 'EEFT', 'SILC', 'INOV', 'INOD', 'MRIN', 'WEX', 'TYL', 'EXLS', 'CLGX', 'PCYG', 'RCI', 'OFC', 'CVG', 'SYKE', 'CSGS', 'ISDR', 'ATNI', 'SRVR', 'CASS', 'VZA', 'DLR-I', 'DLR-J', 'DLR-C', 'OPRX', 'CCRC', 'DLR-G', 'DLR-H']
outsourcing 					= ['MRVL', 'INFY', 'DRAD', 'ACN', 'CTSH', 'EFX', 'ADP', 'WIT', 'DXC', 'PAYX', 'UIS', 'STT', 'AMN', 'MGIC', 'FIS', 'EGOV', 'BCO', 'TU', 'SYNT', 'EPAM', 'SRT', 'TNET', 'JOBS', 'KELYA', 'WNS', 'KFY', 'SEIC', 'IIJI', 'GIB', 'EVTC', 'CRL', 'MAN', 'EEFT', 'VRTU', 'HSON', 'WLTW', 'AXE', 'G', 'TYL', 'VISI', 'ALJJ', 'PRFT', 'CIGI', 'NCI', 'TBI', 'BBSI', 'CVG', 'GPX', 'SYKE', 'TTEC', 'AHEXY', 'ATTO', 'BZLFY', 'STT-C', 'STT-E', 'CCRC', 'STT-G', 'KELYB', 'STT-D']
logistics 						= ['LMT', 'CAT', 'UPS', 'ETP', 'NOC', 'FDX', 'XPO', 'PBR', 'VALE', 'INFY', 'ETE', 'DLTR', 'VLO', 'PI', 'ANW', 'CTSH', 'ZTO', 'NM', 'FGP', 'BPL', 'FLEX', 'CLD', 'RLGT', 'OMI', 'CVEO', 'ACM', 'SXCP', 'PLD', 'SID', 'GMLP', 'RRD', 'CVRR', 'PAA', 'NGL', 'KNX', 'CYRX', 'RRTS', 'MPLX', 'CEQP', 'GOL', 'MT', 'EC', 'SNDR', 'FLR', 'CZZ', 'HOS', 'PBF', 'DK', 'SVU', 'PBR.A', 'PFSW', 'DSKE', 'ANDV', 'USX', 'BGSF', 'KBR', 'JBHT', 'SXC', 'WTTR', 'BCO', 'TRMB', 'TRGP', 'SYNT', 'PFGC', 'MOC', 'XSPL', 'LITB', 'ANDX', 'GLP', 'USDP', 'ECHO', 'HSC', 'CHRW', 'TECD', 'QUAD', 'WERN', 'EXPD', 'YRIV', 'USAK', 'MATX', 'CAI', 'CVTI', 'PBFX', 'DKL', 'VLP', 'VEC', 'CACI', 'ARW', 'SAIC', 'ARCB', 'DCP', 'INT', 'CLS', 'SNX', 'DSGX', 'UGP', 'EVK', 'WSC', 'EXLS', 'ULH', 'SANM', 'HUBG', 'LSTR', 'HOFT', 'DLHC', 'RELL', 'CSWC', 'TBI', 'GEF', 'SAIA', 'SEMG', 'CANG', 'PTSI', 'WCC', 'VRTV', 'PARR', 'CKH', 'SPLP', 'KTCC', 'WSFS', 'FWRD', 'OMAB', 'DXPE', 'SEB', 'VSEC', 'WARFY', 'PKOH', 'SPLP-A', 'CSUAY', 'GRAM', 'MIELY', 'DLAKY', 'ROYMY', 'IMBBY', 'DPSGY', 'GEF.B', 'DSDVY', 'BXBLY', 'NGL-B', 'ILPT', 'CSWCL', 'NM-G', 'CYRXW', 'PANL', 'DSKEW', 'MITSY', 'NM-H', 'CCRC', 'RLGT-A', 'NGLS-A']
most_popular_under_twenty_five 	= ['F', 'GE', 'FIT', 'GPRO', 'CRON', 'SNAP', 'CHK', 'ZNGA', 'SIRI', 'GRPN', 'XXII', 'S', 'PLUG', 'RAD', 'NVAX', 'GERN', 'APRN', 'INSY', 'GLUU', 'UAA', 'AUY', 'JCP', 'TEVA', 'BILI', 'TRXC', 'BOTZ', 'CARA', 'P', 'VSLR', 'NOK', 'ENPH', 'CRBP', 'CY', 'UA', 'SPWR', 'RUN']
sports 							= ['SIRI', 'BRK.B', 'VZ', 'NKE', 'UAA', 'COST', 'UA', 'CMCSA', 'TTWO', 'EA', 'ELY', 'WWE', 'LULU', 'AMMA', 'XGTI', 'GNC', 'MDXG', 'TTM', 'MANU', 'FL', 'VIPS', 'DKS', 'COKE', 'BGFV', 'MB', 'YOGA', 'PLAY', 'DDE', 'VFC', 'CBS', 'TSG', 'VSI', 'VSTO', 'ADDYY', 'HIBB', 'RICK', 'RACE', 'DAKT', 'GAIA', 'IPG', 'JASNW', 'FLL', 'NWSA', 'ARMK', 'CCE', 'MBUU', 'JASN', 'ZUMZ', 'CLUB', 'CLCT', 'MSGN', 'BATRA', 'RTIX', 'NWS', 'COT', 'OUT', 'RRR', 'MCFT', 'LLIT', 'MSG', 'FWONA', 'QUAD', 'ZBH', 'TPC', 'YGYI', 'SNN', 'AAWW', 'DECK', 'TTC', 'FWONK', 'LSXMA', 'OBCI', 'WBAI', 'DYNT', 'BATRK', 'LSXMK', 'FANZ', 'TRK', 'MCRI', 'CCU', 'TRCO', 'GRVY', 'USPH', 'GCO', 'WHLM', 'RCI', 'WIMHY', 'WINA', 'INSE', 'ODC', 'ISCA', 'RELV', 'SPLP', 'CBS.A', 'SPLP-A', 'PDYPY', 'LSXMB', 'CDNAF']
consumer_product = []  # large inline historical test dataset removed
photovoltaic 					= ['VSLR', 'SPWR', 'SPI', 'FSLR', 'SEDG', 'CSIQ', 'JKS', 'SOL', 'AMRC', 'HQCL', 'NTGN']

ticker_collection 				= [most_popular, bots_index, semiconductor_index, top_movers, cap_weighted, alcohol, beer, china, asia, r_and_d, electric_utilities, renewables, female_ceo, loan, real_estate, kids, entertainment, manufacturing, e_commerce, retail, satellite, broadcasting, wireless, digital_television, television, electronics, radio, automotive, transportation, computer_networking, telecommunications, upcoming_earnings, computer_hardware, road_transportation, internet, material, integrated_circuit, asia_non_china, engineering, packaging, metal, us, business_service,north_america, etf, three_x_etf, aerospace, air_transportation, professional_service, investment_service, cancer_prevention, data_service, outsourcing, logistics, most_popular_under_twenty_five, sports, consumer_product, photovoltaic]
category_names 					= ["most_popular","bots_index","semiconductor_index","top_movers","cap_weighted","alcohol","beer","china","asia","r_and_d","electric_utilities","renewables","female_ceo","loan","real_estate","kids","entertainment","manufacturing","e_commerce","retail","satellite","broadcasting","wireless","digital_television","television","electronics","radio","automotive","transportation","computer_networking","telecommunications","upcoming_earnings","computer_hardware","road_transportation","internet","material","integrated_circuit","asia_non_china","engineering","packaging","metal","us","business_service","north_america","etf","three_x_etf","aerospace","air_transportation","professional_service","investment_service","cancer_prevention","data_service","outsourcing","logistics","most_popular_under_twenty_five","sports","consumer_product","photovoltaic"]

####################################################################################################
####################################################################################################
####################################################################################################

def create_category_csv():
	for b, a in enumerate(ticker_collection):
		c = open("./ticker_categories/" + str(category_names[b]) + ".csv", "w+")
		d = csv.writer(c)
		for e in a:
			d.writerow([e])

####################################################################################################
####################################################################################################
####################################################################################################

#  URL FOR ACCESSING HISTORICALS: https://api.robinhood.com/quotes/historicals/?symbols=AMD,CRSP&interval=day&span=week
def get_ticker_dataset(tickers, interval, span):
	tickers = strip_tag_array(tickers)
	a 		= requests.get("https://api.robinhood.com/quotes/historicals/?symbols=" + str(tickers) + "&interval=" + str(interval) + "&span=" + str(span) + "")
	b 		= a.text
	b 		= json.loads(b)
	return b

####################################################################################################
####################################################################################################
####################################################################################################

def get_news(tick):
	ticker_news = test.get_news(tick)
	return ticker_news

####################################################################################################
####################################################################################################
####################################################################################################

def get_tagged_tickers(tagnames):
	tickers = []
	for a in tagnames:
		b = requests.get("https://api.robinhood.com/midlands/tags/tag/"+a+"/")
		c = json.loads(b.text)
		# print(c)
		if "{'detail': 'Not found.'}" not in str(c):
			for d in c["instruments"]:
				e = requests.get(d)
				f = json.loads(e.text)
				tickers.append(f["symbol"])
	return tickers

####################################################################################################
####################################################################################################
####################################################################################################

def log_tag_changes(tagname):
	a 			= "./_tagname_historical_data"
	b 			= a + "/" + str(datetime.datetime.now()).split(" ")[0].replace("-", "")
	c 			= b + "/" + tagname + ".csv"
	if not os.path.exists(a):
		os.makedirs(a, exist_ok=True)
	if not os.path.exists(b):
		os.makedirs(b, exist_ok=True)
	if not os.path.exists(c):
		tickers = get_tagged_tickers([str(tagname)])
		d = open(c, "w+")
		e = csv.writer(d)
		for f in tickers:
			e.writerow([f])

####################################################################################################
####################################################################################################
####################################################################################################

def init_tag_logging():
	for z in tags:	
		print()
		print("-"*50)
		print(z)
		print("-"*50)
		print()
		log_tag_changes(str(z))
		print()
		print("-"*50)
		print(z)
		print("-"*50)
		print()

####################################################################################################
####################################################################################################
####################################################################################################

def get_instrument(tick):
	# stock_instrument = test.instruments(tick)[0]
	stock_instrument = test.instruments(tick)
	# for a in stock_instrument:
		# print(a)
		# try:
		# 	print(stock_instrument[a])
		# except:
		# 	pass
		# print(stock_instrument[a])
		# print("*"*50)
	return stock_instrument

####################################################################################################
####################################################################################################
####################################################################################################

# buy_order = test.place_buy_order(stock_instrument, 1)
# sell_order = test.place_sell_order(stock_instrument, 1)

# process_tickers(rh_list)

# results
# # interval
# # quote
# # instrument
# # span
# # symbol
# # bounds
# # historicals
# # # open_price 
# # # close_price 
# # # begins_at 
# # # interpolated 
# # # session 
# # # high_price 
# # # low_price 
# # # volume

####################################################################################################
####################################################################################################
####################################################################################################

def strip_tag_array(tickers):
	tickers = str(tickers).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
	return tickers

####################################################################################################
####################################################################################################
####################################################################################################

def get_hist_values(historical_data):
	historical_data = historical_data["historicals"]
	entries 		= []
	for a in historical_data:
		for b in a:
			# print(a)
			# print(b)
			# for c in a[b]:
			if "close_price" in str(b):	
				entries.append(a[b])
					# try:
					# except:
					# 	pass
	return entries
		# print(historical_data[a])

####################################################################################################
####################################################################################################
####################################################################################################

def get_close_avg(close_price):
	prices 				= []
	closing_averages 	= {}
	for a in close_price:
		try:
			prices.append(float(a["close_price"]))
		except:
			pass
	closing_averages["span_total_avg"] 	= float(sum(prices)/len(prices))
	closing_averages["1_day_avg"] 		= float(sum(prices[-1:])/len(prices[-1:]))
	closing_averages["10_day_avg"] 		= float(sum(prices[-10:])/len(prices[-10:]))
	closing_averages["20_day_avg"] 		= float(sum(prices[-20:])/len(prices[-20:]))
	closing_averages["50_day_avg"] 		= float(sum(prices[-50:])/len(prices[-35:]))
	closing_averages["100_day_avg"] 	= float(sum(prices[-100:])/len(prices[-100:]))
	closing_averages["200_day_avg"] 	= float(sum(prices[-200:])/len(prices[-120:]))
	return closing_averages

####################################################################################################
####################################################################################################
####################################################################################################

def get_open_avg(open_price):
	prices 				= []
	opening_averages 	= {}
	for a in open_price:
		try:
			prices.append(float(a["open_price"]))
		except:
			pass
	opening_averages["span_total_avg"] 	= float(sum(prices)/len(prices))
	opening_averages["1_day_avg"] 		= float(sum(prices[-1:])/len(prices[-1:]))
	opening_averages["10_day_avg"] 		= float(sum(prices[-10:])/len(prices[-10:]))
	opening_averages["20_day_avg"] 		= float(sum(prices[-20:])/len(prices[-20:]))
	opening_averages["50_day_avg"] 		= float(sum(prices[-50:])/len(prices[-35:]))
	opening_averages["100_day_avg"] 	= float(sum(prices[-100:])/len(prices[-100:]))
	opening_averages["200_day_avg"] 	= float(sum(prices[-200:])/len(prices[-120:]))
	return opening_averages

####################################################################################################
####################################################################################################
####################################################################################################

def get_averages(dataset, price_type):
	prices 				= []
	opening_averages 	= {}
	for a in dataset:
		try:
			prices.append(float(a["open_price"]))
		except:
			pass
	opening_averages["span_total_avg"] 	= float(sum(prices)/len(prices))
	opening_averages["1_day_avg"] 		= float(sum(prices[-1:])/len(prices[-1:]))
	opening_averages["10_day_avg"] 		= float(sum(prices[-10:])/len(prices[-10:]))
	opening_averages["20_day_avg"] 		= float(sum(prices[-20:])/len(prices[-20:]))
	opening_averages["50_day_avg"] 		= float(sum(prices[-50:])/len(prices[-35:]))
	opening_averages["100_day_avg"] 	= float(sum(prices[-100:])/len(prices[-100:]))
	opening_averages["200_day_avg"] 	= float(sum(prices[-200:])/len(prices[-120:]))
	# print(opening_averages)
	return opening_averages

####################################################################################################
####################################################################################################
####################################################################################################

def get_open_close_avg(open_avg, close_avg):
	# prices 			= []
	open_close_averages = {}
	for a in open_avg:
		try:
			prices 						= [float(open_avg[a]), float(close_avg[a])]
			price_sum 					= sum(prices)
			price_len 					= len(prices)
			open_close_averages[str(a)] = price_sum/price_len
		except:
			pass
	# open_close_averages["span_total_open_avg"] = float(sum(prices)/len(prices))
	# open_close_averages["20_day_open_avg"] = float(sum(prices[-20:])/len(prices[-20:]))
	# open_close_averages["50_day_open_avg"] = float(sum(prices[-50:])/len(prices[-35:]))
	# open_close_averages["100_day_open_avg"] = float(sum(prices[-100:])/len(prices[-100:]))
	# open_close_averages["200_day_open_avg"] = float(sum(prices[-200:])/len(prices[-120:]))
	return open_close_averages

# def get_value_gap(value_set_a, value_set_b):

####################################################################################################
####################################################################################################
####################################################################################################

def process_percent_change_daily(price_data):
	for a in price_data:
		change = float(a["open_price"])/float(a["close_price"])
		print("PERCENT CHANGE DAILY: " + str(change))

####################################################################################################
####################################################################################################
####################################################################################################

def get_percent_change(value_set_a, value_set_b):
	# percent_change 	= (value_set_a - value_set_b)/(value_set_a + value_set_b)
	percent_change 		= float(value_set_a)/float(value_set_b)
	return float(percent_change)

####################################################################################################
####################################################################################################
####################################################################################################

def plotem(industry, dataset):
	counter 		= 0
	dates 			= [] 
	open_val 		= [] 
	close_val 		= [] 
	high_val 		= [] 
	low_val 		= [] 
	high_low_avg 	= []
	open_close_avg 	= []
	sma_twenty 		= []
	sma_fifty 		= []
	sma_two_hund 	= []
	if industry == False:
		# aapl = data.DataReader('AAPL', 'google', '2017-06-01')
		while counter < len(dataset):
			dates.append(dataset[counter]["begins_at"])
			sma_twenty.append(float(dataset[counter]["sma_20"]))
			sma_fifty.append(float(dataset[counter]["sma_50"]))
			sma_two_hund.append(float(dataset[counter]["sma_200"]))
			open_val.append(float(dataset[counter]["open_price"]))
			close_val.append(float(dataset[counter]["close_price"]))
			high_val.append(float(dataset[counter]["high_price"]))
			low_val.append(float(dataset[counter]["low_price"]))
			hi_lo_avg 	= (float(dataset[counter]["low_price"])+float(dataset[counter]["high_price"]))/2.0
			open_close 	= (float(dataset[counter]["open_price"])+float(dataset[counter]["close_price"]))/2.0
			high_low_avg.append(float(hi_lo_avg))
			open_close_avg.append(float(open_close))
			counter+=1
	elif industry == True:
		for a in dataset:
			print(dataset[a])
			print()
			print()
			dates.append(a)
			open_val.append(dataset[a]["price_open_avg"])
			close_val.append(dataset[a]["price_close_avg"])
			low_val.append(dataset[a]["price_low_avg"])
			high_val.append(dataset[a]["price_high_avg"])


	plt.ion()
	fig, ax = plt.subplots()
	candlestick2_ohlc(ax,open_val,high_val,low_val,close_val, colorup="#FFFFFF", colordown="#FF0000", width=2.0)
	# index_bar(ax, close_val, facecolor='b', edgecolor='r', width=1, alpha=1.0)
	# plot_day_summary_oclh(ax, close_val, ticksize=3, colorup='k', colordown='r')

	xdate 	= dates
	# xdate = [datetime.datetime.fromtimestamp(i) for i in quotes['time']]

	ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

	def mydate(x,pos):
	    try:
	        return xdate[int(x)]
	    except IndexError:
	        return ''

	ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	ax.set_facecolor((0.0, 0.0, 0.0))
	fig.autofmt_xdate()
	# fig.tight_layout()

	# PLOT CANDLE AVERAGES
	# plt.plot(dates, open_close_avg, color="b", linewidth=1.5)
	# plt.plot(dates, high_low_avg, color="m", linewidth=1.5)
	
	# PLOT SMAs
	plt.plot(dates, close_val, color="#664444", linewidth=1.5)
	plt.plot(dates, sma_twenty, color="g", linewidth=1.5)
	plt.plot(dates, sma_fifty, color="y", linewidth=1.5)
	plt.plot(dates, sma_two_hund, color="m", linewidth=1.5)


	plt.draw()
	plt.grid(True)
	# plt.draw()
	# plt.pause(50)
	plt.show(block=True)


####################################################################################################
####################################################################################################
####################################################################################################

def get_sma(dataset, time_range):
	counter = 0
	arr_len = len(dataset)
	while counter < arr_len:
		price_arr = []
		start_count = counter 
		end_count = counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			# print("-"*50)
			# print(dataset[sub_counter])
			# print("-"*50)
			# get_price = float(dataset[sub_counter])
			try:
				get_price = float(dataset[sub_counter]["close_price"])
				price_arr.append(get_price)
				sub_counter-=1
			except:
				pass

		sma_val = np.mean(price_arr)
		dataset[counter]["sma_" + str(time_range)] = sma_val
		counter+=1
	return dataset

####################################################################################################
####################################################################################################
####################################################################################################

def convert_to_date_index(dataset):
	new_dataset = {}
	for a in dataset:
		new_dataset[str(a["begins_at"])] = a
	return new_dataset

####################################################################################################
####################################################################################################
####################################################################################################

def gather_industries(tickers, intervals, time_range):
	tag_set = {}
	for a in tickers:
		test_hist_data = get_hist_values(test.get_ticker_dataset_quotes(str(a), intervals, time_range))
		dataset = get_sma(test_hist_data, 20)
		dataset = get_sma(dataset, 50)
		dataset = get_sma(dataset, 200)
		dataset = convert_to_date_index(dataset)
		for b in dataset:
			if b not in tag_set:
				tag_set[b] = {}
				tag_set[b][a] = dataset[b]
			else:	
				tag_set[b][a] = dataset[b]
	return tag_set

####################################################################################################
####################################################################################################
####################################################################################################

def get_industries_sma(dataset):
	industry_values = {}
	for a in dataset:
		# print(a)
		closing_prices = []
		opening_prices = []
		high_prices = []
		low_prices = []
		# opening_prices = []
		for b in dataset[a]:
			opening_prices.append(float(dataset[a][b]["open_price"]))
			closing_prices.append(float(dataset[a][b]["close_price"]))
			high_prices.append(float(dataset[a][b]["high_price"]))
			low_prices.append(float(dataset[a][b]["low_price"]))
		industry_values[a] = {"price_open_avg":np.mean(opening_prices), "price_close_avg":np.mean(closing_prices), "price_high_avg":np.mean(high_prices), "price_low_avg":np.mean(low_prices)}
	# print(industry_values)
	return industry_values

####################################################################################################
####################################################################################################
####################################################################################################

def get_markets():
	a = requests.get("https://api.robinhood.com/markets/")
	b = a.text
	c = json.loads(b)
	return c

####################################################################################################
####################################################################################################
####################################################################################################

def market_direction(indexname, direction):
	a = requests.get("https://api.robinhood.com/midlands/movers/"+indexname+"/?direction="+direction+"")
	b = a.text
	c = json.loads(b)
	return c

####################################################################################################
####################################################################################################
####################################################################################################

def test_moving_averages(tag, time_interval, time_span):
	test_hist_data = get_hist_values(test.get_ticker_dataset_quotes("CRSP", "week", "5year"))
	# test_hist_data = get_hist_values(test.get_ticker_dataset_quotes("CRSP", "day", "year"))
	# test_hist_data = get_hist_values(test.get_ticker_dataset_quotes("CRSP", "5minute", "week"))
	# [large inline historical test dataset removed during archival cleanup]
	# get_averages(test_hist_data, "close_price")
	
	dataset = get_sma(test_hist_data, 20)
	dataset = get_sma(dataset, 50)
	dataset = get_sma(dataset, 200)

	##############################
	### INDUSTRIES TEST
	##############################

	# dataset 		= convert_to_date_index(dataset)
	# INTERVALS 	= ['15second', '5minute', '10minute', 'hour', 'day', 'week']
	# SPANS 		= ['day', 'hour', 'week', 'year', '5year', 'all']

	# dataset = gather_industries(global_stocks, "week", "5year")
	# dataset = gather_industries(tag, time_interval, time_span)
	# dataset = gather_industries(beer, "week", "5year")
	# dataset = gather_industries(asia, "week", "5year")
	# dataset = gather_industries(r_and_d, "week", "5year")
	# dataset = gather_industries(electric_utilities, "week", "5year")
	# dataset = gather_industries(renewables, "day", "year")
	# dataset = gather_industries(renewables, "week", "5year")
	# dataset = gather_industries(female_ceo, "week", "5year")
	# dataset = gather_industries(loan, "week", "5year")
	# dataset = gather_industries(real_estate, "week", "5year")
	# dataset = gather_industries(kids, "week", "5year")
	# dataset = gather_industries(entertainment, "week", "5year")
	# dataset = gather_industries(manufacturing, "week", "5year")
	# dataset = gather_industries(e_commerce, "week", "5year")
	# dataset = gather_industries(retail, "week", "5year")
	# dataset = gather_industries(broadcasting, "week", "5year")
	# dataset = gather_industries(digital_television, "week", "5year")
	# dataset = gather_industries(television, "week", "5year")
	# dataset = gather_industries(electronics, "week", "5year")
	# dataset = gather_industries(radio, "week", "5year")
	# dataset = gather_industries(automotive, "week", "5year")
	# dataset = gather_industries(transportation, "week", "5year")
	# dataset = gather_industries(telecommunications, "week", "5year")
	# dataset = gather_industries(upcoming_earnings, "week", "5year")
	# dataset = gather_industries(computer_hardware, "week", "5year")
	# dataset = gather_industries(material, "week", "5year")
	# dataset = gather_industries(packaging, "week", "5year")
	# dataset = gather_industries(business_service, "week", "5year")
	# dataset = gather_industries(etf, "week", "5year")
	# dataset = gather_industries(aerospace, "week", "5year")
	# dataset = gather_industries(air_transportation, "week", "5year")
	# dataset = gather_industries(professional_service, "week", "5year")
	# dataset = gather_industries(investment_service, "week", "5year")
	# dataset = gather_industries(cancer_prevention, "week", "5year")
	# dataset = gather_industries(outsourcing, "week", "5year")
	# dataset = gather_industries(logistics, "week", "5year")
	# dataset = gather_industries(most_popular_under_twenty_five, "week", "5year")
	# dataset = gather_industries(sports, "week", "5year")
	# dataset = gather_industries(consumer_product, "week", "5year")
	
	# for a inphotovoltaic:
	# 	print(dataset[a])
	dataset = get_industries_sma(dataset)
	# print(dataset)
	plotem(True, dataset)

	##############################
	##############################
	##############################
	

	# print(dataset)
	# plotem(tag_or_ticker, dataset)

	# print("OPENING AVERAGES: " +  str(get_open_avg(test_hist_data)))
	# print("CLOSING AVERAGES: " + str(get_close_avg(test_hist_data)))
	# print("OPENING + CLOSING AVERAGES: " + str(get_open_close_avg(get_open_avg(test_hist_data), get_close_avg(test_hist_data))))

	# value_set_a = get_close_avg(test_hist_data)
	# value_set_a = value_set_a["10_day_avg"]

	# value_set_b = get_open_avg(test_hist_data)
	# value_set_b = value_set_b["10_day_avg"]
	# print(value_set_a)
	# print(value_set_b)
	# print("DAILY PERCENT CHANGE: " + str(get_percent_change(float(value_set_a), float(value_set_a))))
	# process_percent_change_daily(test_hist_data)
	# print(test_hist_data)
	# counter = 0
	# arr_len = len(test_data)
	# print(arr_len)
	# while counter < arr_len:
	# 	try:
	# 		print(test_data[counter:counter+14])
	# 	except:
	# 		pass
	# 	# print(counter)
	# 	counter += 1
	# for a in test_hist_data:
	# 	print(len(test_hist_data))
	# 	print(a["close_price"])
	# print("OPENING + CLOSING AVERAGES: " + str(get_open_close_avg(get_open_avg(test_hist_data), get_close_avg(test_hist_data))))
	# print(test.get_ticker_dataset_quotes("FB", "day", "year"))
	# print(test.get_ticker_dataset_quotes("FB", "week", "5year"))


####################################################################################################
####################################################################################################
####################################################################################################

# dataset 		= convert_to_date_index(dataset)
# tickers 		= [] # Enter array of tickers
# time_interval = ['15second', '5minute', '10minute', 'hour', 'day', 'week']
# time_span 	= ['day', 'hour', 'week', 'year', '5year', 'all']
def plot_tickers(tickers, time_interval, time_span):
	dataset = gather_industries(tickers, time_interval, time_span)
	dataset = get_industries_sma(dataset)
	# print(dataset)
	plotem(True, dataset)

####################################################################################################
####################################################################################################
####################################################################################################

def get_price_data(historical_dataset):
	# for b, a in enumerate(historical_dataset["results"]):
		# print()
		# print("-"*50)
		# print()
		# print(a["symbol"])
		# print()
		# print("-"*50)
		# print()
		# for c in historical_dataset["results"][b]["historicals"]:
		# 	print(c)
	return historical_dataset["results"]
	# return historical_dataset["results"][b]["historicals"]

####################################################################################################
####################################################################################################
####################################################################################################


####################################################################################################
########################################## INITIAL STEPS ###########################################
####################################################################################################

# 1. INIT TAG COLLECTION AND SAVE LOCALLY
## Create a local copy of ticker groupings to avoid making a ton of requests/slowing down the process
# init_tag_logging()

# 2. COLLECT HISTORICAL QUOTES AND SAVE LOCALLY

# 3. UPDATE 

####################################################################################################
########################################### BACKTESTING ############################################
####################################################################################################

# 1. UPDATE DATA COLLECTIONS. TAGS AND QUOTES

# 2. CHECK FOR INCOMPLETE TAG LISTINGS/CSV FILES

# 3. RUN DIFFS ON TAG SETS. COMPARE CHANGES IN GROUPINGS. SIMPLY CHECK LEN AND MEMBERSHIP COUNTS

# 4. PROCESS SMAs AND ANY OTHER INDICATOR

# 5. PLOT EM

# 6. CREATE BRIEF REPORTS ON TAG COLLECTIONS. SIMPLE CHANGE DETECTION IF IMPATIENT 

# plot_tickers(alcohol, "week", "5year")
# print(test.get_news("FB"))
# plot_tickers(["AMD"], "week", "5year")
# plot_tickers(television, "week", "5year")
# process_tickers(loan)
# test_moving_averages(television, "week", "5year")
# print(test.instruments("BTC"))
# print(test.news("FB"))
# print(test.get_popularity("FB"))
# print(test.get_tickers_by_tag("technology"))
# print(test.get_fundamentals("FB"))
# get_ticker_dataset("FB", "day", "year")
# testing = get_ticker_dataset("FB", "day", "year")
# print(get_ticker_dataset("FB", "day", "year"))



# print(get_markets())
# print(market_direction("sp500", "up"))



# def get_sma_diff_range(dataset, sma_type):
# 	diffs = []
# 	for a in dataset:
# 		# test_fract 	= float(a["sma_" + str(sma_type[0])])/float(a["sma_" + str(sma_type[1])])
# 		test_diff 	= float(a["sma_" + str(sma_type[0])])-float(a["sma_" + str(sma_type[1])])
# 		diffs.append(float(test_diff))
# 	diffs.sort()
	
# 	front 	= []
# 	back  	= []
# 	counter = 0
# 	ends 	= int(len(diffs)*.2)
# 	backend = len(diffs)-ends

# 	while counter < ends:
# 		# print(diffs[counter])
# 		# print(ends)
# 		# print(backend)
# 		# print(counter)
# 		front.append(diffs[counter])
# 		counter+=1
	
# 	counter = 1
# 	# print(ends)
# 	# print()
# 	while (ends-counter)+backend > backend:
# 		# print(diffs[(ends-counter)+backend])
# 		back.append(diffs[(ends-counter)+backend])
# 		# print((ends-counter)+backend)
# 		counter+=1

# 	# print("*"*50)
# 	# print(np.mean(front))
# 	# print(np.mean(back))
# 	# print("*"*50)
# 	return [np.mean(front), np.mean(back)]



































sma_a = 1
sma_b = 3
sma_c = 12
fract = .2

# start_date 		= 100000 
sma_diff_time = 1000



def get_sma_diff_range(dataset, sma_type):
	diffs 	= []

	dataset_end = len(dataset)-1
	# dataset_start = dataset_end-100
	dataset_start = dataset_end-sma_diff_time
	while dataset_start < dataset_end:
	# for a in dataset:
		a = dataset[dataset_start]
		test_diff 	= float(a["sma_" + str(sma_type[0])])-float(a["sma_" + str(sma_type[1])])
		diffs.append(float(test_diff))
		dataset_start += 1

	diffs.sort()
	front 	= []
	back  	= []
	counter = 0
	ends 	= int(len(diffs)*fract)
	backend = len(diffs)-ends

	while counter < ends:
		front.append(diffs[counter])
		counter+=1
	
	counter = 1

	while (ends-counter)+backend > backend:
		back.append(diffs[(ends-counter)+backend])
		counter+=1
	return [np.mean(front), np.mean(back)]






# x = open("20190122_145449___data.json", "r+")
x = open("20190120_192023___data.json", "r+")
w = json.load(x)



# testing = w
# print(w)
print("-"*50)
print(len(w))
# for hh in ff:
# 	# print(hh)
# 	w.append(hh)
# w.append(ff)
testing = w
# print(ff)
# print(w)
# print(w)
# print(len(w))
# print(len(jj))
print("-"*50)
# ETH GEMINI HR 2017 - Han 2019 = 100K+ off 1k
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 3)

# ETH GEMINI 1 MIN TOTAL 2016-2018 = 330K+ off 1k 
# dataset = get_sma(testing, 2)
# dataset = get_sma(testing, 7)

# BTC GEMINI 1 MIN TOTAL 2015-2017 = 443501.71825211716 off 1k 
# dataset = get_sma(testing, 2)
# dataset = get_sma(testing, 7)


# LAST LEFT OFF GDAX 20190120_192023___data ETH - FULL CONDITIONAL - 12289 return
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 2)
# dataset = get_sma(testing, 12)

dataset = get_sma(testing, sma_a)
dataset = get_sma(testing, sma_b)
# print(dataset)
dataset = get_sma(testing, sma_c)

# dataset = get_sma(testing[0]["historicals"], 2)
# dataset = get_sma(testing[0]["historicals"], 7)
# dataset = get_sma(testing[0]["historicals"], 15)



def strat_support_resist(dataset, sma_type):
	for a in dataset:
		# print(a[])
		print(a["sma_" + str(sma_type[0])])
		print(a["sma_" + str(sma_type[1])])
		print(a["sma_" + str(sma_type[2])])


def backtest(dataset):
	start_balance 	= 1000
	balance 		= start_balance
	quantity 		= 0.0
	last_val 		= 0.0
	buy 			= False
	valuation 		= 0.0
	signal 			= "BOUGHT"
	diff 			= 100.0*(float(start_balance)/float(balance))
	sma_counter 	= 0
	sma_total 		= 0
	sma_type 		= []
	sma_appended 	= False

	for d in dataset:
		if sma_appended == False:
			for e in d:
				if "sma_" in str(e):
					sma_counter+=1
					sma_inter = int(e.replace("sma_", ""))
					sma_type.append(sma_inter)
			sma_total = sma_counter
			sma_type.sort()
			sma_appended = True
		break

	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	buy_thresh = 0
	sell_thresh = 0
	# buy_thresh = get_sma_diff_range(dataset, sma_type)[0]
	# sell_thresh = get_sma_diff_range(dataset, sma_type)[1]
	# buy_thresh = get_sma_diff_range_from_center(dataset, sma_type)[0]
	# sell_thresh = get_sma_diff_range_from_center(dataset, sma_type)[1]
	test_end 		= len(dataset) 
	test_start 		= 0
	# test_start 		= test_end-start_date
	# test_start 		= test_end-300000
	# -4.960080557818564
	# 4.9140145637349075

	tt = []
	yy = []
	for vv, d in enumerate(dataset):
	# while test_start < test_end:
		test_start = test_start
		# print(test_start)
		# d = dataset[test_start]
		# tt.append(d)
		yy.append(d)
		# print(sma_type)
		# print("-"*50)
		try:
			buy_thresh = get_sma_diff_range(yy, sma_type)[0]
			sell_thresh = get_sma_diff_range(yy, sma_type)[1]
			# print(buy_thresh)
			# print(sell_thresh)
		except:
			pass
		# print(d)

		# print(d["sma_" + str(sma_type[1]))
		# print(d["sma_" + str(sma_type[1]))
		# test_diff 	= float(d["sma_" + str(sma_type[1])])-float(d["sma_" + str(sma_type[2])])
		test_diff 	= float(d["sma_" + str(sma_type[0])])-float(d["sma_" + str(sma_type[1])])
		# print(vv)
		# print(buy)
		# print(buy_thresh)
		# print(sell_thresh)
		# print(test_diff)
		# order_date 	= d["date"]
		order_date 	= d["begins_at"]
		# try:	
		# if test_fract > 1.007 and buy == True and float(start_balance) > 0.0:
		# if test_diff > sell_thresh and buy == True:
		# if test_diff > sell_thresh and buy == True and quantity*float(d["close_price"]) > float(start_balance) and last_val < quantity*float(d["close_price"]):
		if test_diff > sell_thresh and buy == True and quantity*float(d["close_price"]) > float(start_balance):
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			balance 	= quantity*float(d["close_price"])
			valuation	= 0.0
			quantity 	= 0.0