from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from events.models import Event
from events.serializers import EventSerializer

def evaluate(user, obj, request):
    return user.username == obj.baby.parent.name

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='EventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'events.view_event',
                    'destroy': evaluate,
                    'update': evaluate,
                    'partial_update': 'events.change_event',
                }
            }
        ),
    )


    def perform_create(self, serializer):
        """user = self.request.user
        assign_perm('events.change_event', user, event)
        assign_perm('events.view_event', user, event)
        return Response(serializer.data)"""
        parent_baby=serializer.validated_data["baby"]
        print(parent_baby)
       
        user = self.request.user
        #usuario=user.username
        nombre_user=str(user.username)
        nombre_padre=str(parent_baby)
        print(nombre_user==nombre_padre)
        print(user.username)
        
        if (nombre_user!=nombre_padre):
            print ("Usted no tiene autorizado eso")
        elif(nombre_user==nombre_padre):
            event = serializer.save()
            print ("LLEGO A GUARDARSE")
            assign_perm('events.change_event', user, event)
            assign_perm('events.view_event', user, event)
            return Response(serializer.data)