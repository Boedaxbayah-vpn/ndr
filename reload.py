
import requests,json,os,time
from requests import get,post
from colorama import *

r  = requests.Session()
init(autoreset=True)
merah = Fore.LIGHTRED_EX
kuning = Fore.LIGHTYELLOW_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
magenta = Fore.LIGHTMAGENTA_EX
cyan = Fore.LIGHTCYAN_EX
hitam = Fore.LIGHTBLACK_EX
putih = Fore.LIGHTWHITE_EX
reset = Fore.RESET
base_url = "https://api.stake.games/graphql"
# data_balance = {"operationName":"UserVaultBalances","variables":{},"query":"query UserVaultBalances {\n  user {\n    id\n    balances {\n      available {\n        amount\n        currency\n        __typename\n      }\n      vault {\n        amount\n        currency\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

def banner():
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f""" 
{putih}[{hijau}*{putih}] {biru}claim reload stake
""")

def anticaptcha(key,coin):
	headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
	r.headers.update(headers)
	data = {"clientKey":key,"task":{"type":"NoCaptchaTaskProxyless","websiteURL":f"https://stake.games/?currency={coin}&modal=vip&tab=reload","websiteKey":"6LejnqMaAAAAAFiADZRW595wLmw1pib6kG-gYS18"},"softId":0,"languagePool":"en"}
	a = r.post("https://api.anti-captcha.com/createTask",json=data).json()
	taskid = a['taskId'];errorid = a['errorId']
	if errorid == 0:
		while True:
			data = {"clientKey":key,"taskId":taskid}
			b = r.post("https://api.anti-captcha.com/getTaskResult",json=data).json()
			if "status" not in json.dumps(b):
				break
			elif "status" in json.dumps(b):
				status = b['status']
				if status == "ready":
					return b['solution']['gRecaptchaResponse']
			time.sleep(2)
	else:
		anticaptcha(key,coin)

def captcha2(key,coin):
	parameter = {"key":key,"method":"userrecaptcha","googlekey":"6LejnqMaAAAAAFiADZRW595wLmw1pib6kG-gYS18","pageurl":f"https://stake.games/?currency={coin}&modal=vip&tab=reload","json":1}
	a = get("https://2captcha.com/in.php",params=parameter,headers={'Content-Type': 'application/json', 'Accept': 'application/json'}).json()
	status = a['status'];orderid = a['request']
	if status == 1:
		while True:
			parameter = {"key":key,"id":orderid,"json":1,"action":"get"}
			b = get("https://2captcha.com/res.php",params=parameter,headers={'Content-Type': 'application/json', 'Accept': 'application/json'},timeout=60).json()
			if b['status'] == 1:
				return b['request']
			elif b['status'] == 0 and 'CAPCHA_NOT_READY' in b['request']:
				time.sleep(5)
				continue
			else:
				exit(f'{merah}error :',b['request'])
	else:
		captcha2(key,coin)

def formater(nilai):
	return "{:.8f}".format(nilai)

def susu(t):
	while t:
		print(f"{hijau}claim reload after {biru}{t} {hijau}seconds ",flush=True,end='\r')
		t -= 1
		time.sleep(1)

def SelectCrypto(cur):
	if cur.lower() == 'bch':
		return 0
	if cur.lower() == 'btc':
		return 1
	if cur.lower() == 'doge':
		return 2
	if cur.lower() == 'eos':
		return 3
	if cur.lower() == 'eth':
		return 4
	if cur.lower() == 'ltc':
		return 5
	if cur.lower() == 'trx':
		return 6
	if cur.lower() == 'xrp':
		return 7

def ResterictRegion():
	data = {"operationName":"RestrictedRegion","variables":{},"query":"query RestrictedRegion {\n  isBlocked\n  country\n}\n"}
	headers = {
		'accept': '*/*',
		'accept-language': 'en-US,en;q=0.9',
		'content-type': 'application/json',
		'origin': 'https://stake.games',
		'referer': 'https://stake.games/',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/"537.36 Edg/90.0.818.66',
		'x-access-token': '',
		'x-language': 'en',
		'x-lockdown-token': ''
	}
	r.headers.update(headers)
	req = r.post(base_url,json=data).json()
	country = req['data']['country']
	IsBlock = req['data']['isBlocked']
	if IsBlock == True:
		exit("you region is blocked from stake")
	else:
		return

