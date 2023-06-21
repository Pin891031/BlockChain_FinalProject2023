# 區塊練期末/能源貨幣系統
## 摘要
### 動機
$~~~~~~~~$能源貨幣理論是指亨利·福特（Henry Ford）提出的一種關於貨幣和能源之間關係的理論。福特是20世紀初期的美國汽車製造商和工業家，他認為能源是經濟運作的核心，貨幣只是其中的一種媒介。\
$~~~~~~~~$本計畫希望將能源進行量化，方便進行計算實際消耗額度，也可以將能源當作貨幣進行交易。
## 開始使用
安裝web3套件，打開命令提示字元輸入
```
pip install web3 == 5.24.0
```
#### 修改GUI,py檔案
* 在Infura上新增web3節點，選擇乙太坊中的Goerli複製連結貼到程式第6行引號中
* 將你要運行智能合約的metamask錢包地址貼到程式第7行引號中
* 將你要運行智能合約的metamask錢包私鑰貼到程式第40,87,117行引號中
* 將智能合約放到Remix上面編譯並將ABI貼到程式第9行中括號中
#### 運行步驟
將智能合約FPver7.sol佈署到Goerli test net上\
點擊GUI.py執行python檔或使用命令提示字元執行
## 成果展示
### GUI展示
##### 新增貨幣
![image](https://github.com/Pin891031/BlockChain_FinalProject2023/blob/main/sample%20IMG/GUI_1.PNG)
##### 檢視餘額
![image](https://github.com/Pin891031/BlockChain_FinalProject2023/blob/main/sample%20IMG/GUI_2.PNG)
##### 執行轉帳
![image](https://github.com/Pin891031/BlockChain_FinalProject2023/blob/main/sample%20IMG/GUI_3.PNG)
##### 消耗能源
![image](https://github.com/Pin891031/BlockChain_FinalProject2023/blob/main/sample%20IMG/GUI_4.PNG)
##### 查詢貨幣名稱
![image](https://github.com/Pin891031/BlockChain_FinalProject2023/blob/main/sample%20IMG/GUI_5.PNG)
### Remix上智能合約輸入欄位
![image](https://github.com/Pin891031/BlockChain_FinalProject2023/blob/main/sample%20IMG/remix.PNG)
## 程式碼
### 智能合約
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyToken {
    struct Token {
        string name;
        uint256 totalSupply;
    }
    
    mapping(address => mapping(string => uint256)) public balanceOf;
    mapping(string => Token) public tokens;
    string[] public tokenNames;
    
    event Transfer(address indexed from, address indexed to, string tokenName, uint256 value);
    event Consume(address indexed to, string tokenName, uint256 value);
    event TokenAdded(string tokenName, uint256 tokenSupply);

    constructor() {}

    function addToken(string memory _tokenName, uint256 _tokenSupply) public {
        require(tokens[_tokenName].totalSupply == 0, "Token already exists");
        tokens[_tokenName] = Token(_tokenName, _tokenSupply);
        tokenNames.push(_tokenName);
        balanceOf[msg.sender][_tokenName] = _tokenSupply;
        emit TokenAdded(_tokenName, _tokenSupply);
    }

    function transfer(address _from, address _to, string memory _tokenName, uint256 _value) public returns (bool) {
        require(balanceOf[_from][_tokenName] >= _value, "Insufficient balance");
        balanceOf[_from][_tokenName] -= _value;
        balanceOf[_to][_tokenName] += _value;
        emit Transfer(_from, _to, _tokenName, _value);
        return true;
    }

    function consume(address _addr, string memory _tokenName, uint256 _value) public returns (bool) {
        require(balanceOf[_addr][_tokenName] >= _value, "Insufficient balance");
        balanceOf[_addr][_tokenName] -= _value;
        tokens[_tokenName].totalSupply -= _value;
        emit Consume(_addr, _tokenName, _value);
        return true;
    }
}

```
### GUI
```python
import tkinter as tk
from tkinter import ttk
from web3 import Web3

# Infura連接參數
infura_url = '' #Infura節點
account_metamask = "" # metamask 帳號address
contract_address = '' #合約地址
contract_abi = [] #智能合約的ABI

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
    nonce = web3.eth.getTransactionCount(account_metamask)
    
    try:
                
        # 調用智能合约的 transfer 函式
        tx = contract.functions.addToken(token_name,amount).buildTransaction({
            'from': account_metamask, # 發送交易的帳戶地址
            'nonce': nonce, # 計數器
            'gas': 200000 # gas limit
        })
        
        # 私鑰對交易簽名
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "")  # 使用合约所有者的私鑰
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
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "")  # 使用合约所有者的私鑰
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
        signed_tx = web3.eth.account.sign_transaction(tx, private_key = "")  # 使用合约所有者的私鑰
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
```
## 參考資料
* [能源貨幣理論](https://news.cnyes.com/news/id/4727133)
* [Python Tkinter 實作GUI](https://codingsean.wordpress.com/2020/07/17/python-tkinter/)
* [Solidity製作參考](https://ithelp.ithome.com.tw/users/20092025/ironman/1759?page=1)
