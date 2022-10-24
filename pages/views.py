# pages/views.py
from requests import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import gspread
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials


class indexView(TemplateView):
    template_name = "index.html"
    print(dataHelp())


class DashboardView(TemplateView):
    template_name = "dash_test.html"

class coachView(TemplateView):
    template_name = ""
    


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):

        # defining the scope of the application
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        # credentials to the account
        cred = ServiceAccountCredentials.from_json_keyfile_name("auth.json", scope)

        # authorize the clientsheet
        client = gspread.authorize(cred)

        # open spreadsheet and specific sheet
        wks = client.open("Test Data umSoccer Test").sheet1

        # wks.update('A1', "test_ian_fin")
        df = pd.DataFrame(wks.get_all_records())
        df.head()

        # Call the base implementation first to get a context

        ctx = super().get_context_data(**kwargs)

        # Add your own entry

        ctx["trish"] = "Hello"
        ctx["ian"] = "Lets go!"
        ctx["data"] = df["Event Date"][0]

        return ctx
