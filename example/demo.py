import sys
sys.path.append('../')
import urwid
from anymesh import AnyMesh, AnyMeshDelegateProtocol, MeshMessage, MeshDeviceInfo

# DELEGATE CLASS FOR ANYMESH
class AmDelegate(AnyMeshDelegateProtocol):
    def connected_to(self, anymesh, device_info):
        msg_list_box.add_line('connected to ' + device_info.name)

    def disconnected_from(self, anymesh, name):
        msg_list_box.add_line('disconnected from ' + name)

    def received_msg(self, anymesh, message):
         if 'msg_list_box' in globals():
            msg_list_box.add_line('Message from ' + message.sender, message.data['msg'])


#FUNCTION TO START ANYMESH.  WE DON'T CALL .RUN BECAUSE URWID HAS STARTED THE TWISTED REACTOR FOR US
def start_anymesh(name, listens_to):
    global delegate, any_mesh
    delegate = AmDelegate()
    if 'any_mesh' not in globals():
        any_mesh = AnyMesh(name, listens_to, delegate)

def handle_input(key):
    if key == 'esc':
        raise urwid.ExitMainLoop()


class SetupListBox(urwid.ListBox):
    def __init__(self):
        body = [urwid.Text('Setup your Mesh Instance'), urwid.Divider(), urwid.Edit("Enter device name: ")]
        super(SetupListBox, self).__init__(urwid.SimpleFocusListWalker(body))

    def keypress(self, size, key):
        key = super(SetupListBox, self).keypress(size, key)
        if key == 'enter':
            if self.focus_position > 2 and len(self.body[self.focus_position].edit_text) == 0:
                device_name = self.body[2].edit_text
                device_listens = []
                for index, item in enumerate(self.body):
                    if index > 2:
                        device_listens.append(item.edit_text)
                start_anymesh(device_name, device_listens)
                load_msg_frame()

            else:
                self.body.insert(self.focus_position + 1, urwid.Edit("Enter a keyword to listen to: "))
                self.focus_position += 1
        elif key == 'esc':
            raise urwid.ExitMainLoop()


class MessageListBox(urwid.ListBox):
    def __init__(self):
        body = [urwid.Text('Message Log'), urwid.Divider()]
        super(MessageListBox, self).__init__(urwid.SimpleListWalker(body))

    def add_line(self, text_to_add, second_line=None):
        if second_line is not None:
            self.body.append(urwid.Divider())
        self.body.append(urwid.Text(text_to_add))
        if second_line is not None:
            self.body.append(urwid.Text(second_line))
            self.body.append(urwid.Divider())
        self.set_focus(self.focus_position + 1)
        if second_line is not None:
            self.set_focus(self.focus_position + 3)
        refresh_device_column()
        loop.draw_screen()


class MsgEntryListBox(urwid.ListBox):
    def __init__(self):
        body = [urwid.Edit("Target:"), urwid.Edit("Message:"), urwid.Button("Request", self.req_pressed), urwid.Button("Publish", self.pub_pressed)]
        super(MsgEntryListBox, self).__init__(urwid.SimpleFocusListWalker(body))

    #THESE TWO ACTIONS WILL CAUSE ANYMESH TO SEND A MESSAGE - EITHER A PUBLISH OR A REQUEST
    def req_pressed(self, something):
        target = self.body[0].edit_text
        message = {"msg": self.body[1].edit_text}
        any_mesh.request(target, message)
        msg_list_box.add_line('Sending request', message['msg'])

    def pub_pressed(self, something):
        target = self.body[0].edit_text
        message = {"msg": self.body[1].edit_text}
        any_mesh.publish(target, message)
        msg_list_box.add_line('Publishing message', message['msg'])


def load_msg_frame():
    global frame, entry_box, msg_list_box
    msg_list_box = MessageListBox()
    entry_box = MsgEntryListBox()
    frame.body = msg_list_box
    frame.footer = urwid.BoxAdapter(entry_box, 7)
    frame.focus_position = 'footer'
    entry_box.set_focus(0)

def refresh_device_column():
    options = ('pack', None)
    device_list = [(urwid.Text("Connected Devices"), options), (urwid.Divider(), options)]
    for device in any_mesh.get_connections():
        device_list.append((urwid.Text(device.name), options))
    device_pile.contents = device_list

frame = urwid.Frame(SetupListBox())
device_pile = urwid.Pile([urwid.Text("Connected Devices")])
columns = urwid.Columns([('weight', 2, urwid.BoxAdapter(frame, 50)), ('weight', 1, device_pile)], 5)
fill = urwid.Filler(columns, 'top')

tLoop = urwid.TwistedEventLoop()
loop = urwid.MainLoop(fill, event_loop=tLoop, unhandled_input=handle_input)
loop.run()