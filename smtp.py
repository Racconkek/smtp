import socket
import ssl
import base64
import sys

target = "Raccoon-kek@yandex.ru"

user_name = 'Raccoon-kek@yandex.ru'
password = 'belladonna'

def request(socket, request):
    socket.send((request + '\n').encode())
    recv_data = socket.recv(65535).decode()
    return recv_data


host_addr = 'smtp.yandex.ru'
port = 465


def read_msg():
    with open('source\msg.txt', 'rb') as file:
        return base64.b64encode(file.read()).decode()
        # return base64.b64encode('\n'.join(file.readlines()).encode()).decode()
        # return '\n'.join(file.readlines())


def read_pict(filename):
    with open("source\\" + filename, 'rb') as file:
        return base64.b64encode(file.read()).decode()


# def create_msg():
#     head = ""
#     head += "From: " + user_name + '\n'
#     head += "To: " + target + '\n'
#     head += "Subject: " + "=?utf-8?B?" + base64.b64encode("Тестовое письмо".encode()).decode() + "?=" + '\n'
#     head += "MIME-Version: 1.0" + '\n'
#     bound = "bound123456789"
#     head += 'Content-Type: multipart/mixed; boundary="' + bound + '"' + '\n'
#     head += "\n"
#     body = ""
#     body += "--" + bound + '\n'
#     body += "Content-Transfer-Encoding: 7bit" + '\n'
#     body += "Content-Type: text/plain" + '\n' + '\n'
#     body += read_msg() + '\n'
#     body += "--" + bound + '\n'
#     body += 'Content-Disposition: attachment; filename="icon.png"' \
#             '\nContent-Transfer-Encoding: base64' \
#             '\nContent-Type: image/png; name="icon.png"' + '\n' + '\n'
#     body += read_pict("icon.png") + '\n'
#     body += "--" + bound + '--' + '\n'
#     body += '.' + '\n'
#     return head + body


def create_head(user, target, subject, bound):
    head = ""
    head += "From: " + user + '\n'
    head += "To: " + target + '\n'
    head += "Subject: " + "=?utf-8?B?" + base64.b64encode(subject.encode()).decode() + "?=" + '\n'
    head += "MIME-Version: 1.0" + '\n'
    # bound = "bound123456789"
    head += 'Content-Type: multipart/mixed; boundary="' + bound + '"' + '\n'
    head += "\n"

    return head

def create_body(bound, attachments):
    body = ""
    body += "--" + bound + '\n'
    body += "Content-Type: text/plain; "
    body += 'charset="UTF-8"' + '\n'
    body += "Content-Transfer-Encoding: base64 " + '\n' + '\n'
    body += read_msg() + '\n'

    for attach in attachments:
        body += "--" + bound + '\n'
        body += 'Content-Disposition: attachment; filename="' + attach + '"' \
                '\nContent-Transfer-Encoding: base64' \
                '\nContent-Type: image/png; name="icon.png"' + '\n' + '\n'
        body += read_pict(attach) + '\n'

    body += "--" + bound + '--' + '\n'
    body += '.' + '\n'

    return body

def create_message(user, target, subject, attachments):
    bound = "bound123456789"
    return create_head(user, target, subject, bound)+create_body(bound, attachments)

def parse_configs():
    user = ''
    targets = None
    passwd = ''
    subject = ''
    attachments = None
    with open('source\configs.txt', encoding='utf-8') as file:
        for line in file:
            # line = line.decode('utf-8')
            if line.find("from:") == 0:
                user = line.split(' ')[1].strip()
                print(user)
            if line.find("to:") == 0:
                targets = line[4:].strip().split(' ')
                print(targets)
            if line.find("password:") == 0:
                passwd = line.split(' ')[1].strip()
                print(passwd)
            if line.find("subject:") == 0:
                subject = line.split(' ')[1].strip()
                print(subject)
            if line.find("attachments:") == 0:
                attachments = line[13:].strip().split(' ')
                print(attachments)
        if user == '' or targets is None or passwd == '':
            sys.exit(-1)
        return user, passwd, subject, targets, attachments

def send_letter(user, passwd, subject, targets, attachments):
    for t in targets:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host_addr, port))
            client = ssl.wrap_socket(client)
            print(client.recv(1024))
            print(request(client, 'ehlo Ivan'))
            base64login = base64.b64encode(user.encode()).decode()
            base64password = base64.b64encode(passwd.encode()).decode()
            print(request(client, 'AUTH LOGIN'))
            print(request(client, base64login))
            print(request(client, base64password))
            print(request(client, 'MAIL FROM: ' + user))
            print(request(client, "RCPT TO: " + t))
            print(request(client, 'DATA'))
            print(request(client, create_message(user, t, subject, attachments)))

def main():
    user, passwd, subject, targets, attachments = parse_configs()
    send_letter(user, passwd, subject, targets, attachments)
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    #     client.connect((host_addr, port))
    #     client = ssl.wrap_socket(client)
    #     print(client.recv(1024))
    #     print(request(client, 'ehlo Ivan'))
    #     base64login = base64.b64encode(user_name.encode()).decode()
    #
    #     base64password = base64.b64encode(password.encode()).decode()
    #     print(request(client, 'AUTH LOGIN'))
    #     print(request(client, base64login))
    #     print(request(client, base64password))
    #     print(request(client, 'MAIL FROM: ' + user_name))
    #     print(request(client, "RCPT TO: " + target))
    #     print(request(client, 'DATA'))
    #     print(request(client, create_msg()))


if __name__ == '__main__':
    main()
