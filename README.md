# mf-ecasino-concept

## Requirements

Python 3.6.4

## Building static assets (`semantic`)

1. Go to ecasino directory (`cd ecasino`)
2. Run `npm i`, use default semantic settings
3. Go to `semantic` directory (`cd semantic`)
4. Build assets:
    - if you have globally installed gulp: `gulp build`
    - else run `../node_modules/gulp/bin/gulp.js build`

## Manual setup

1. Create virtualenv (`virutalenv venv` / `python -m virutalenv venv`)
2. Activate it (`source venv/bin/activate`)
3. Install requirements (`pip install -r requirements.txt`)
4. Create and configure role / db in postgres (db:`ecasino`, `ecasino:ecasino`)
5. Go to app directory (`cd ecasino`)
6. Run migrations (`python manage.py migrate`)
7. Load default bonuses: `python manage.py loaddata initial-bonus.json`
8. Create superuser account to access `/admin` interface: `python manage.py createsuperuser`
9. Run server (`python manage.py runserver`)
10. Access server on `http://localhost:8000` and admin on 'http://localhost:8000/admin'

## Container setup

1. Build app container: `docker-compose build`
2. Run containers: `docker-compose up`
3. If required, in separate terminal:
    - load fixtures: `docker exec -it mfecasinoconcept_web_1 python manage.py loaddata initial-bonus.json`
    - create superuser: `docker exec -it mfecasinoconcept_web_1 python manage.py createsuperuser`
4. Access server on `http://localhost:8000` and admin on 'http://localhost:8000/admin'

## Additional design assumptions

- Every bonus may have different wagering amount.
- Money spent on playing is accumulated, and may be then used toward cashing-in
  the awarded bonus money to real-money wallet.
- Awarded bonuses work as bonus money wallets that disappear once the bonus is
  cashed-in.
