from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
# from hos.logic import plan_trip_with_hos
import hos.logic as hos_logic

from .image import render_log
import io

@api_view(["GET"])
def ping(_request):
    return Response({"logs": "ok"})

def log_sheet(request, day=0):
    if hos_logic.LAST_PLAN is None:
        return HttpResponse("No trip plan found. Run /api/routing/plan first.", status=400)

    if day >= len(hos_logic.LAST_PLAN):
        return HttpResponse("Day not found", status=404)

    segments = hos_logic.LAST_PLAN[day]["segments"]
    date_label = hos_logic.LAST_PLAN[day]["date"]

    im = render_log(segments, date_label=date_label)
    out = io.BytesIO()
    im.save(out, format="PNG")
    out.seek(0)
    return HttpResponse(out.getvalue(), content_type="image/png")

# def log_sheet(request, day=0):
#     """
#     Render the daily log sheet PNG.
#     For now: uses dummy segments. Later: plug in real HOS planner output.
#     """
#     segments = [
#         {"status": "on_duty", "start": "08:00", "end": "09:00", "note": "Pickup"},
#         {"status": "driving", "start": "09:00", "end": "13:00", "note": "Leg 1"},
#         {"status": "off_duty", "start": "13:00", "end": "13:30", "note": "Break"},
#         {"status": "driving", "start": "13:30", "end": "18:00", "note": "Leg 2"},
#         {"status": "off_duty", "start": "18:00", "end": "04:00", "note": "Sleeper"},
#     ]

#     im = render_log(segments, date_label="2025-09-16")
#     out = io.BytesIO()
#     im.save(out, format="PNG")
#     out.seek(0)
#     return HttpResponse(out.getvalue(), content_type="image/png")