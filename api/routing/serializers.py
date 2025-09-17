from rest_framework import serializers

class PlanRequestSerializer(serializers.Serializer):
    current_location = serializers.CharField()
    pickup_location = serializers.CharField()
    dropoff_location = serializers.CharField()
    cycle_used_hours = serializers.IntegerField(min_value=0)
