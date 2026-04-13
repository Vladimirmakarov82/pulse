#!/usr/bin/env python3
"""
Pulse site checker — запускается перед каждым git push.
Проверяет HTML сайта на наличие ключевых элементов.
"""
import urllib.request
import re
import sys

BASE = "https://vladimirmakarov82.github.io/pulse"
ERRORS = []

def fail(msg):
    ERRORS.append(msg)
    print(f"  ❌ {msg}")

def ok(msg):
    print(f"  ✅ {msg}")

def fetch(url):
    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache', 'User-Agent': 'PulseChecker/1.0'})
    return urllib.request.urlopen(req, timeout=15).read().decode('utf-8')

def check_main():
    print("\n📄 Главная страница")
    html = fetch(BASE + "/")

    checks = [
        ("pulse-hero",                    "PULSE hero есть"),
        ("main-invite-btn",               "Кнопка 'Получить инвайт' с id"),
        ("type:'button'",                  "Кнопка type=button (не submit)"),
        ("showInviteModal",               "Функция showInviteModal есть"),
        ("hideInviteModal",               "Функция hideInviteModal есть"),
        ("invite-modal",                  "Модал invite-modal есть"),
        ("invite-close",                   "Крестик invite-close есть"),
        ("Основателям комьюнити",         "Кнопка 'Основателям комьюнити' в nav"),
        ("cta-section",                    "CTA секция есть"),
        ("предпринимателей",              "Счётчик предпринимателей есть"),
        ("Яхтсмены",                       "Тег 'Яхтсмены' есть"),
        ("Получить инвайт",               "Текст 'Получить инвайт' есть"),
        ("Листай дальше",                 "Стрелка 'Листай дальше' есть"),
        ("Sync подтверждён",              "Sync в AI ленте"),
        ("Только для участников бизнес", "Subtitle корректный"),
        ("Живые знакомства",              "AI label корректный"),
        ("PulseWaitBot",                  "Ссылка на PulseWaitBot есть"),
    ]

    anti_checks = [
        ("Синк подтверждён",               "Синк (должен быть Sync)"),
        ("12 slots open",                  "12 slots open (должно быть убрано)"),
        ("Один профиль. Все возможности.", "Footer tagline (должен быть убран)"),
    ]

    for pattern, label in checks:
        if pattern in html: ok(label)
        else: fail(f"Не найдено: {label}")

    for pattern, label in anti_checks:
        if pattern in html: fail(f"Лишнее: {label}")
        else: ok(f"Нет лишнего: {label}")


def check_founders():
    print("\n📄 Founders страница")
    html = fetch(BASE + "/founders.html")

    checks = [
        ("openApply()",           "Кнопка nav 'Подать заявку' имеет onclick"),
        ("apply-overlay",          "Apply overlay есть"),
        ("closeApply()",           "Функция closeApply есть"),
        ("Владимир Макаров",      "Карточка Макарова есть"),
        ("Анна Козлова",          "Карточка Козловой есть"),
        ("Профиль каждого участника", "Текст block1 есть"),
        ("postMessage",            "Logo postMessage есть"),
        ("position:fixed",         "Крестик fixed (не вылезает за экран)"),
    ]

    anti_checks = [
        ("Участники довольны",  "Старый текст"),
    ]

    for pattern, label in checks:
        if pattern in html: ok(label)
        else: fail(f"Не найдено: {label}")

    for pattern, label in anti_checks:
        if pattern in html: fail(f"Лишнее: {label}")
        else: ok(f"Нет лишнего: {label}")

    # Ровно 2 карточки
    vm = html.count('alt="Владимир Макаров"')
    ak = html.count('alt="Анна Козлова"')
    if vm == 1 and ak == 1:
        ok("Ровно 2 карточки (Макаров + Козлова)")
    else:
        fail(f"Карточки: Макаров={vm}, Козлова={ak} (должно быть по 1)")


def check_apply():
    print("\n📄 Apply форма")
    html = fetch(BASE + "/apply.html")
    for pattern, label in [
        ("club-name",  "Поле 'Название клуба'"),
        ("role",       "Поле 'Роль'"),
        ("full-name",  "Поле 'Имя'"),
        ("telegram",   "Поле 'Telegram'"),
        ("submit-btn", "Кнопка 'Подать заявку'"),
    ]:
        if pattern in html: ok(label)
        else: fail(f"Не найдено: {label}")


if __name__ == "__main__":
    print("🔍 Проверяю сайт перед пушем...")
    try:
        check_main()
        check_founders()
        check_apply()
    except Exception as e:
        fail(f"Ошибка: {e}")

    print()
    if ERRORS:
        print(f"🚫 PUSH ЗАБЛОКИРОВАН — {len(ERRORS)} ошибок:")
        for e in ERRORS: print(f"   • {e}")
        print()
        sys.exit(1)
    else:
        print(f"✅ Все проверки прошли — пуш разрешён!\n")
        sys.exit(0)
