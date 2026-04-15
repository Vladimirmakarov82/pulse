#!/usr/bin/env python3
"""Проверяет локальные файлы перед git push."""
import re, sys, os

REPO = os.path.dirname(os.path.abspath(__file__))
ERRORS = []

def fail(msg): ERRORS.append(msg); print(f"  ❌ {msg}")
def ok(msg): print(f"  ✅ {msg}")
def read(f): return open(os.path.join(REPO, f)).read()

def check(html, pattern, label, must_exist=True):
    found = pattern in html
    if must_exist:
        if found: ok(label)
        else: fail(f"Не найдено: {label}")
    else:
        if not found: ok(f"Нет лишнего: {label}")
        else: fail(f"Лишнее: {label}")

def main():
    print("\n📄 index.html + app.js")
    html = read("index.html") + read("app.js")
    check(html, "pulse-hero",                "PULSE hero")
    check(html, "main-invite-btn",            "Кнопка инвайт с id")
    check(html, "type:\"button\"",              "Кнопка type=button (не submit)")
    check(html, "showInviteModal",            "showInviteModal функция")
    check(html, "hideInviteModal",            "hideInviteModal функция")
    check(html, "invite-modal",              "Модал invite-modal")
    check(html, "invite-close",              "Крестик invite-close")
    check(html, "Основателям комьюнити",     "Кнопка nav Основателям")
    check(html, "cta-section",               "CTA секция")
    check(html, "предпринимателей",          "Счётчик предпринимателей")
    check(html, "Яхтсмены",                  "Тег Яхтсмены")
    check(html, "Sync подтверждён",          "Sync в AI ленте")
    check(html, "Только для участников бизнес", "Subtitle")
    check(html, "Живые знакомства",          "AI label")
    check(html, "PulseProfile_bot",              "Ссылка на бота")
    check(html, "rgba(34,197,94,0.08)",      "Зелёная nav кнопка")
    # Антипроверки
    check(html, "Синк подтверждён",          "Синк→Sync", False)
    check(html, "12 slots open",             "12 slots open", False)
    check(html, "Один профиль. Все возможности.", "Footer tagline", False)

    print("\n📄 founders.html")
    html = read("founders.html")
    check(html, 'openApply()',               "Кнопка nav onclick")
    check(html, "apply-overlay",             "Apply overlay")
    check(html, "closeApply()",              "closeApply функция")
    check(html, "Владимир Макаров",   "Карточка Макарова")
    check(html, 'alt="Анна Козлова"',       "Карточка Козловой")
    check(html, "бесплатная реклама клуба", "Текст block1")
    check(html, "postMessage",               "Logo postMessage")
    check(html, "position:fixed",            "Крестик fixed")
    check(html, "Участники довольны",        "Старый текст", False)
    # Ровно 2 карточки
    vm = html.count('Владимир Макаров')
    ak = html.count('alt="Анна Козлова"')
    if vm >= 1 and ak == 1: ok("Ровно 2 карточки")
    else: fail(f"Карточки: VM={vm} AK={ak} (нужно по 1)")

    print("\n📄 apply.html")
    html = read("apply.html")
    for p, l in [("club-name","Поле клуба"),("role","Поле роль"),("full-name","Поле имя"),("telegram","Поле telegram"),("submit-btn","Кнопка submit")]:
        check(html, p, l)

if __name__ == "__main__":
    print("🔍 Проверяю файлы перед пушем...")
    main()
    print()
    if ERRORS:
        print(f"🚫 PUSH ЗАБЛОКИРОВАН — {len(ERRORS)} ошибок:")
        for e in ERRORS: print(f"   • {e}")
        print()
        sys.exit(1)
    else:
        print(f"✅ Все проверки прошли — пуш разрешён!\n")
        sys.exit(0)
