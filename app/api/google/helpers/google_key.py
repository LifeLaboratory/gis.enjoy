import requests as req
from api.helpers.json import converter

__author__ = 'RaldenProg'


def set_google_key():
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101," \
              "-73.89188969999998&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C" \
              "-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C" \
              "-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C" \
              "-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C" \
              "-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key={}"
    key = ["AIzaSyBWO3Uw0kUvZjecHbgoXjV42ihgdWkahFg",
           "AIzaSyBx1nKFzNuXY6yeYF4zHS9zf7GrrfrYY2s",
           "AIzaSyCsJ9risL0M1losrNXdgRM0f9SIBhoz240",
           "AIzaSyB7wiKdhshjLFf8MJnt2v3tqI1-CPiDMoA",
           "AIzaSyAenHjhZDmeIjnzftM8hE2XfSYgMGL7uuQ",
           "AIzaSyCTVbmRU-8V3ya63Uce-gYTVaFugzkp794",
           "AIzaSyCX2NrmL4FvRMguC7Fw_9VTneJxGKzzzuM",
           "AIzaSyCq1eN3OLTe0RWDxrnkcdovunYVhrMmH68",
           "AIzaSyAAeR-hL5mevOnoqs-F_9V3R-TMjI7-DB0",
           "AIzaSyBFUm8_SPBeZjxD6gPnZHEWp6wOROPXPaw",
           "AIzaSyBL3U4P7UNzLH3UJgtJ3pVWPQC4tTNd66g",
           "AIzaSyCq1eN3OLTe0RWDxrnkcdovunYVhrMmH68",
           "AIzaSyCoL4nAJQr9-MXvRgRVW-FPjgBJBdAi6Wk",
           "AIzaSyANPHRugehEQeHEqNZfsP2sdI8MYlHx8PE",
           "AIzaSyDLX4jT_FG3OR21ayCpBH2DE9eY2egbtiI",
           "AIzaSyD39PkKI4O5VhNQCK75htcCrh0ZtC5yj7o",
           "AIzaSyDCDlgJOT_YqxINbki_5LBJH844AlXalBs",
           "AIzaSyB5zwH6ZjRrl45J322WnGgtH6CgHS8tRYg",
           "AIzaSyCchAfgzg5toHqppqqC5SpNWymInz3mVqU",
           "AIzaSyDi_Smd05scAeA5pJhd1viS2EJXCQow2bI",
           "AIzaSyBWPjjxyfCQVc6E2fSr_f1BiEdkxucMDms",
           "AIzaSyAXOPOqSM0mUSiBG5_jAJGiR-brlViUjZE",
           "AIzaSyBbuyWEFd-whw11GMqcZiiOIxQTIXGUpy8",
           "AIzaSyBKvTtpBfFvWpBWgUOy_Cdu0OgidzKpxms",
           "AIzaSyDJBtcPKCV1-QjhMA5roZqtryAscjgj7X4",
           "AIzaSyBkmfUmisrjEJ_FnCELQFLZ9SUdMgrPTB0",
           "AIzaSyCOxYCba7J0-5-vlwQw4iy5VgVe_r_6VKc",
           "AIzaSyB0Eqh4vo3ylR_4h_pCeOHjRRjCwprwK4s",
           "AIzaSyDZOwzvxMlPHpUtsHMb_WpotTBv46lnOWc",
           "AIzaSyCj46NqzaZ0G0npT_6tTarewAYPgUZ3V3M",
           "AIzaSyAjTR3-ERFPdXtJxCSpfrEkQ6kE4S5mE5s"
        ]
    s = req.Session()
    for k in key:
        answer = s.get(url.format(k))
        answer = converter(answer.text)
        if answer["status"] == "OK":
            return k
    return "key not found"