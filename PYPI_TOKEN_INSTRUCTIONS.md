# Получение токена PyPI для публикации opencode-sessions

## Шаг 1: Регистрация на PyPI

1. Перейдите на https://pypi.org
2. Нажмите "Register" (если нет аккаунта)
3. Заполните форму:
   - Username: (выберите имя)
   - Email: (ваш email)
   - Password: (надёжный пароль)
4. Подтвердите email (письмо придёт на указанный адрес)

## Шаг 2: Создание API токена

1. Войдите в аккаунт PyPI
2. Перейдите в Account Settings → API tokens
3. Нажмите "Add API token"
4. Заполните форму:
   - **Token name**: `opencode-sessions-publish`
   - **Scope**: Выберите "Entire account" (для первого пакета)
     - Или "opencode-sessions" если хотите ограничить доступ
   - **Expires**: Рекомендуется "Never" или длительный срок
5. Нажмите "Create token"
6. **Скопируйте токен** (он покажется только один раз!):
   - Формат: `pypi-...` (длинная строка)

## Шаг 3: Настройка аутентификации

### Вариант A: Файл `.pypirc` (рекомендуется)

```bash
# Создайте файл ~/.pypirc
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-ваш_скопированный_токен_здесь
EOF

# Установите правильные права
chmod 600 ~/.pypirc
```

### Вариант B: Конфигурация uv

```bash
# Создайте директорию если нет
mkdir -p ~/.config/uv

# Создайте файл конфигурации
cat > ~/.config/uv/auth.json << 'EOF'
{
  "https://upload.pypi.org/legacy/": {
    "username": "__token__",
    "password": "pypi-ваш_скопированный_токен_здесь"
  }
}
EOF
```

### Вариант C: Переменные окружения

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-ваш_скопированный_токен_здесь"
```

## Шаг 4: Публикация

```bash
cd ~/tech/ocs

# Проверка (dry-run)
uv publish --dry-run

# Публикация
uv publish
```

## Шаг 5: Проверка публикации

Через несколько минут после публикации:

```bash
# Проверьте на PyPI
curl -s https://pypi.org/pypi/opencode-sessions/json | python3 -c "import sys, json; data=json.load(sys.stdin); print('Version:', data['info']['version'])"

# Установите и проверьте
pip install opencode-sessions
opencode-sessions --help
ocs --help
```

## Устранение проблем

### Ошибка: "Invalid or non-existent authentication information"
- Проверьте что токен скопирован полностью
- Убедитесь что используется `__token__` как username
- Проверьте права файла `.pypirc` (600)

### Ошибка: "Package already exists"
- Имя `opencode-sessions` должно быть доступно (проверено)
- Если занято, нужно выбрать другое имя в `pyproject.toml`

### Ошибка: "HTTPError: 400 Client Error"
- Проверьте версию в `pyproject.toml` (1.3.0)
- Убедитесь что версия уникальна (не публиковалась ранее)

## Безопасность

- **Никогда не коммитьте токены в git!**
- Токен даёт доступ к вашему аккаунту PyPI
- Используйте `.gitignore` для конфигурационных файлов
- При утечке токена, отзовите его в настройках PyPI

## Ссылки

- PyPI: https://pypi.org
- Документация uv: https://docs.astral.sh/uv/guides/publishing/
- Документация twine: https://twine.readthedocs.io/