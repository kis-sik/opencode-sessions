# opencode-sessions

Утилита для управления сессиями OpenCode с интерфейсом как у `claude-sessions`.

## Установка

### Самодостаточная установка (рекомендуется)
Скрипт содержит встроенные команды установки:

```bash
# Установить для текущего пользователя
./opencode-sessions --install

# Установить системно (для всех пользователей, требует sudo)
sudo ./opencode-sessions --install-system

# Удалить для текущего пользователя
./opencode-sessions --uninstall

# Удалить системно (требует sudo)
sudo ./opencode-sessions --uninstall-system
```

### Ручная установка
1. Скопируйте скрипт в PATH:
```bash
cp opencode-sessions ~/.local/bin/
chmod +x ~/.local/bin/opencode-sessions
```

2. Установите автодополнение для Fish:
```bash
cp opencode-sessions.fish ~/.config/fish/completions/
```

3. Перезапустите терминал или выполните:
```bash
source ~/.config/fish/config.fish
```

## Использование

```
opencode-sessions                    # сессии для текущей директории
opencode-sessions --print-all        # все сессии
opencode-sessions --sort-date        # сортировка по дате (новые сверху)
opencode-sessions --sort-tokens      # сортировка по токенам (больше сверху)
opencode-sessions --sort-cost        # сортировка по стоимости (дороже сверху)
opencode-sessions --sort-messages    # сортировка по сообщениям (больше сверху)
opencode-sessions --stats            # статистика по проектам
opencode-sessions --delete <name>    # удалить по имени или UUID
opencode-sessions --delete-unnamed   # удалить все без кастомного имени
```

## Примеры

```bash
# Показать сессии текущего проекта
opencode-sessions

# Показать все сессии с сортировкой по токенам
opencode-sessions --print-all --sort-tokens

# Удалить сессию по имени
opencode-sessions --delete "Firewall"

# Показать статистику
opencode-sessions --stats
```

## Автодополнение в Fish

После установки файла автодополнения:
- Нажмите Tab для подсказок опций
- При использовании `--delete` Tab покажет доступные сессии
- Работает с любыми опциями из списка выше