# opencode-sessions

Утилита для управления сессиями OpenCode с интерфейсом как у `claude-sessions`.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Особенности

- 📊 **Табличный вывод** с статистикой токенов, стоимости и сообщений
- 🔄 **Сортировка** по дате, токенам, стоимости, сообщениям
- 🗑️ **Удаление сессий** по имени или UUID
- 📈 **Детальная статистика** по проектам
- 🐟 **Автодополнение** для Fish shell
- 🔧 **Самодостаточная установка** - скрипт устанавливает сам себя
- 🎯 **Интерфейс как у claude-sessions** - знакомый UX

## Установка

### Быстрая установка (рекомендуется)
```bash
# Скачать и установить одной командой
curl -sL https://raw.githubusercontent.com/yourusername/opencode-sessions/main/opencode-sessions | python3 - --install
```

### Из исходников
```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/opencode-sessions.git
cd opencode-sessions

# Установить для текущего пользователя
./opencode-sessions --install

# Или установить системно (для всех пользователей)
sudo ./opencode-sessions --install-system
```

### Ручная установка
```bash
# Скопировать скрипт
cp opencode-sessions ~/.local/bin/
chmod +x ~/.local/bin/opencode-sessions

# Установить автодополнение Fish
cp opencode-sessions.fish ~/.config/fish/completions/
source ~/.config/fish/config.fish
```

## Удаление
```bash
# Удалить для текущего пользователя
opencode-sessions --uninstall

# Удалить системно
sudo opencode-sessions --uninstall-system
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

После установки:
- `opencode-sessions <Tab>` - подсказки опций
- `opencode-sessions --delete <Tab>` - список доступных сессий
- Работает со всеми флагами

## Лицензия

MIT License - смотрите файл [LICENSE](LICENSE)