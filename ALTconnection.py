import wifiCfg


def connect_wifi(ssid, password):
    """
    A wrapper function for wifiCfg.doConnect(ssid, password).
    In this function we print an informative message in the terminal in the cases of success
    and failure. We override the error raise in the original function.

    Parameters
    ----------
    ssid : str
        The Wi-Fi network name.
    password : str
        The Wi-Fi network password.

    Returns
    -------
    True/False
        True in case of connection success and False otherwise.
    """
    try:
        wifiCfg.doConnect(ssid, password)
        print('Connection Established')
        return True
    except Exception as e:
        print("Can't Connect to WIFI : " + str(e), 0, 0, 0x000)
        return False


def check_connection():
    """
    A wrapper function for wifiCfg.isConnected().
    Raises an exception if Wi-Fi isn't connected instead of returning False.

    Raises
    -------
    In case of no internet connection.
    """
    if not wifiCfg.is_connected():
        raise Exception(__name__ + ": No internet connection.")
  