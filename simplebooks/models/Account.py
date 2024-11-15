from __future__ import annotations
from sqloquent import SqlModel, RelatedModel, RelatedCollection
from .AccountType import AccountType
from .Entry import Entry
from .EntryType import EntryType
import packify


class Account(SqlModel):
    connection_info: str = ''
    table: str = 'accounts'
    id_column: str = 'id'
    columns: tuple[str] = (
        'id', 'name', 'type', 'ledger_id', 'parent_id', 'code',
        'category', 'details'
    )
    id: str
    name: str
    type: str
    ledger_id: str
    parent_id: str
    code: str|None
    category: str|None
    details: bytes|None
    ledger: RelatedModel
    parent: RelatedModel
    children: RelatedCollection
    entries: RelatedCollection

    # override automatic property
    @property
    def type(self) -> AccountType:
        """The AccountType of the Account."""
        return AccountType(self.data['type'])
    @type.setter
    def type(self, val: AccountType):
        if type(val) is AccountType:
            self.data['type'] = val.value

    # override automatic property
    @property
    def details(self) -> packify.SerializableType:
        """A packify.SerializableType stored in the database as a blob."""
        return packify.unpack(self.data.get('details', None) or b'n\x00\x00\x00\x00')
    @details.setter
    def details(self, val: packify.SerializableType):
        if isinstance(val, packify.SerializableType):
            self.data['details'] = packify.pack(val)

    @staticmethod
    def _encode(data: dict|None) -> dict|None:
        if type(data) is not dict:
            return data
        if type(data.get('type', None)) is AccountType:
            data['type'] = data['type'].value
        return data

    @classmethod
    def insert(cls, data: dict) -> Account | None:
        """Ensure data is encoded before inserting."""
        result = super().insert(cls._encode(data))
        return result

    def balance(self, include_sub_accounts: bool = True) -> int:
        """Tally all entries for this account. Includes the balances of
            all sub-accounts if include_sub_accounts is True.
        """
        totals = {
            EntryType.CREDIT: 0,
            EntryType.DEBIT: 0,
            'subaccounts': 0,
        }
        for entries in self.entries().query().chunk(500):
            entry: Entry
            for entry in entries:
                totals[entry.type] += entry.amount

        if include_sub_accounts:
            for acct in self.children:
                totals['subaccounts'] += acct.balance(include_sub_accounts=True)

        if self.type in (
            AccountType.ASSET, AccountType.DEBIT_BALANCE,
            AccountType.CONTRA_LIABILITY, AccountType.CONTRA_EQUITY,
        ):
            return totals[EntryType.DEBIT] - totals[EntryType.CREDIT] + totals['subaccounts']

        return totals[EntryType.CREDIT] - totals[EntryType.DEBIT] + totals['subaccounts']
