from django.shortcuts import render
from .serializers import PlanRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlanRequestSerializer
from .services import geocode, get_route
import hos.logic as hos_logic


@api_view(["GET"])
def ping(_request):
    return Response({"routing": "ok"})

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

        # generate hos_plan and save it globally
        days = hos_logic.plan_trip_with_hos(
            route_distance_miles=route["distance_miles"],
            avg_speed=55,
            cycle_used_hours=data["cycle_used_hours"]
        )

        response = {"route": route, "hos_plan": {"days": days}}
        return Response(response)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)