from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from http import HTTPStatus
import requests
import time

# Create your views here.


class GetCoordinates(View):
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
        param_dict = request.GET
        fuel_type = param_dict.get("fuel_type")
        latitude = param_dict.get("latitude")
        longitude = param_dict.get("longitude")
        radius = param_dict.get("radius")
        api_key = "FinfYVhfNcMPWyZPOS2BRycSuwFDCXfx8J4lbmni"
        station_loc_response = requests.get(
            f"https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?"
            + f"api_key={api_key}&fuel_type={fuel_type}&latitude={latitude}&longitude={longitude}&radius={radius}&limit=1"
        )
        # print(station_loc_response.json()["fuel_stations"])
        station_coords = (
            station_loc_response.json()["fuel_stations"][0]["longitude"],
            station_loc_response.json()["fuel_stations"][0]["latitude"],
        )

        return JsonResponse({"station_coords": station_coords}, status=HTTPStatus.OK)
