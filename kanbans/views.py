from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from teams.models import Team
from auths.models import User
from kanbans.models import Column, Ticket
from kanbans.serializers import ColumnSerializer, TicketSerializer

# TODO: 권한설정 커스텀하기(팀원, 팀장, 일반유저)

class ColumnsView(APIView):
    '''
    URL: /kanbans/columns
    '''
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        '''
        Column 전체 조회 API
        TODO: ticket 목록도 함께 조회: `column` 내부에는 속한 `ticket` 목록을 같이 반환합니다.
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


class ColumnDetailsView(APIView):
    '''
    URL: /kanbans/columns/<int:col_id>
    '''
    permission_classes = [IsAuthenticated]

    def put(self, request, col_id):
        '''
        Column 수정 API
        '''
        user = request.user
        team = Team.objects.get(members=user)
        column = Column.objects.get(id=col_id)

        if column.team != team:
            return Response(
                {"detail": "You do not have permission to update this column."}, 
                status=status.HTTP_403_FORBIDDEN
            )

    def delete(self, request, col_id):
        '''
        Column 삭제 API
        '''
        user = request.user
        team = Team.objects.get(members=user)
        column = Column.objects.get(id=col_id)

        if column.team != team:
            return Response(
                {"detail": "You do not have permission to delete this column."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        ticket_count = column.ticket_set.count()  # 역참조 이용
        if ticket_count > 0:
            tickets = column.ticket_set.all()
            ticket_data = [{"id": ticket.id, "title": ticket.title} for ticket in tickets]

            return Response(
                {
                    "detail": "Column cannot be deleted as it contains tickets.",
                    "ticket_count": ticket_count,
                    "tickets": ticket_data,
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        column.delete()
        return Response(
            {"detail": "Column deleted successfully."}, 
            status=status.HTTP_200_OK
        )


class ReorderColumnsView(APIView):
    '''
    URL: /kanbans/columns/orders
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        '''
        Column 순서 변경 API
        '''
        user = request.user
        team = Team.objects.get(members=user)
        order = request.data.get('order')

        if not order:
            return Response(
                {"detail": "Order parameter is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        columns = Column.objects.filter(team=team).order_by('order')
        if len(order) != columns.count():
            return Response(
                {"detail": "Invalid order parameter."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        for col_id, new_order in zip([col.id for col in columns], order):
            column = Column.objects.get(id=col_id)
            column.order = new_order
            column.save()

        return Response(
            {"detail": "Columns reordered successfully."}, 
            status=status.HTTP_200_OK
        )


class TicketsView(APIView):
    '''
    URL: /kanbans/columns/<int:col_id>/tickets
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, column_id):
        '''
        Ticket 생성 API
        '''
        column = Column.objects.get(id=column_id)

        if request.user not in column.team.members.all():
            return Response(
                {"detail": "You do not have permission to create a ticket in this column."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(column=column)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
