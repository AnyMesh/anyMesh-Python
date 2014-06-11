#AnyMesh

AnyMesh is a multi-platform, decentralized, auto-discovery, auto-connect mesh networking API.  

Current supported platforms:

* Node.js
* iOS
* Python

AnyMesh makes it easy to build a decentralized, multi-platform mesh network on any LAN, without having to manually implement TCP / UDP processes.

All supported platforms work roughly the same way.  Configure each AnyMesh instance with 2 properties:

* Name - a name or identifier for the device / program
* ListensTo - an array of "subscriptions"

> AnyMesh will automatically find and connect to other AnyMesh
> instances.  (One AnyMesh instance per network adapter / IP address.)

Then, to communicate across the network, an instance can send two types of messages:

* Request - send a message to a specific device Name.
* Publish - send a message to any subscriber of your message's "target".

That's all there is to it!

#AnyMesh Python

AnyMesh Python uses the venerable Twisted library to handle asynchronous networking processes.  
Download and install Twisted here: https://twistedmatrix.com/trac/


##Quickstart:
Create an AnyMesh Object:

    any_mesh = AnyMesh('Dave', ['status', 'alerts'], delegate)

The "delegate" variable in the constructor above should be a subclass of AnyMeshDelegateProtocol.  Here's an example:

    class AmDelegate(AnyMeshDelegateProtocol)
      def connected_to(self, device_info):
        print "connected to " + device_info.name
        for subscription in device_info.listens_to:
          print subscription

      def disconnected_from(self, name):
        print "disconnected from " + name

      def received_msg(self, message):
        print "received message from " + message.sender
        print "message: " + json.dumps(message.data)

Start the Twisted Event Loop:

    any_mesh.run();

Send a request:

    any_mesh.request("Bob", {"msg":"Hello Bob", "priority":1});

Publish to subscribers:

    any_mesh.publish("updates", {"update":"new headlines!", "content":[1, 5, 8]});


## Some notes on Twisted:
AnyMesh Python uses Twisted's Reactor run loop.  If your app needs to integrate its own event loops, you have a couple of options:
* Schedule repeating tasks on Twisted's reactor: https://twistedmatrix.com/documents/12.0.0/core/howto/time.html
* Run your event loop on a separate thread.

If possible, I would recommend the former, as long as your tasks do not block the event loop for too long.

###Any questions, comments, or suggestions, e-mail me (Dave) at davepaul0@gmail.com!





> Written with [StackEdit](https://stackedit.io/).
