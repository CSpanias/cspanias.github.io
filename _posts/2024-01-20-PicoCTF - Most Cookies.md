---
title: PicoCTF - Most Cookies
date: 2024-01-20
categories: [CTF, Web]
tags: [picoctf, web, web-exploitation, most-cookies, cookies]
img_path: /assets/picoctf/web_exploitation/most_cookies
published: true
image:
    path: ../../picoctf_logo.png
---

![](room_banner.png){: width="70%"}

> **Description**: Alright, enough of using my own encryption. Flask session cookies should be plenty secure! `server.py http://mercury.picoctf.net:53700/`.

1. This challenge is a continuation of [Cookies](https://cspanias.github.io/posts/PicoCTF-Cookies/) and [More Cookies](https://cspanias.github.io/posts/PicoCTF-More-Cookies/). The difference is that it includes both a link and a Python script called `server.py`: 

    ![](home.png){: .normal width="60%"}

    ```python
    from flask import Flask, render_template, request, url_for, redirect, make_response, flash, session
    import random
    app = Flask(__name__)
    flag_value = open("./flag").read().rstrip()
    title = "Most Cookies"
    cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
    app.secret_key = random.choice(cookie_names)

    @app.route("/")
    def main():
        if session.get("very_auth"):
            check = session["very_auth"]
            if check == "blank":
                return render_template("index.html", title=title)
            else:
                return make_response(redirect("/display"))
        else:
            resp = make_response(redirect("/"))
            session["very_auth"] = "blank"
            return resp

    @app.route("/search", methods=["GET", "POST"])
    def search():
        if "name" in request.form and request.form["name"] in cookie_names:
            resp = make_response(redirect("/display"))
            session["very_auth"] = request.form["name"]
            return resp
        else:
            message = "That doesn't appear to be a valid cookie."
            category = "danger"
            flash(message, category)
            resp = make_response(redirect("/"))
            session["very_auth"] = "blank"
            return resp

    @app.route("/reset")
    def reset():
        resp = make_response(redirect("/"))
        session.pop("very_auth", None)
        return resp

    @app.route("/display", methods=["GET"])
    def flag():
        if session.get("very_auth"):
            check = session["very_auth"]
            if check == "admin":
                resp = make_response(render_template("flag.html", value=flag_value, title=title))
                return resp
            flash("That is a cookie! Not very special though...", "success")
            return render_template("not-flag.html", title=title, cookie_name=session["very_auth"])
        else:
            resp = make_response(redirect("/"))
            session["very_auth"] = "blank"
            return resp

    if __name__ == "__main__":
        app.run()
    ```

eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.ZawTtg.9oqnwbmC-fHJr0Qho7dEWar9s2c
eyJ2ZXJ5X2F1dGgiOiJzbmlja2VyZG9vZGxlIn0.ZawUxg.SXd-NQ3AjxwvwA-yqAuwDfpB6BE