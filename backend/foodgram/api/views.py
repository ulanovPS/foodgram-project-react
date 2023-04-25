from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from grocery_assistant.models import Unit_of_measure

from .serializers import Unit_of_measure_Serializer


@api_view(['GET', 'POST', 'DELETE'])
def unit_of_measure_list(request):
    if request.method == 'POST':
        serializer = Unit_of_measure_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    units = Unit_of_measure.objects.all()
    serializer = Unit_of_measure_Serializer(units, many=True)
    return Response(serializer.data)
