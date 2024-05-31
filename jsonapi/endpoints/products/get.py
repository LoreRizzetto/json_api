import http.server
import json
import re

from ...models import Product
from ...request_router import RequestRouter


@RequestRouter.register_handler("GET", "/products")
def _(handler: RequestRouter, match: re.Match):
    handler.send_body(
        json.dumps(
            {
                "links": {},
                "data": list(map(lambda x: x.to_jsonapi(), Product.select())),
                "included": [],
            }
        )
    )


@RequestRouter.register_handler("GET", "/products/([0-9]+)")
def _(handler: RequestRouter, match: re.Match):
    product = Product.select().where(Product.id == int(match.group(1))).get()

    handler.send_body(
        json.dumps(
            {
                "data": product.to_jsonapi(extra=False),
            }
        )
    )
