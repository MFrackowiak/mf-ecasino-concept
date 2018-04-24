# mf-ecasino-concept

## Requirements

Python 3.6.4

## Manual setup

1. Create virtualenv (`virutalenv venv` / `python -m virutalenv venv`)
2. Activate it (`source venv/bin/activate`)
3. Install requirements (`pip install -r requirements.txt`)
4. Create and configure role / db in postgres (db:`ecasino`, `ecasino:ecasino`)
4. Go to app directory (`cd ecasino`)
5. Run migrations (`python manage.py migrate`)
6. Run server (`python manage.py runserver`)

## Container setup

\#TODO

## Additional design assumptions

- Every bonus may have different wagering amount.
- Money spent on playing is accumulated, and may be then used toward cashing-in
  the awarded bonus money to real-money wallet.
- Awarded bonuses work as bonus money wallets that disappear once the bonus is
  cashed-in.
