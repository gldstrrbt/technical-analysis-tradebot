import os
import subprocess, requests, urllib

# client_id: 910fb9f4-f10a-4247-bbb7-e119669b049d
username = os.getenv("ROBINHOOD_USERNAME", "")
password = os.getenv("ROBINHOOD_PASSWORD", "")
def login():
	username = os.getenv("ROBINHOOD_USERNAME", "")
	password = os.getenv("ROBINHOOD_PASSWORD", "")
	header = {"Accept": "application/json"}
	# data = {"client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
	#         "expires_in": 86400,
	#         "grant_type": "password",
	#         "password": password,
	#         "scope": "internal",
	#         "username": username}
	data = {
		"client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
		"expires_in": 86400,
		"grant_type": "password",
		"password": password,
		"scope": "internal",
		"username": username,
		"access_token": os.getenv("ROBINHOOD_ACCESS_TOKEN", ""),
		"backup_code": "null",
		"expires_in": 86400,
		"mfa_code": "null",
		"refresh_token": os.getenv("ROBINHOOD_REFRESH_TOKEN", ""),
		"scope": "internal",
		"token_type": "Bearer"
	}

	url = "https://api.robinhood.com/oauth2/token/"
	r = requests.post(url, data=data, headers=header)
	return r.text

# print(login())
















def login_b( username, password, mfa_code=None):
	username = username
	password = password
	mfa_code = mfa_code
	header = {"Accept": "application/json", "Content-Type": "application/json"}
	# header = {"Authorization": os.getenv("API_TOKEN", "")}
	#fields = { 'password' : password, 'username' : username, 'mfa_code': mfa_code }
	#fields = { 'password' : password, 'username' : username }
	
	if mfa_code:
		fields = { 'client_id' : 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
					'expires_in' : 86400,
					'grant_type': 'password',
					'password' : password,
					'scope' : 'internal',
					'username' : username,
					'mfa_code': mfa_code }
	else:
		fields = { 'client_id' : 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
					'expires_in' : 86400,
					'grant_type': 'password',
					'password' : password,
					'scope': 'internal',
					'username' : username }
	try:
		data = urllib.urlencode(fields) #py2
	except:
		data = urllib.parse.urlencode(fields) #py3
	# res = session.post(endpoints['login'], data=data)
	res = requests.post("https://api.robinhood.com/oauth2/token/", data=data, headers=header)
	#res.raise_for_status()
	res = res.json()
	#print(data)
	try:
		#auth_token = res['token']
		oauth_token = res['access_token']
	except KeyError:
		return res
	#headers['Authorization'] = 'Token '+auth_token
	headers['Authorization'] = 'Bearer ' + oauth_token
	return True



print(login_b(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""), mfa_code=None))











def login(username, password):  
	command = 'curl -v https://api.robinhood.com/oauth2/token/ -H "Accept: application/json" -d "username='+username+'&password='+password+'&access_token=<REDACTED>"'  
	# command = 'curl -v https://api.robinhood.com/api-token-auth/ -H "Accept: application/json" -d "username='+username+'&password='+password+'"'  
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)  
	out, err = p.communicate()  
	if len(out) < 1:  
		print('Error connecting to server:')
		print(err)
	else:  
		print('Connection successful.')
	return out

def logout(token):  
	command = 'curl -v https://api.robinhood.com/api-token-logout/ -H "Accept: application/json" -H "Authorization: Token '+str(token)+'" -d ""'  
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)  
	out, err = p.communicate()


def accountInfo(token):  
	command = 'curl -v https://api.robinhood.com/accounts/ -H "Accept: application/json" -H "Authorization: Token '+str(token)+'"'  
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)  
	out, err = p.communicate()  
	return out

def main():  
	print('Logging in...')
	token = login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))  
	token = token[10:-2]  
	print('token: ', token)
	print('Grabbing account information...')
	account_info = accountInfo(token)  
	print(account_info)
	print('Logging out...')
	logout(token)

# main()




# import subprocess

# def login(username, password):  
#     # command = 'curl -v https://api.robinhood.com/api-token-auth/ -H "Accept: application/json" -d "username='+username+'&password='+password+'"'  
#     command = 'curl -v https://api.robinhood.com/oauth2/token/ -H "Accept: application/json" -d "username='+username+'&password='+password+'"'  
#     p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)  
#     out, err = p.communicate()  
#     if len(out) < 1:  
#         print('Error connecting to server:')
#         print(err)
#     else:  
#         print('Connection successful.')
#     return out

# def logout(token):  
#     command = 'curl -v https://api.robinhood.com/api-token-logout/ -H "Accept: application/json" -H "Authorization: Token '+str(token)+'" -d ""'  
#     p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)  
#     out, err = p.communicate()


# def accountInfo(token):  
#     command = 'curl -v https://api.robinhood.com/accounts/ -H "Accept: application/json" -H "Authorization: Token '+str(token)+'"'  
#     p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)  
#     out, err = p.communicate()  
#     return out

# def main():  
#     print('Logging in...')
#     token = login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))  
#     token = token[10:-2]  
#     print('token: ', format(token).encode())
#     print('Grabbing account information...')
#     account_info = accountInfo(token)  
#     print(account_info)
#     print('Logging out...')
#     logout(token)

# main()