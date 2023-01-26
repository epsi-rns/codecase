import paho.mqtt.client as mqtt

# This is the Subscriber
class mqSubscriber:
  def on_connect(self,
      client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/test")

  def on_message(self,
      client, userdata, msg):
    float_num = float(msg.payload.decode())
    print("%.2f" % float_num)

  def main(self):
    client = mqtt.Client()
    client.connect("localhost",1883,60)

    client.on_connect = self.on_connect
    client.on_message = self.on_message

    client.loop_forever()

mqSub = mqSubscriber()
mqSub.main()
