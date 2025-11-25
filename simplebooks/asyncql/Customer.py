from sqloquent.asyncql import AsyncSqlModel
import packify


_empty_dict = packify.pack({})


class Customer(AsyncSqlModel):
    connection_info: str = ''
    table: str = 'customers'
    id_column: str = 'id'
    columns: tuple[str] = ('id', 'name', 'code', 'details', 'description')
    id: str
    name: str
    code: str|None
    details: bytes|None
    description: str|None

    # override automatic property
    @property
    def details(self) -> packify.SerializableType:
        """A packify.SerializableType stored in the database as a blob."""
        return packify.unpack(self.data.get('details', None) or _empty_dict)
    @details.setter
    def details(self, val: packify.SerializableType):
        self.data['details'] = packify.pack(val)
