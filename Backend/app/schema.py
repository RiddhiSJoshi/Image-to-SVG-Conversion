# schema.py
import strawberry
from typing import Optional
from fastapi import UploadFile
from model_utils import image_to_svg

latest_svg: Optional[str] = None

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_image(self, file: UploadFile) -> str:
        global latest_svg
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise ValueError("Only JPEG and PNG are supported.")

        svg = image_to_svg(await file.read())
        latest_svg = svg
        return svg

@strawberry.type
class Query:
    @strawberry.field
    def latest_svg(self) -> Optional[str]:
        return latest_svg

schema = strawberry.Schema(query=Query, mutation=Mutation)
