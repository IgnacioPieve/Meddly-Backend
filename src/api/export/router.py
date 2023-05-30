import io
import re

from fastapi import APIRouter, Depends
from starlette.responses import Response

from api.auth.dependencies import authenticate
from api.export.service import UserDataPDFGenerator
from api.user.models import User

router = APIRouter(prefix="/export", tags=["Export"])


@router.get(
    "/export_pdf",
    responses={200: {"content": {"application/pdf": {}}}},
    response_class=Response,
    summary="Export PDF",
)
async def export_pdf(user: User = Depends(authenticate)):
    """
    Export user data as PDF

    This endpoint allows the authenticated user to export their data as a PDF file.

    Args:
    - user (User): Authentication dependency. This parameter is automatically obtained from the request.
    """
    user = User(**user)
    name = user.get_fullname().lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_-]+", "-", name)
    name = re.sub(r"^-+|-+$", "", name)

    output_stream = io.BytesIO()
    pdf = await UserDataPDFGenerator.generate_pdf(user)
    pdf.write(output_stream)
    pdf_bytes = output_stream.getvalue()
    output_stream.close()
    headers = {"Content-Disposition": f'attachment; filename="Meddly-{name}.pdf"'}
    return Response(pdf_bytes, headers=headers, media_type="application/pdf")
