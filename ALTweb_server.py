import socket
from urllib.parse import urlparse, parse_qs
import wifiCfg
from ALTconnection import *
from ALTutils import urlDecode, extract_string
from ALTwidgets import Alert


def get_user_input(port=80, alert_msg = 'Navigate to:'):
    check_connection()
    
    ip = wifiCfg.wlan_sta.ifconfig()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip[0], port))
    s.listen(5)

    print(alert_msg + ' http://' + str(ip[0]) + ':' + str(port) + '/submit')

    while 1:
        input_var = None
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = urlDecode(str(request))
        parsed_url = urlparse(extract_string(request, 'GET '))
        requested_path = parsed_url.path
        if requested_path == '/submit':
            input_var = parse_qs(parsed_url.query).get('input', [None])[0]
            if input_var:
                html_file = open("./Assets/HTML/submitted.html", "r")
                response = html_file.read()
            else:
                html_file = open("./Assets/HTML/submit.html", "r")
                response = html_file.read()
        elif requested_path == '/favicon.ico':
            html_file = open("./Assets/HTML/favicon.ico", "rb")
            response = html_file.read()
        else:
            html_file = open("./Assets/HTML/not_found.html", "r")
            response = html_file.read()

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        
        if input_var:
            s.close()
            return input_var
