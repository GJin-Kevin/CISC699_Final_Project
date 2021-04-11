from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print('Error: {}, Error Code: {}, Error Detail: {}'.format(reqId, errorCode, errorString))

    def contractDetailes(self, reqId, contractDetails):
        print("Contract Details: {}, {}".format(reqId, contractDetails))



def main():

    app = TestApp()
    
    app.connect("127.0.0.1", 7497, 0)

    contract = Contract()

    contract.symbol = "AAPL"
    contract.secType = "STK" 
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.primaryExchange = 'NASDAQ'

    app.reqContractDetails(1, contract)

    app.run()


if __name__ == "__main__":
    main()

    print('done')