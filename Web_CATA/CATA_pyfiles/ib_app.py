from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer

class IbApp(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId , errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId ):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract = Contract()
        contract.symbol = self.sec_id
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        order = Order()
        order.action = self.buy_or_sell
        order.totalQuantity = self.qty
        order.orderType = "MKT"


        self.placeOrder(self.nextOrderId, contract, order)

    def set_order_attributes(self, sec_id, buy_or_sell, qty):

        self.sec_id = sec_id
        self.buy_or_sell = buy_or_sell
        self.qty = qty

    def stop(self):
        self.done = True
        self.disconnect()

    def main(self):

        self.nextOrderId = 0
        self.connect("127.0.0.1", 7497, 9)

        Timer(3, self.stop).start()
        self.run()

