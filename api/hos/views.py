from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from hos.logic import plan_trip_with_hos
from routing.serializers import PlanRequestSerializer
from routing.services import geocode, get_route
from rest_framework import status

@api_view(["GET"])
def ping(_request):
    return Response({"hos": "ok"})




@api_view(["POST"])
def plan_trip(request):
    serializer = PlanRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    try:
        cur = geocode(data["current_location"])
        pick = geocode(data["pickup_location"])
        drop = geocode(data["dropoff_location"])

        route = get_route([cur, pick, drop])

        # add pickup 1h
        days = plan_trip_with_hos(
            route_distance_miles=route["distance_miles"],
            avg_speed=55,
            cycle_used_hours=data["cycle_used_hours"]
        )

        response = {
            "route": route,
            "hos_plan": {"days": days}
        }
        return Response(response)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
