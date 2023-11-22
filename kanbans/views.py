from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from teams.models import Team
from auths.models import User
from kanbans.models import Column
from kanbans.serializers import ColumnSerializer


class ColumnView(APIView):
    '''
    URL: /kanbans/columns
    '''
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        '''
        Column 전체 조회 API
        '''
        user = request.user
        team = Team.objects.get(members=user)

        columns = Column.objects.filter(team=team).order_by('order')
        serializer = ColumnSerializer(columns, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
        Column 추가 API
        '''
        user = request.user
        team = Team.objects.get(members=user)
        if not team.owner.filter(id=user.id).exists():
            return Response({"detail": "Only team owner can add columns."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['team'] = team.pk
        data['order'] = Column.objects.filter(team=team).count() + 1

        column_serializer = ColumnSerializer(data=data)
        if column_serializer.is_valid():
            column_serializer.save()
            return Response(
                column_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            column_serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

