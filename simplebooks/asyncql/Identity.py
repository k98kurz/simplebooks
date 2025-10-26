from __future__ import annotations
from sqloquent.asyncql import AsyncSqlModel, AsyncRelatedCollection
import packify


_empty_dict = packify.pack({})


class Identity(AsyncSqlModel):
    connection_info: str = ''
    table: str = 'identities'
    id_column: str = 'id'
    columns: tuple[str] = (
        'id', 'name', 'details', 'pubkey', 'seed', 'secret_details', 'description',
    )
    id: str
    name: str
    details: bytes
    pubkey: bytes|None
    seed: bytes|None
    secret_details: bytes|None
    description: str|None
    ledgers: AsyncRelatedCollection

    # override automatic property
    @property
    def details(self) -> packify.SerializableType:
        """A packify.SerializableType stored in the database as a blob."""
        return packify.unpack(self.data.get('details', _empty_dict))
    @details.setter
    def details(self, val: packify.SerializableType):
        self.data['details'] = packify.pack(val)

    def public(self) -> dict:
        """Return the public data for cloning the Identity."""
        return {
            k:v for k,v in self.data.items()
            if k not in self.columns_excluded_from_hash
        }
