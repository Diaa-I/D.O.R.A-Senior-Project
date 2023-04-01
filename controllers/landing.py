from flask import Flask, flash, render_template, redirect, request, url_for

class landingController:


    def rendering():
        return render_template("/views/landing.html")