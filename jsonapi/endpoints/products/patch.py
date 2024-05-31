import http.server
import json
import re

from ...models import Product
from ...request_router import RequestRouter


@RequestRouter.register_handler("PATCH", "/products/([0-9]+)")
def _(handler: RequestRouter, match: re.Match):
    data = json.loads(handler.get_body())

    product = Product.select().where(Product.id == int(match.group(1))).get()

    for n, k in data["data"]["attributes"].items():
        setattr(product, n, k)

    product.save()

    handler.send_body(
        json.dumps(
            {
                "data": product.to_jsonapi(extra=False),
            }
        ),
        200
    )
