import io
import re

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse, Response
from dependencies import auth
from routers.export.pdf_generator.export_script import generate_pdf

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/export_pdf", responses={200: {"content": {"application/pdf": {}}}}, response_class=Response,
            summary="Export PDF", include_in_schema=False)
@router.get("/export_pdf/", responses={200: {"content": {"application/pdf": {}}}}, response_class=Response,
            summary="Export PDF")
def export_pdf(authentication=Depends(auth.authenticate)):
    user, db = authentication
    name = user.get_fullname().lower().strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_-]+', '-', name)
    name = re.sub(r'^-+|-+$', '', name)

    output_stream = io.BytesIO()
    generate_pdf(user).write(output_stream)
    pdf_bytes = output_stream.getvalue()
    output_stream.close()
    headers = {'Content-Disposition': f'attachment; filename="Meddly-{name}.pdf"'}
    return Response(pdf_bytes, headers=headers, media_type='application/pdf')
