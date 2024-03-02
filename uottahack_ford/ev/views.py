from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from http import HTTPStatus
import requests
import time

# Create your views here.


class EVTracker(View):
    def get(self, request):
        param_dict = request.GET
        start_address = param_dict.get("start_address")
        start_address = "+".join(start_address.split())
        end_address = param_dict.get("end_address")
        end_address = "+".join(end_address.split())
        api_key = "65e372703f207320149400yiu8b77f2"
        start_osm_response = requests.get(
            "https://geocode.maps.co/search?q={}&api_key={}".format(
                start_address, api_key
            )
        )
        time.sleep(1)
        end_osm_response = requests.get(
            "https://geocode.maps.co/search?q={}&api_key={}".format(
                end_address, api_key
            )
        )
        print(end_osm_response.json())
        start_coords = (
            start_osm_response.json()[0]["lat"],
            start_osm_response.json()[0]["lon"],
        )
        end_coords = (
            end_osm_response.json()[0]["lat"],
            end_osm_response.json()[0]["lon"],
        )
        return JsonResponse(
            {"start": start_coords, "end": end_coords}, status=HTTPStatus.OK
        )
