import tkinter as tk
from tkinter import ttk
from web3 import Web3

# Infura連接參數
infura_url = 'https://goerli.infura.io/v3/d97c786f20e34797aa30be5243b9e48a'
account_metamask = "0x70c9acB021A6Da74E685FD1f94a832dD5cB69f56" # metamask 帳號
contract_address = '0xe29ebc04057E8f52A031d56B0D2e5D7392361788'
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_tokenName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_tokenSupply",
				"type": "uint256"
			}
		],
		"name": "addToken",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_tokenName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_value",
				"type": "uint256"
			}
		],
		"name": "consume",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "tokenName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Consume",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "tokenName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "tokenSupply",
				"type": "uint256"
			}
		],
		"name": "TokenAdded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_tokenName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "tokenName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tokenNames",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "tokens",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "totalSupply",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# 使用Infura提供的節點連接到以太坊網絡
web3 = Web3(Web3.HTTPProvider(infura_url))

# 載入智能合約
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

nonce = web3.eth.getTransactionCount(account_metamask)

# Tkinter介面
root = tk.Tk()
root.title('能源貨幣系統')
root.geometry("500x450")  # 設定寬度高度

# 創建函式，以便從智能合約中新增貨幣
def Add_currency():
    token_name = TokenName_entry.get()
    amount = int(amount_entry.get())
    
    try:
                
        # 調用智能合约的 transfer 函式
        tx = contract.functions.addToken(token_name,amount).buildTransaction({
            'from': account_metamask, # 發送交易的帳戶地址
            'nonce': nonce, # 計數器
            'gas': 200000 # gas limit
        })
        
        # 私鑰對交易簽名
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "333d61c227f65b7e73f67f4fe80eabc5620349c139cb7d69fbdd2d6d5cc94327")  # 使用合约所有者的私鑰
        # 將已簽名的交易發送出去
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # 等待交易確認
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
		
        
        Add_label.config(text=f'已生成{token_name} 共計{amount}個')
    except Exception as e:
        Add_label.config(text=f'錯誤：{str(e)}')
        


# 創建函式，以便從智能合約中獲取傳貨幣餘額
def get_balance():
    address = address_entry.get()
    token_name = TokenName2_entry.get()
    try:
        balance = contract.functions.balanceOf(address,token_name).call()
        
        if balance:
            balance_label.config(text=f'{token_name} \n餘額：{balance}')
        else:
            balance_label.config(text=f'請輸入地址')
    except Exception as e:
        balance_label.config(text=f'錯誤：{str(e)}')
        

# 創建函式，以便從智能合約中執行轉帳
def transfer_tokens():
    from_address = from_entry.get()
    to_address = to_entry.get()
    amount = int(amount2_entry.get())
    token_name = TokenName3_entry.get()
    nonce = web3.eth.getTransactionCount(account_metamask)

    try:
                
        # 調用智能合约的 transfer 函式
        tx = contract.functions.transfer(from_address,to_address,token_name,amount).buildTransaction({
            'from': account_metamask, # 發送交易的帳戶地址
            'nonce': nonce, # 計數器
            'gas': 200000 # gas limit
        })
        
        # 私鑰對交易簽名
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "333d61c227f65b7e73f67f4fe80eabc5620349c139cb7d69fbdd2d6d5cc94327")  # 使用合约所有者的私鑰
        # 將已簽名的交易發送出去
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # 等待交易確認
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
		
       	from_balance = contract.functions.balanceOf(from_address,token_name).call()
        to_balance = contract.functions.balanceOf(to_address,token_name).call()
        
        balance_label2.config(text=f'{token_name} \n己方餘額：{from_balance}\n對方餘額：{to_balance}')
    except Exception as e:
        balance_label2.config(text=f'錯誤：{str(e)}')
# 創建函式，以便從智能合約中執行消耗
def consume_tokens():
    consume_address = consume_entry.get()
    consume_amount = int(consume_amount_entry.get())
    token_name = TokenName4_entry.get()
    nonce = web3.eth.getTransactionCount(account_metamask)

    try:
                
        #  調用智能合约的 consume 函式
        tx = contract.functions.consume(consume_address,token_name,consume_amount).buildTransaction({
            'from': account_metamask, # 發送交易的帳戶地址
            'nonce': nonce, # 計數器
            'gas': 200000 # gas limit
        })
        
        # 私鑰對交易簽名
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "333d61c227f65b7e73f67f4fe80eabc5620349c139cb7d69fbdd2d6d5cc94327")  # 使用合约所有者的私鑰
        # 將已簽名的交易發送出去
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # 等待交易確認
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
		
       	consume_balance = contract.functions.balanceOf(consume_address,token_name).call()
        
        balance_label3.config(text=f'{token_name} \n餘額：{consume_balance}')
    except Exception as e:
        balance_label3.config(text=f'錯誤：{str(e)}')

