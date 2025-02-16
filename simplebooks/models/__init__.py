from .Account import Account
from .AccountCategory import AccountCategory
from .AccountType import AccountType
from .ArchivedEntry import ArchivedEntry
from .ArchivedTransaction import ArchivedTransaction
from .Currency import Currency
from .Customer import Customer
from .Entry import Entry
from .EntryType import EntryType
from .Identity import Identity
from .Ledger import Ledger
from .LedgerType import LedgerType
from .Statement import Statement
from .Transaction import Transaction
from .Vendor import Vendor
from sqloquent import contains, within, has_many, belongs_to


Identity.ledgers = has_many(Identity, Ledger, 'identity_id')
Ledger.owner = belongs_to(Ledger, Identity, 'identity_id')

Ledger.currency = belongs_to(Ledger, Currency, 'currency_id')

Ledger.accounts = has_many(Ledger, Account, 'ledger_id')
Account.ledger = belongs_to(Account, Ledger, 'ledger_id')

Account.children = has_many(Account, Account, 'parent_id')
Account.parent = belongs_to(Account, Account, 'parent_id')

Account.category = belongs_to(Account, AccountCategory, 'category_id')
AccountCategory.accounts = has_many(AccountCategory, Account, 'category_id')

Account.entries = has_many(Account, Entry, 'account_id')
Entry.account = belongs_to(Entry, Account, 'account_id')

Entry.transactions = within(Entry, Transaction, 'entry_ids')
Transaction.entries = contains(Transaction, Entry, 'entry_ids')

Transaction.ledgers = contains(Transaction, Ledger, 'ledger_ids')
Ledger.transactions = within(Ledger, Transaction, 'ledger_ids')

Statement.ledger = belongs_to(Statement, Ledger, 'ledger_id')
Ledger.statements = has_many(Ledger, Statement, 'ledger_id')

Statement.transactions = contains(Statement, Transaction, 'tx_ids')
Transaction.statements = within(Transaction, Statement, 'tx_ids')

Statement.archived_transactions = contains(Statement, ArchivedTransaction, 'tx_ids')
ArchivedTransaction.statements = within(ArchivedTransaction, Statement, 'tx_ids')

ArchivedEntry.transactions = within(ArchivedEntry, ArchivedTransaction, 'entry_ids')
ArchivedTransaction.entries = contains(ArchivedTransaction, ArchivedEntry, 'entry_ids')

ArchivedEntry.account = belongs_to(ArchivedEntry, Account, 'account_id')
Account.archived_entries = has_many(Account, ArchivedEntry, 'account_id')

ArchivedTransaction.ledgers = contains(ArchivedTransaction, Ledger, 'ledger_ids')
Ledger.archived_transactions = within(Ledger, ArchivedTransaction, 'ledger_ids')