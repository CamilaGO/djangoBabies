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
        parent_baby=serializer.validated_data["baby"]
        #print(parent_baby)
        user = self.request.user
        #usuario=user.username
        nameUser=str(user.username)
        nameParent=str(parent_baby)
        #print(nameUser==nameParent)
        #print(user.username)
        
        if (nameUser!=nameParent):
            print ("Usted no tiene autorizado eso")
        elif(nameUser==nameParent):
            event = serializer.save()
            print ("Se guardo el evento")
            assign_perm('events.change_event', user, event)
            assign_perm('events.view_event', user, event)
            return Response(serializer.data)
    
