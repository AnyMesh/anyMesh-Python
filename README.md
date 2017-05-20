NOTE: AnyMesh is no longer under active development or support.

#AnyMesh
https://github.com/AnyMesh


AnyMesh is a multi-platform, decentralized, auto-discovery, auto-connect mesh networking API.

Current supported platforms:

* Node.js
* iOS
* Python

AnyMesh makes it easy to build a decentralized, multi-platform mesh network on any LAN, without having to manually implement TCP / UDP processes.

All supported platforms work roughly the same way.  Configure each AnyMesh instance with 2 properties:

* Name - a name or identifier for the instance
* Subscriptions - an array of keywords for your instance to listen for

> AnyMesh will automatically find and connect to other AnyMesh
> instances.

Then, to communicate across the network, an instance can send two types of messages:

* Request - send a message to a specific device Name.
* Publish - send a message associated with a keyword.  Any other instance that subscribes to the keyword will receive the message.

That's all there is to it!
## FAQ

### Q: So what is AnyMesh?
A: AnyMesh is a convenient, powerful way to get multiple programs to connect and send information to one another.
Each instance of AnyMesh will automatically find and connect to other instances.  AnyMesh instances can be running within the same app,
on separate apps on the same device, or on different devices within the same local network (LAN).

A network can contain any combination of these relationships, across any languages or platforms -
You may have a Mac OSX desktop computer running 2 instances of AnyMesh-Python alongside 1 instance of AnyMesh-Node.  These instances are
also connected to 2 more instances of AnyMesh-Node on a Linux computer down the hall, and a Raspberry Pi running AnyMesh-Python hardwired into the router.
Launch an app on your iPhone that uses AnyMesh-iOS, and instantly connect to all these devices automatically!

### Q: Why use AnyMesh instead of RabbitMQ, 0MQ, etc?
A: AnyMesh is certainly not the first mesh networking API on the block.  But AnyMesh was created with a few unique purposes in mind that sets it apart
from other libraries:

* AnyMesh is truly decentralized - Even at the lowest levels of the TCP connections, there is NO device acting as any kind of server or relay.
All AnyMesh instances manage their own connections to every other device.  This means any device can enter or leave the mesh at any time with ZERO disruption
to any other connections.
* AnyMesh has EXTREMELY minimal setup and configuration - Just name your instance and optionally give it some keywords to subscribe to.  There is no need to define roles for instances -
Every instance uses the same simple message distribution pattern.
* AnyMesh is multi-platform - We currently support iOS, Python, and Node.  We hope to start work on Java/Android very soon.


### Q: How can I help?
A: AnyMesh is still very young concept, and although it is fully functional, it will be a little while until we reach v.1.0 on all supported
platforms.  See the CONTRIBUTE.md file for suggestions on contributing to development.
#AnyMesh Python
## Please Read:
11/4/2014 - 0.4.0 has been released!  See CHANGELOG for details.

AnyMesh Python uses the venerable Twisted library to handle asynchronous networking processes.  
Download and install Twisted here: https://twistedmatrix.com/trac/

##Installation
	pip install anymesh

##Quickstart:
Create an AnyMesh Object:

    any_mesh = AnyMesh('Dave', ['status', 'alerts'], delegate)

The "delegate" variable in the constructor above should be a subclass of AnyMeshDelegateProtocol.  Here's an example:

    class AmDelegate(AnyMeshDelegateProtocol)
      def connected_to(self, anymesh, device_info):
        print "connected to " + device_info.name
        for subscription in device_info.subscriptions:
          print subscription

      def disconnected_from(self, anymesh, name):
        print "disconnected from " + name

      def received_msg(self, anymesh, message):
        print "received message from " + message.sender
        print "message: " + json.dumps(message.data)

Start the Twisted Event Loop:

    any_mesh.run();

Send a request:

    any_mesh.request("Bob", {"msg":"Hello Bob", "priority":1})

Publish to subscribers:

    any_mesh.publish("updates", {"update":"new headlines!", "content":[1, 5, 8]})


### A few more helpful methods:    

Get info on current connections:

    var connectionsList = any_mesh.get_connections()

Change your anymesh instance's subscriptions:

	any_mesh.update_subscriptions(['weather', 'sports'])

Define a callback in your delegate to be notified of another anymesh's subscription change:

	def received_updated_subscriptions(self, anymesh, subscriptions, name):
		print name + "updated their subscriptions!"
		for subscription in subscriptions:
          print subscription


## Some notes on Twisted:
AnyMesh Python uses Twisted's Reactor run loop.  If your app needs to integrate its own event loops, you have a couple of options:
* Schedule repeating tasks on Twisted's reactor: https://twistedmatrix.com/documents/12.0.0/core/howto/time.html
* Run your event loop on a separate thread.

If possible, I would recommend the former, as long as your tasks do not block the event loop for too long.

## Still need help?
Check out the unit tests and the example app to see AnyMesh in action.
###AnyMesh software is licensed with the MIT License

###Any questions, comments, or suggestions, contact the Author:
Dave Paul
davepaul0@gmail.com
