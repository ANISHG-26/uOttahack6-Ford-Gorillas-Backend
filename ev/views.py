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
        if len(start_osm_response.json()) == 0:
            return JsonResponse(
                {"message": "Start address not found"}, status=HTTPStatus.OK
            )
        if len(end_osm_response.json()) == 0:
            return JsonResponse(
                {"message": "End address not found"}, status=HTTPStatus.OK
            )
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


class StationLocator(View):
    def get(self, request):
        state = "ON"
        country = "CA"
        fuel_type = "ELEC"
        api_key = "FinfYVhfNcMPWyZPOS2BRycSuwFDCXfx8J4lbmni"
        start_osm_response = requests.get(
            f"https://developer.nrel.gov/api/alt-fuel-stations/v1.geojson?"
            + f"api_key={api_key}&fuel_type={fuel_type}&state={state}&country={country}"
        )
        time.sleep(2)
        return JsonResponse(start_osm_response, status=HTTPStatus.OK)
