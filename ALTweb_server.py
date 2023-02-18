from m5stack import *
from uiflow import *
from m5ui import *
import wifiCfg
import socket

from ALTutils import urlDecode, extract_string
from ALTwidgets import Alert


def get_user_input(SSID, password):
    ip = wifiCfg.wlan_sta.ifconfig()

    wifiCfg.doConnect(SSID, password)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip[0], 80))
    s.listen(5)

    msg = ''
    if not wifiCfg.wlan_sta.isconnected():
        return ''

    Alert('Type https://' + str(ip[0]) + '/ in Your Browser', 0x000000, '', 0x000000, 0xFFFFFF, None, None)

    conn, addr = s.accept()
    request = conn.recv(1024)
    request = urlDecode(str(request))
    user_input = extract_string(request, '?input=')

    response = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>User Input Page</title>
    <style>
      /* CSS styles */
      body {
        font-family: Arial, sans-serif;
        background-color: #f8f8f8;
        margin: 0;
      }

      .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 40px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
      }

      h1 {
        font-size: 32px;
        margin-bottom: 20px;
      }

      input[type="text"] {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border: 2px solid #ccc;
        border-radius: 4px;
        font-size: 16px;
        transition: border-color 0.3s;
      }

      input[type="text"]:focus {
        outline: none;
        border-color: dodgerblue;
      }

      .btn {
        background-color: dodgerblue;
        color: #fff;
        border: none;
        padding: 12px 24px;
        border-radius: 4px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
      }

      .btn:hover {
        background-color: #0066cc;
      }

      .error {
        border-color: red;
      }

      .datetime {
        font-size: 20px;
        margin-top: 40px;
        color: #555;
      }

      .time {
        font-weight: bold;
        color: dodgerblue;
        font-size: 36px;
        margin-bottom: 10px;
      }

      .date {
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 18px;
        color: #999;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Enter your input:</h1>
      <form id="myForm">
        <input type="text" id="userInput" placeholder="Your input here...">
        <button class="btn" type="submit">Submit</button>
      </form>
    </div>
    <script>
      function submitInput(event) {
        event.preventDefault();
        const userInput = document.getElementById("userInput");
        const u_input = userInput.value;
        if (u_input === "") {
          userInput.classList.add("error");
          userInput.setAttribute("placeholder", "Please enter your input");
        } else {
          window.location.href = window.location.href + "?input=" + encodeURIComponent(u_input);
        }
      }

      function updateTime() {
        const now = new Date();
        const time = now.toLocaleTimeString([], {
          hour: "numeric",
          minute: "2-digit",
          hour12: true
        });
        const date = now.toLocaleDateString([], {
          weekday: "long",
          year: "numeric",
          month: "long",
          day: "numeric"
        });
        document.getElementById("currentTime").innerHTML = time;
        document.getElementById("currentDate").innerHTML = date;
      }
      setInterval(updateTime, 1000); // call updateTime every second
      document.getElementById("myForm").addEventListener("submit", submitInput);
    </script>
  </body>
    '''
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

    return user_input