#查詢貨幣名稱
def search_tokenName():
    Num = int(TokenNum_entry.get())
    try:
        token_name = contract.functions.tokenNames(Num).call()

        search_label.config(text=f'{token_name}')
    except Exception as e:
        search_label.config(text=f'錯誤編號')

# Tkinter元件
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)


# 新增貨幣
page1 = ttk.Frame(notebook)
notebook.add(page1, text='新增貨幣')

frame = tk.Frame(page1)
frame.place(relx=0.5, rely=0.5, anchor='center')

TokenName_label = tk.Label(frame, text='貨幣名稱：')
TokenName_label.pack()

TokenName_entry = tk.Entry(frame)
TokenName_entry.pack()

amount_label = tk.Label(frame, text='總額：')
amount_label.pack()

amount_entry = tk.Entry(frame)
amount_entry.pack()

doit_button = tk.Button(frame, text='新增貨幣', command=Add_currency)
doit_button.pack(pady=10)

Add_label = tk.Label(frame, text='')
Add_label.pack()

# 檢視餘額
page2 = ttk.Frame(notebook)
notebook.add(page2, text='檢視餘額')

frame1 = tk.Frame(page2)
frame1.place(relx=0.5, rely=0.5, anchor='center')

address_label = tk.Label(frame1, text='地址：')
address_label.pack()

address_entry = tk.Entry(frame1)
address_entry.pack()

TokenName2_label = tk.Label(frame1, text='貨幣名稱：')
TokenName2_label.pack()

TokenName2_entry = tk.Entry(frame1)
TokenName2_entry.pack()

get_balance_button = tk.Button(frame1, text='檢視餘額', command=get_balance)
get_balance_button.pack(pady=10)

balance_label = tk.Label(frame1, text='\n')
balance_label.pack()

# 執行轉帳
page3 = ttk.Frame(notebook)
notebook.add(page3, text='執行轉帳')

frame2 = tk.Frame(page3)
frame2.place(relx=0.5, rely=0.5, anchor='center')

TokenName3_label = tk.Label(frame2, text='貨幣名稱：')
TokenName3_label.pack()

TokenName3_entry = tk.Entry(frame2)
TokenName3_entry.pack()


from_label = tk.Label(frame2, text='轉出地址：')
from_label.pack()

from_entry = tk.Entry(frame2)
from_entry.pack()

to_label = tk.Label(frame2, text='轉入地址：')
to_label.pack()

to_entry = tk.Entry(frame2)
to_entry.pack()

amount2_label = tk.Label(frame2, text='轉帳數量：')
amount2_label.pack()

amount2_entry = tk.Entry(frame2)
amount2_entry.pack()

transfer_button = tk.Button(frame2, text='執行轉帳', command=transfer_tokens)
transfer_button.pack(pady=10)

balance_label2 = tk.Label(frame2, text='\n\n')
balance_label2.pack()

# 消耗能源
page4 = ttk.Frame(notebook)
notebook.add(page4, text='消耗能源')

frame3 = tk.Frame(page4)
frame3.place(relx=0.5, rely=0.5, anchor='center')

TokenName4_label = tk.Label(frame3, text='貨幣名稱：')
TokenName4_label.pack()

TokenName4_entry = tk.Entry(frame3)
TokenName4_entry.pack()

consume_label = tk.Label(frame3, text='消費地址：')
consume_label.pack()

consume_entry = tk.Entry(frame3)
consume_entry.pack()

consume_amount_label = tk.Label(frame3, text='消耗數量：')
consume_amount_label.pack()

consume_amount_entry = tk.Entry(frame3)
consume_amount_entry.pack()

consume_button = tk.Button(frame3, text='消耗能源', command=consume_tokens)
consume_button.pack(pady=10)

balance_label3 = tk.Label(frame3, text='\n')
balance_label3.pack()

# 查詢貨幣名稱
page5 = ttk.Frame(notebook)
notebook.add(page5, text='查詢貨幣名稱')

frame4 = tk.Frame(page5)
frame4.place(relx=0.5, rely=0.5, anchor='center')

TokenNum_label = tk.Label(frame4, text='貨幣生成編號：')
TokenNum_label.pack()

TokenNum_entry = tk.Entry(frame4)
TokenNum_entry.pack()

search_button = tk.Button(frame4, text='查詢', command=search_tokenName)
search_button.pack(pady=10)

search_label = tk.Label(frame4, text='')
search_label.pack()

root.mainloop()

if name == 'main':
    app.run()
