from qpid.messaging import Connection, MessagingError, Message
from qpid.messaging.message import TYPE_MAPPINGS


class FanoutPublisher(object):
    """
    qpid fanout publisher
    """

    def __init__(self, broker, address):
        self.broker = broker
        self.address = address
        self.connection = None
        self.session = None
        self.sender = None
        self.heartbeat_sender = None

    def __del__(self):
        self.destroy()

    def init(self):
        self.connection = Connection(self.broker, reconnect=True, reconnect_interval=3)
        try:
            self.connection.open()
            self.session = self.connection.session()
            self.sender = self.session.sender(self.address)
        except MessagingError:
            print (traceback.format_exc())
            return False

        return True

    def destroy(self):
        if self.connection:
            self.connection.close()

    def publish(self, message):
        if self.sender is None:
            if not self.init():
                return False
        try:
            message.properties = {'x-amqp-0-10.routing-key': self.address}
            self.sender.send(message)
            print('publish info. broker: {}, reply_to: {}'.format(self.broker, self.address))
        except MessagingError:
            print(traceback.format_exc())
            return False

        return True

qb_msg = {'LIST': [
        {
        'UPDATE_TIME': '2016-11-30 10:33:35',
        'DATA_SOURCE': 'XIGNITE',
        'SYMBOL': 'USDCNY',
        'ASK_PRICE': 6.884,
        'SPREAD': 0.0006,
        'SN': 9713930,
        'BID_PRICE': 6.8834},
        {
        'UPDATE_TIME': '2016-11-30 10:33:36',
        'DATA_SOURCE': 'XIGNITE',
        'SYMBOL': 'USDCNY',
        'ASK_PRICE': 6.885,
        'SPREAD': 0.0007,
        'SN': 9713931,
        'BID_PRICE': 6.8835
        }
        ]
    }


if __name__ == '__main__':
    publisher = FanoutPublisher('192.168.1.234', 'fxspot.cdh2qb.push.fanout.test')
    publisher.publish(Message(content=qb_msg, content_type=TYPE_MAPPINGS[dict]))
    publisher.destroy()
    print 'done.'
