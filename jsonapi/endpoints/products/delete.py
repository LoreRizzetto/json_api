import http.server
import json
import re

from ...models import Product
from ... import models
import peewee
from ...request_router import RequestRouter


@RequestRouter.register_handler("DELETE", "/products/([0-9]+)")
def _(handler: RequestRouter, match: re.Match):
    try:
        product = Product.select().where(Product.id == int(match.group(1))).get()
        product.delete_instance()
        handler.send_body("", 204)
    except Product.DoesNotExist:
        handler.send_body("", 404)
