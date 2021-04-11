from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum



class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        EWrapper.__init__(self)

    def error(self, reqId, errorCode, errorString):
        print('Error: {}, Error Code: {}, Error Detail: {}'.format(reqId, errorCode, errorString))

    def contractDetailes(self, reqId, contractDetails):
        print("Contract Details: {}, {}".format(reqId, contractDetails))

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Tic Id: {}, tickType: {}, price: {}.".format(reqId, TickTypeEnum.to_str(tickType), price))

    def tickSize(self, reqId, tickType, size):
        print('Tick Size. Ticker Id: {}'.format(reqId))

def main():

    app = TestApp()
    
    app.connect("127.0.0.1", 7497, 0)

    contract = Contract()

    contract.symbol = "AAPL"
    contract.secType = "STK" 
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.primaryExchange = 'NASDAQ'

    app.reqMarketDataType(4)
    app.reqMktData(1, contract, "", False, False, [])

    app.run()


if __name__ == "__main__":
    main()

    print('done')