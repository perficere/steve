from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED

from core.permissions import InternalCommunication

from . import engine


@api_view(["POST"])
@permission_classes([InternalCommunication])
def trigger(request):
    engine.execute(async_=True)
    return Response(status=HTTP_202_ACCEPTED)
