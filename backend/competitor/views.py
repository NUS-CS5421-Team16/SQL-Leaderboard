from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from competitor.models import Competitor
from competitor.serializer import CompetitorSerializer


@api_view(['POST'])
def register(request):
    # change email and password
    print('register')
    return Response(status=status.HTTP_200_OK, data={})


@api_view(['POST'])
def login(request):
    # authenticate
    print('login')
    return Response(status=status.HTTP_200_OK, data={})


class CompetitorViewset(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return super(CompetitorViewset, self).retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['PUT'])
    def team(self, request, *args, **kwargs):
        # change team detail

        return Response(status=status.HTTP_200_OK, data={})

    @action(detail=True, methods=['POST', 'GET'])
    def task(self, request, *args, **kwargs):
        # create task
        if request.method == 'POST':

            return Response(status=status.HTTP_200_OK, data={})
        # retrieve latest task of the team
        elif request.method == 'GET':

            return Response(status=status.HTTP_200_OK, data={})
