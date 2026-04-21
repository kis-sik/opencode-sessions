# Публикация ocs на PyPI

## Подготовка

### 1. Зарегистрироваться на PyPI
- Перейти на https://pypi.org
- Создать аккаунт (если нет)
- Подтвердить email

### 2. Создать API токен
- Войти в аккаунт PyPI
- Перейти в Account Settings → API tokens
- Создать новый токен с scope:
  - `Entire account` (для первого пакета)
  - Или `opencode-sessions` (ограниченный доступ)
- Скопировать токен: `pypi-...`

### 3. Настроить аутентификацию

#### Вариант A: Файл `.pypirc`
```bash
# Создать файл ~/.pypirc
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-ваш_токен_здесь
EOF

# Установить правильные права
chmod 600 ~/.pypirc
```

#### Вариант B: Переменные окружения
```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-ваш_токен_здесь"
```

#### Вариант C: Конфигурация uv
```bash
# Создать файл ~/.config/uv/auth.json
mkdir -p ~/.config/uv
cat > ~/.config/uv/auth.json << 'EOF'
{
  "https://upload.pypi.org/legacy/": {
    "username": "__token__",
    "password": "pypi-ваш_токен_здесь"
  }
}
EOF
```

## Публикация

### 1. Собрать дистрибутивы
```bash
cd ~/tech/ocs
uv build
```

### 2. Проверить дистрибутивы
```bash
# Проверить wheel
uvx twine check dist/*

# Проверить метаданные
python3 -m twine check dist/*
```

### 3. Опубликовать
```bash
# Используя uv
uv publish

# Или используя twine
uvx twine upload dist/*
```

### 4. Проверить публикацию
```bash
# Через несколько минут
pip install opencode-sessions
# или
uv add opencode-sessions
```

## Важные моменты

### Имя пакета
- На PyPI: `opencode-sessions` (доступно)
- Импорт: `import ocs`
- CLI команда: `ocs`

### Версионирование
- Текущая версия: 1.3.0
- Следуем SemVer: MAJOR.MINOR.PATCH
- Теги на GitHub: v1.0.0, v1.1.0, v1.2.0, v1.3.0

### Метаданные
- `pyproject.toml` содержит все необходимые метаданные
- README.md используется как long_description
- MIT лицензия
- Python >=3.7

## После публикации

### 1. Обновить документацию
```bash
# Обновить README с PyPI бейджами
echo "[![PyPI version](https://badge.fury.io/py/opencode-sessions.svg)](https://pypi.org/project/opencode-sessions/)" >> README.md
```

### 2. Создать релиз на GitHub
```bash
# Создать релиз v1.3.0 с дистрибутивами
gh release create v1.3.0 \
  --title "ocs v1.3.0" \
  --notes "Interactive rename with fzf" \
  dist/ocs-1.3.0-py3-none-any.whl \
  dist/ocs-1.3.0.tar.gz
```

### 3. Протестировать установку
```bash
# Чистая установка
pip uninstall -y opencode-sessions
pip install opencode-sessions
ocs --help
```

## Устранение проблем

### Ошибка: "Package already exists"
- Имя `ocs` уже занято (версия 0.12.0)
- Используем `opencode-sessions`
- Обновить `pyproject.toml` если нужно

### Ошибка: "Missing credentials"
- Проверить `.pypirc` или переменные окружения
- Убедиться что токен правильный
- Попробовать `uv publish --token pypi-...`

### Ошибка: "Invalid version"
- Проверить формат версии в `pyproject.toml`
- Должно быть: `1.3.0` (не `v1.3.0`)

## Ссылки
- PyPI: https://pypi.org/project/opencode-sessions/
- GitHub: https://github.com/kis-sik/opencode-sessions
- Документация: README.md