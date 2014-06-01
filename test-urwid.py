import urwid

def handle_input(key):
    if key == 'esc':
        raise urwid.ExitMainLoop()
    if key == 'enter':
        if listBox.focus_position > 1:
            listWalker.insert(listBox.focus_position + 1, urwid.Edit("Enter a keyword to listen to: "))



body = [urwid.Text('Hello!'), urwid.Divider()]
body.append(urwid.Edit("Enter device name: "))

listWalker = urwid.SimpleFocusListWalker(body)
listBox = urwid.ListBox(listWalker)
boxAdapter = urwid.BoxAdapter(listBox, 50)

text = urwid.Text('Connected devices')
columns = urwid.Columns([('weight', 2, boxAdapter), ('weight', 1, text)], 5)
fill = urwid.Filler(columns, 'top')

loop = urwid.MainLoop(fill, event_loop=urwid.TwistedEventLoop(), unhandled_input=handle_input)
loop.run()