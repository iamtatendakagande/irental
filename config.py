import os
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://tkagande:@127.0.0.1/irental'
)
