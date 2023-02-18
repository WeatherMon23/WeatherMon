# WeatherMon

[![GitHub Release](https://img.shields.io/github/release/WeatherMon23/WeatherMon)](https://github.com/WeatherMon23/WeatherMon/releases/Latest)
[![MicroPython](https://img.shields.io/badge/MicroPython-1.12-brightgreen)](https://docs.micropython.org/en/v1.12/)
[![LVGL](https://img.shields.io/badge/LVGL-7.11-orange)](https://docs.lvgl.io/7.11/)
<div id="top" align="center">

This project was created by Ahmad Agbaria, Lareine Atallah, and Thomas Hashem at Technion - Israel Institute of
Technology, with guidance from [Interdisciplinary Center for Smart Technologies](https://icst.cs.technion.ac.il/).

</div>

## Getting Started

1. Setup working environment by following the steps
   in [Installation Instructions](https://docs.google.com/document/d/1nUOnHGdZ3OWzpR0EWO7GWwUKkHQWSkAC/).
2. Generate [SendGrid](https://docs.sendgrid.com/for-developers/sending-email/api-getting-started)
   and [Twilio](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account) API keys and
   update [Secrets.json](Secrets.json) accordingly.
3. Build Your first project by
   reading [Starter Tutorials](https://docs.google.com/document/d/1rzM6ghP-TxwVlcws6WDDN8_cuASt5gPu/).

## Project Structure

- [Assets](Assets) - Assets that were used in this project
    - [Audio](Assets%2FAudio) - Audio files
    - [Icons](Assets%2FIcons) - Icons
- [Examples](Examples) - Demo for multiple weather stations connected to the cloud
    - [Dashboard.py](Examples%2FDashboard.py) - Station for displaying data
    - [Publisher.py](Examples%2FPublisher.py) - Station for data-gathering
- [Tutorials](Tutorials) - Multiple Tutorials to get You started
    - [Tutorial_0.py](Tutorials%2FTutorial_0.py)
- [Unit Tests](Unit%20Tests) - Tests for validating prober functionality / merging new features
    - [Sensors.py](Unit%20Tests%2FSensors.py) - Reading data from external BPS sensor
    - [SMS.py](Unit%20Tests%2FSMS.py) - Sending SMS
- [ALTconnection.py](ALTconnection.py) - Interface for connecting to Wi-Fi network
- [ALTelements.py](ALTelements.py) - Interface for creating elements to be displayed on the screen
- [ALTnotifications.py](ALTnotifications.py) - Interface to create a notification center to the user
- [ALTutils.py](ALTutils.py) - Interface which provides some helpful utils
- [ALTweather.py](ALTweather.py) - Interface that fetches weather and time information from the internet
- [ALTwidgets.py](ALTwidgets.py) - Interface for creating complex widgets to be displayed on the screen; each widget can
  combine multiple elements from different interfaces
- [Secrets.json](Secrets.json) - JSON file to contain API keys and secret data

<p align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Micropython-logo.svg" alt="MicroPython" width=400/>

</p>
