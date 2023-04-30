from flask import Flask, flash, render_template, redirect, request, url_for

class landingController:

    def a():
        return render_template("/views/index.html")

    def rendering():
        return render_template("/views/landing.html")