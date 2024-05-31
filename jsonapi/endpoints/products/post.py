import http.server
import json
import re

from ...models import Product
from ...request_router import RequestRouter


@RequestRouter.register_handler("POST", "/products")
def _(handler: RequestRouter, match: re.Match):
    data = json.loads(handler.get_body())

    product = Product.create(**data["data"]["attributes"])

    handler.send_body(
        json.dumps(
            {
                "data": product.to_jsonapi(extra=False),
            }
        ),
        201,
        {"Location": f"/products/{product.id}"},
    )
