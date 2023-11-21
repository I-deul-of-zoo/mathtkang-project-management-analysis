from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from teams.models import Team
from auths.models import User
from teams.serializers import TeamSerializer


class TeamCreation(APIView):
    '''
    팀 생성 API
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['board_name'] = f"{data['name']} Board"  # 보드 이름 자동 생성

        team_serializer = TeamSerializer(data=data)
        if team_serializer.is_valid():
            team = team_serializer.save()
            # 팀장으로 설정
            team.owner.add(request.user)

            return Response(
                team_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            team_serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

