from datetime import datetime, timedelta

ON_DUTY = "on_duty"
OFF_DUTY = "off_duty"
SLEEPER = "sleeper"
DRIVING = "driving"
LAST_PLAN = None 
def plan_trip_with_hos(route_distance_miles, avg_speed=55, cycle_used_hours=0):
    """
    Returns a list of daily logs with duty segments.
    """
    miles_remaining = route_distance_miles
    miles_since_fuel = 0

    days = []
    duty_day = []
    global LAST_PLAN

    current_time = datetime(2025, 9, 16, 8, 0)  # start 8 AM
    driving_in_window = 0
    duty_in_window = 0
    cycle_total = cycle_used_hours

    def push_segment(status, hours, note=""):
        nonlocal current_time, driving_in_window, duty_in_window, cycle_total, duty_day
        start = current_time
        end = current_time + timedelta(hours=hours)
        duty_day.append({
            "status": status,
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M"),
            "note": note
        })
        current_time = end
        if status in [ON_DUTY, DRIVING]:
            duty_in_window += hours
            cycle_total += hours
        if status == DRIVING:
            driving_in_window += hours

    # start day with pickup
    push_segment(ON_DUTY, 1, "Pickup")

    while miles_remaining > 0:
        # enforce 70/8 limit
        if cycle_total >= 70:
            push_segment(OFF_DUTY, 34, "34-hour restart")
            days.append({
                "date": current_time.strftime("%Y-%m-%d"),
                "segments": duty_day
            })
            duty_day = []
            duty_in_window = driving_in_window = 0
            cycle_total = 0
            continue

        # enforce 14-hour duty window
        if duty_in_window >= 14:
            push_segment(OFF_DUTY, 10, "10-hour reset")
            days.append({
                "date": current_time.strftime("%Y-%m-%d"),
                "segments": duty_day
            })
            duty_day = []
            duty_in_window = driving_in_window = 0
            continue

        # enforce 30-min break after 8h driving
        if driving_in_window >= 8:
            push_segment(OFF_DUTY, 0.5, "30-min break")
            driving_in_window = 0
            continue

        # fuel stop check
        if miles_since_fuel >= 1000:
            push_segment(ON_DUTY, 0.5, "Fuel stop")
            miles_since_fuel = 0
            continue

        # max driving time left in this window
        can_drive = min(11 - driving_in_window, 14 - duty_in_window, 70 - cycle_total)
        if can_drive <= 0:
            push_segment(OFF_DUTY, 10, "10-hour reset")
            days.append({
                "date": current_time.strftime("%Y-%m-%d"),
                "segments": duty_day
            })
            duty_day = []
            driving_in_window = duty_in_window = 0
            continue

        # drive next leg
        leg_time = min(miles_remaining / avg_speed, can_drive)
        push_segment(DRIVING, leg_time, "Driving")
        miles_remaining -= leg_time * avg_speed
        miles_since_fuel += leg_time * avg_speed

    # add drop-off 1h
    push_segment(ON_DUTY, 1, "Drop-off")
    # days.append({"date": duty_day[0]["start"], "segments": duty_day})
    days.append({
        "date": current_time.strftime("%Y-%m-%d"),
        "segments": duty_day
    })

    LAST_PLAN = days 
    return days
