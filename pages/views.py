# pages/views.py
from requests import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import gspread
import pandas as pd
import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from oauth2client.service_account import ServiceAccountCredentials


class indexView(LoginRequiredMixin, TemplateView):
    # template_name="index.html"

    # def get_queryset(self, *args, **kwargs):
    # super(indexView, self).__inti__(*args, **kwargs)

    def get(self, request):
        # print (self.request)  # Works!
        # return super(indexView, self).dispatch(request, *args, **kwargs)  # Don't forget this
        print(self.request.user)
        user = self.request.user
        if user.coach == True:
            template_name = "dash_test.html"
        else:
            template_name = "home.html"
        # return HttpResponse(template_name)
        return render(self.request, template_name)

    # user =  self.user

    # user = get_queryset()


class DashboardView(TemplateView):
    template_name = "dash_test.html"


class coachView(TemplateView):
    template_name = ""


class HomePageView(TemplateView):

    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):

        # # defining the scope of the application
        # scope = [
        #     "https://spreadsheets.google.com/feeds",
        #     "https://www.googleapis.com/auth/drive",
        # ]

        # # credentials to the account
        # cred = ServiceAccountCredentials.from_json_keyfile_name("auth.json", scope)

        # # authorize the clientsheet
        # client = gspread.authorize(cred)

        # # open spreadsheet and specific sheet
        # wks = client.open("Test Data umSoccer Test").sheet1

        # # wks.update('A1', "test_ian_fin")
        # df = pd.DataFrame(wks.get_all_records())
        # df.head()

        # Call the base implementation first to get a context

        ctx = super().get_context_data(**kwargs)

        # Add your own entry

        ctx["trish"] = "Hello"
        ctx["ian"] = "Lets go!"

        return ctx
