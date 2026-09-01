from rest_framework import serializers


class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(
        required=True,
        max_length=255,
    )

    finish = serializers.CharField(
        required=True,
        max_length=255,
    )

    def validate(self, attrs):
        start = attrs["start"].strip()
        finish = attrs["finish"].strip()

        if not start:
            raise serializers.ValidationError(
                {"start": "Start location is required."}
            )

        if not finish:
            raise serializers.ValidationError(
                {"finish": "Finish location is required."}
            )

        if start.lower() == finish.lower():
            raise serializers.ValidationError(
                "Start and finish locations must be different."
            )

        attrs["start"] = start
        attrs["finish"] = finish

        return attrs