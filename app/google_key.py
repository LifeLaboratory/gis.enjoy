__author__ = 'RaldenProg'
import requests as req
import json
def KEY():
       key = ["AIzaSyCq1eN3OLTe0RWDxrnkcdovunYVhrMmH68",
              "AIzaSyAAeR-hL5mevOnoqs-F_9V3R-TMjI7-DB0",
              "AIzaSyBFUm8_SPBeZjxD6gPnZHEWp6wOROPXPaw",
              "AIzaSyBL3U4P7UNzLH3UJgtJ3pVWPQC4tTNd66g",
              "AIzaSyCq1eN3OLTe0RWDxrnkcdovunYVhrMmH68",
              "AIzaSyCoL4nAJQr9-MXvRgRVW-FPjgBJBdAi6Wk",
              "AIzaSyANPHRugehEQeHEqNZfsP2sdI8MYlHx8PE",
              "AIzaSyDLX4jT_FG3OR21ayCpBH2DE9eY2egbtiI"
              ]
       s = req.Session()
       for k in key:
              url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101,-73.89188969999998&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key={}".format(k)

              answer = s.get(url)
              answer = json.loads(answer.text)
              if answer["status"] == "OK":
                     return k
       return "key not found"
