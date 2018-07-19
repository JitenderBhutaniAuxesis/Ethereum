# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
from django.shortcuts import render
from .models import Account
import time
from .forms import UserForm,TransactionForm

WAIT_TIME = 15
KEYS_DIR = r"/home/auxesis/Documents/Ethereum/PrivateEthr1"
PORT = 8546 # 6060
URL = 'http://localhost:' + str(PORT)
headers = {'Content-type': 'application/json'}
payload = {"jsonrpc": "2.0","id": 1}

# Create your views here.
def home(request):
    return render(request, 'crypto/home.html', {'number' : 1})


def accounts(request):
    template = 'crypto/all_accounts.html'
    payload['method'] = 'eth_accounts'
    payload['params'] = []


    # response = session.post('http://localhost:8501', json=payload, headers=headers)
    # print('raw json response: {}'.format(response.json()))
    # print('network id: {}'.format(response.json()['result']))

    if request.method == 'GET' :
        try:
            response = requests.post(URL, data=json.dumps(payload), headers=headers)
            json_data = json.loads(response.text)

            result = json_data['result']
            final_result = []
            for address in result:
                data_dict = {}
                balance = get_balance(request, address)
                data_dict['address'] = address
                data_dict['balance'] = str(int(balance, 16))
                final_result.append(data_dict)

            return render(request, template, {'accounts': final_result})
        except Exception as e:
            return render(request, template,{'error_message' : str(e)})

    return render(request, template, {'accounts': ['Bad Request']})



def get_balance(request, address):
    payload['method'] = 'eth_getBalance'
    payload['params'] = [address,'latest']
    try:
        response = requests.post(URL, data=json.dumps(payload), headers=headers)
        json_data = json.loads(response.text)
        return json_data['result']
    except Exception as e:
        return str(e)


def account_details(request):
    pass


def new_account(request):
    template = 'crypto/new_account.html'
    if request.method == 'GET':
        return render(request, template, {'error_message' : ''})


def new_account(request):
    template = 'crypto/new_account.html'
    if request.method == 'GET':
        form = UserForm(None)
        return render(request, template, {'error_message' : '','form' : form})

    if request.method == 'POST':
        try :
            form = UserForm(request.POST)

            if form.is_valid():
                cleaned_data = form.cleaned_data
                username = cleaned_data['username']
                password = cleaned_data['password']

                payload['method'] = "personal_newAccount"
                payload['params'] = [password]
                response = requests.post(URL, data=json.dumps(payload), headers=headers)
                json_data = json.loads(response.text)

               #user.save()
                form = UserForm(None)
                return render(request, template, {'error_message': 'Success - Addreess : ' + json_data['result'],'form' : form})

        except Exception as e:
            form = UserForm(None)
            return render(request, template, {'error_message': str(e),'form' : form})


def send_transaction(request):
    template = 'crypto/send_transaction.html'
    if request.method == 'GET':
        form = TransactionForm(None)
        return render(request, template, {'error_message': '', 'form': form})

    if request.method == 'POST':
        try:
            form = TransactionForm(request.POST)

            if form.is_valid():
                cleaned_data = form.cleaned_data
                from_address = cleaned_data['from_address']
                to_address = cleaned_data['to_address']
                amount = cleaned_data['amount']
                password =  cleaned_data['password']

                payload['method'] = 'personal_unlockAccount'
                payload['params'] = [from_address,password]
                response = requests.post(URL, data=json.dumps(payload), headers=headers)
                json_data = json.loads(response.text)

                if 'result' in json_data:
                    if json_data['result'] == True:
                        payload['method'] = "eth_sendTransaction"
                        payload['params'] = [{"from": from_address, "to": to_address, "value": hex(int(amount))}]
                        response = requests.post(URL, data=json.dumps(payload), headers=headers)
                        json_data = json.loads(response.text)

                    form = TransactionForm(None)
                    start_mining()
                    time.sleep(WAIT_TIME)
                    stop_mining()
                    return render(request, template, {'error_message': 'Success : Transaction ID ' + json_data['result'], 'form': form})

                else:
                    form = TransactionForm(None)
                    return render(request, template,{'error_message': 'Error : ' + json_data['error']['message'], 'form': form})

        except Exception as e:
            form = TransactionForm(None)
            return render(request, template, {'error_message': str(e)})



def start_mining():
    payload['method'] = "miner_start"
    payload['params'] = []
    requests.post(URL, data=json.dumps(payload), headers=headers)

def stop_mining():
    payload['method'] = "miner_stop"
    payload['params'] = []
    requests.post(URL, data=json.dumps(payload), headers=headers)