from django.urls import path
from kanbans import views

app_name = "kanbans"

urlpatterns =[
    path("columns", views.ColumnsView.as_view()),
    path("columns/<int:col_id>/", views.ColumnDetailsView.as_view()),
    path("columns/order", views.ReorderColumnsView.as_view()),
    path("columns/<int:col_id>/tickets/", views.TicketsView.as_view()),
    path("columns/<int:col_id>/tickets/<int:tic_id>/", views.TicketDetailsView.as_view()),
    path("columns/<int:col_id>/tickets/order", views.ReorderTicketsView.as_view()),
]