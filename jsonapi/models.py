import peewee
from playhouse.shortcuts import model_to_dict

#database = peewee.MySQLDatabase(
#    "jsonapi", user="root", password="", host="127.0.0.1", port=3306
#)

database = peewee.SqliteDatabase("db.sqlite3")


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Product(BaseModel):
    id = peewee.AutoField()

    nome = peewee.TextField()
    marca = peewee.TextField()
    prezzo = peewee.IntegerField()

    def to_jsonapi(self, extra=True):
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "attributes": dict(
                filter(lambda x: x[0] != "id", model_to_dict(self).items())
            ),
        } | ({"relationships": {}, "links": {}} if extra else {})


database.create_tables(
    [
        Product,
    ]
)
