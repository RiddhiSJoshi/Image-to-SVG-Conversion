# schema.py

import graphene
from graphene_file_upload.scalars import Upload
from model_utils import image_to_svg

# Memory-based SVG storage (for example only)
latest_svg_result = None

class UploadImage(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    ok = graphene.Boolean()
    svg = graphene.String()

    def mutate(self, info, file):
        global latest_svg_result

        if file.content_type not in ["image/jpeg", "image/png"]:
            raise Exception("Only JPEG and PNG files are supported.")

        try:
            svg = image_to_svg(file.read())
            latest_svg_result = svg
            return UploadImage(ok=True, svg=svg)
        except Exception as e:
            raise Exception(f"Image processing failed: {e}")

class Query(graphene.ObjectType):
    latest_svg = graphene.String(description="Get the latest converted SVG")

    def resolve_latest_svg(self, info):
        return latest_svg_result or ""

class Mutation(graphene.ObjectType):
    upload_image = UploadImage.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