def ReloadChecker(token,coin):
	data = {"operationName":"ClaimReloadMeta","variables":{"currency":coin},"query":"query ClaimReloadMeta($currency: CurrencyEnum!) {\n  user {\n    id\n    flags {\n      flag\n      __typename\n    }\n    flagProgress {\n      flag\n      __typename\n    }\n    reload: faucet {\n      id\n      amount(currency: $currency)\n      active\n      claimInterval\n      lastClaim\n      expireAt\n      createdAt\n      updatedAt\n      __typename\n    }\n    __typename\n  }\n}\n"}
	headers = {
		'accept': '*/*',
		'accept-language': 'en-US,en;q=0.9',
		'content-type': 'application/json',
		'origin': 'https://stake.games',
		'referer': 'https://stake.games/',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/"537.36 Edg/90.0.818.66',
		'x-access-token': token,
		'x-language': 'en',
		'x-lockdown-token': ''
	}
	r.headers.update(headers)
	req = r.post(base_url,json=data).json()
	status_reload = req['data']['user']['reload']['active']
	amount = req['data']['user']['reload']['amount']
	interval_claim = req['data']['user']['reload']['claimInterval']/1000
	return status_reload

def claim(token,cur,meki,ke):
	print(f'{biru}[-] {cyan}account {putih}{ke[0]}/{ke[1]}:')
	headers = {"accept": "*/*","accept-language": "en-US,en;q=0.9,id;q=0.8,mt;q=0.7","content-type": "application/json","origin": "https://stake.games","referer": "https://stake.games/","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-site","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","x-access-token": token,"x-language": "en","x-lockdown-token": "undefined"}
	if "anticaptcha" in meki[0]:
		data = {"operationName":"ClaimReload","variables":{"currency":cur,"captcha":anticaptcha(meki[1],cur)},"query":"mutation ClaimReload($currency: CurrencyEnum!, $captcha: String!) {\n  claimReload: claimFaucet(currency: $currency, captcha: $captcha) {\n    reload: faucet {\n      user {\n        id\n        reload: faucet {\n          id\n          amount(currency: $currency)\n          active\n          claimInterval\n          lastClaim\n          expireAt\n          createdAt\n          updatedAt\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
	elif "2captcha" in meki[0]:
		data = {"operationName":"ClaimReload","variables":{"currency":cur,"captcha":captcha2(meki[1],cur)},"query":"mutation ClaimReload($currency: CurrencyEnum!, $captcha: String!) {\n  claimReload: claimFaucet(currency: $currency, captcha: $captcha) {\n    reload: faucet {\n      user {\n        id\n        reload: faucet {\n          id\n          amount(currency: $currency)\n          active\n          claimInterval\n          lastClaim\n          expireAt\n          createdAt\n          updatedAt\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
	data_init = {"operationName":"initialUserRequest","variables":{},"query":"query initialUserRequest {\n  user {\n    ...UserAuth\n    __typename\n  }\n}\n\nfragment UserAuth on User {\n  id\n  name\n  email\n  hasPhoneNumberVerified\n  hasEmailVerified\n  hasPassword\n  intercomHash\n  createdAt\n  hasTfaEnabled\n  mixpanelId\n  hasOauth\n  flags {\n    flag\n    __typename\n  }\n  roles {\n    name\n    __typename\n  }\n  balances {\n    ...UserBalanceFragment\n    __typename\n  }\n  activeClientSeed {\n    id\n    seed\n    __typename\n  }\n  previousServerSeed {\n    id\n    seed\n    __typename\n  }\n  activeServerSeed {\n    id\n    seedHash\n    nextSeedHash\n    nonce\n    blocked\n    __typename\n  }\n  __typename\n}\n\nfragment UserBalanceFragment on UserBalance {\n  available {\n    amount\n    currency\n    __typename\n  }\n  vault {\n    amount\n    currency\n    __typename\n  }\n  __typename\n}\n"}
	a = r.post("https://api.stake.games/graphql",headers=headers,json=data).json()
	b = r.post('https://api.stake.games/graphql',headers=headers,json=data_init).json()
	if "errors" in json.dumps(a):
		print(f'\t{putih}[-] {merah}reload already claimed')
		return 600
	else:
		index_coin = SelectCrypto(cur)
		tot = a['data']['claimReload']['reload']['user']['reload']['amount']
		ce = int(a['data']['claimReload']['reload']['user']['reload']['claimInterval']/1000)
		print(f'\t{putih}reload {hijau}: {hijau}{formater(tot)} '+putih+cur.upper())
		print(f'\t{putih}balance {hijau}: '+formater(b['data']['user']['balances'][index_coin]['available']['amount'])+f' {putih}'+cur.upper())
		return ce

def menu():
	banner()
	if not os.path.exists('data.json'):
		a = input(f'{biru}[-] {cyan}input currency : {putih}')
		b = int(input(f"{biru}[-] {cyan}input (sleep time) : {putih}"))
		x = {"currency":a,"time":b}
		with open("data.json","w") as data:
			json.dump(x,data)
	if not os.path.exists('token.txt'):
		open('token.txt','a+').write('')
	cc = json.loads(open("data.json").read())["currency"]
	wk = json.loads(open("data.json").read())["time"]
	banner()
	jm = 0
	try:
		lt = open("token.txt").read().splitlines()
		if not os.path.exists("bypass.json"):
			status_bypass = f"{merah}tidak aktif"
		elif os.path.exists("bypass.json"):
			status_bypass = f"{hijau}aktif"
			provider = mykey = json.loads(open("bypass.json").read())["provider"]
			mykey = json.loads(open("bypass.json").read())["key"]
		print(f'{biru}[-] {hijau}total account : {putih}{len(lt)}')
		print(f"{putih}[-] {hijau}menu :\n\t{putih}[1] {cyan}10 / minutes\n\t{putih}[2] {cyan}1 day\n\t{putih}[3] {cyan}bypass captcha {status_bypass}")
		kl = int(input(f'\n{cyan}[-] {putih}choice : '))
		if len(lt) == 0:
			exit(f'{putih}[-] {merah}please input token account !')
		if kl == 1:
			while True:
				acc = 1
				lacc = len(lt)
				mulai = int(time.time())
				for xnxx in lt:
					print('~'*45)
					rel = ReloadChecker(xnxx,cc)
					if rel == True:
						print(f"{putih}[+] {biru}reload is {hijau}active")
						jm = claim(xnxx,cc,(provider,mykey),(acc,lacc))
						acc += 1
					else:
						print(f"{putih}[+] {biru}reload is {merah}non-active")
						acc += 1
						continue
					acc += 1
				selesai = int(time.time())
				kurun_waktu = selesai-mulai
				susu(int(610-kurun_waktu))
		elif kl == 2:
			acc = 1
			lacc = len(lt)
			print(f"{merah}[!] pencet we ku sorangan sapoe sakali ie !")
			input(f"{hijau}press any key to continue")
			menu()
		elif kl == 3:
			pil = int(input(f"\n{putih}[1] {hijau}anti-captcha\n{putih}[2] {hijau}2captcha\n{cyan}\n[-] {putih}choice :"))
			if pil == 1:
				key = input(f"{putih}[-] {cyan}input key {putih}: ")
				provider = "anticaptcha"
			elif pil == 2:
				key = input(f"{putih}[-] {cyan}input key {putih}: ")
				provider = "2captcha"
			data = {"provider":provider,"key":key}
			with open("bypass.json","w") as menulis:
				json.dump(data,menulis)
			input(f"{hijau}press any key to continue")
			menu()
	except KeyboardInterrupt:exit()
	except ValueError:exit(f'{putih}[-]{merah} please input as number !')
#	except Exception as e:exit(e)


ResterictRegion()
menu()
