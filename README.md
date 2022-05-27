# Professional Assessment

Thi is a professional assessment for DeviantArt.

### Setup

```bash
$ python3 -m venv ./tmp/venv
$ source ./tmp/venv/bin/activate # fish shell: source ./tmp/venv/bin/activate.fish
$ pip install -r requirements.txt
$ python manage.py makemigrations && python manage.py migrate
```

### Run

```bash
$ python manage.py runserver
```

### Test

```bash
$ python manage.py test
```

### Cleanup

```bash
$ deactivate
$ rm -rf ./tmp
```

### Author

Author: [@mkhizeryounas](https://github.com/mkhizeryounas)
