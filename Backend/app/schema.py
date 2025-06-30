import strawberry
from typing import Optional
from strawberry.file_uploads import Upload  # Use Strawberry's Upload type
# from fastapi import UploadFile
from model_utils import image_to_svg
import asyncio

latest_svg: Optional[str] = None

@strawberry.type
class ConvertImagePayload:
    svg: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def convert_image_to_svg(self, file: Upload) -> ConvertImagePayload:
        global latest_svg
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise ValueError("Only JPEG and PNG are supported.")

        try:
            content = await file.read()
            svg = image_to_svg(content)
            # svg = await asyncio.to_thread(image_to_svg, content)
        except Exception as e:
            raise ValueError(f"Image conversion failed: {str(e)}")

        latest_svg = svg
        return ConvertImagePayload(svg=svg)

@strawberry.type
class Query:
    @strawberry.field
    def latest_svg(self) -> Optional[str]:
        return latest_svg

schema = strawberry.Schema(query=Query, mutation=Mutation)