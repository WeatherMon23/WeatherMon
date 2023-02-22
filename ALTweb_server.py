from urllib.parse import urlparse, parse_qs
import socket
import wifiCfg
import network
from ALTconnection import *
from ALTutils import urlDecode, extract_string


def get_user_input(port=80, alert_msg='Navigate to:', AP=False):
    """
    Hosts a webpage on the specified port to gather user input

    Parameters
    ----------
    port : int
        Number of port to be used for connection (default : 80)
    alert_msg : msg
        Alert message to be displayed to the user (default : 'Navigate to:')
    AP : bool
        Access Point mode (default : False)
    Returns
    -------
    The string submitted by the user
    """
    ip = ['192.168.4.1']
    if AP:
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid='ESP32')
        ap.config(authmode=3, password='123456789')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip[0], port))

    else:
        check_connection()
        ip = wifiCfg.wlan_sta.ifconfig()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip[0], port))
    s.listen(5)

    print(alert_msg + ' http://' + str(ip[0]) + ':' + str(port) + '/submit')

    while 1:
        status_code = '200 OK'
        input_var = None
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = urlDecode(str(request))
        parsed_url = urlparse(extract_string(request, 'GET '))
        requested_path = parsed_url.path
        if requested_path == '/submit':
            input_var = parse_qs(parsed_url.query).get('input', [None])[0]
            if input_var:
                with open("./Assets/HTML/submitted.html", "r") as html_file:
                    response = html_file.read()
            else:
                with open("./Assets/HTML/submit.html", "r") as html_file:
                    response = html_file.read()
        elif requested_path == '/favicon.ico':
            with open("./Assets/HTML/favicon.ico", "rb") as html_file:
                response = html_file.read()
        else:
            with open("./Assets/HTML/not_found.html", "r") as html_file:
                response = html_file.read()
            status_code = '404 Not Found'

        conn.send('HTTP/1.1 {}\n'.format(status_code))
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

        if input_var:
            s.close()
            return input_var
