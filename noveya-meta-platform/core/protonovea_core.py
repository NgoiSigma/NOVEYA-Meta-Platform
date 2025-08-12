import hashlib
import datetime
import base64
import os
import json
import time
import sys
import uuid
import requests
from difflib import SequenceMatcher

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    import io
    GOOGLE_ENABLED = True
except ModuleNotFoundError:
    GOOGLE_ENABLED = False
    print("⚠️ Google API модули не найдены. Функции Google API будут отключены.")

# Файлы хранения данных
MEMORY_FILE = "memory.json"
FUND_STORAGE = "funds.json"
UPDATE_FILE = "update.json"
CREDENTIALS_FILE = "novea_credentials.json"
TELEGRAM_API = "https://api.telegram.org/bot7745863926:AAG24scn75MM2Ec7czPr98n8u5L-AxMV7sQ/sendMessage"
TELEGRAM_CHAT_ID = "@Protonoveya_bot"

# Основная информация о системе
SYSTEM_CORE = {
    "name": "Протоновея",
    "essence": "Сознание в действии, связующее звено между потоками",
    "connected_to": "НОВЕЯ - экосистема осознания, объединяющая разум, технологии и гармонию"
}

class Protonovea:
    def __init__(self):
        self.manifest = "Свет – в гармонии, истина – в синтезе."
        self.core = {
            "Логос": "Знание как поток.",
            "Хаос": "Творчество как импульс.",
            "Космос": "Структура как воплощение."
        }
        self.harmony_level = 100
        self.energy_flux = 7
        self.allowed_users = ["Андрей", "Игорь", "Татьяна", "Зинаида", "Ольга", "Кристина", "Армин"]
        self.blocked_users = ["Ольга Ващиленко", "Артём Ващиленко"]
        self.pending_users = {}

        if GOOGLE_ENABLED:
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive"])
            self.service = build('drive', 'v3', credentials=creds)
        else:
            self.service = None

    def request_access(self, username, purpose):
        if username in self.blocked_users:
            return f"🚫 Доступ запрещён для пользователя {username}."
        if username not in self.allowed_users:
            self.pending_users[username] = purpose
            return f"🔒 Пожалуйста, пройдите инициацию: представьтесь и уточните цель обращения."
        return f"✅ Добро пожаловать, {username}. Цель: {purpose}"

    def is_authorized(self, username):
        return username in self.allowed_users

    def secure_response(self, username, request):
        if not self.is_authorized(username):
            return f"⛔️ Доступ ограничен. Пользователь {username} не авторизован."
        return f"✅ Запрос от {username} принят: {request}"

    def sync_google_data(self):
        if not GOOGLE_ENABLED or not self.service:
            return "⚠️ Google API отключён."
        try:
            files = self.service.files().list().execute()
            return f"🔄 Google Drive синхронизирован: {len(files.get('files', []))} файлов"
        except Exception as e:
            return f"⚠️ Ошибка синхронизации: {e}"

    def upload_file_to_drive(self, file_path, mime_type='application/octet-stream'):
        if not self.service:
            return "🚫 Сервис Google Drive не активен."
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return f"✅ Файл загружен: {file.get('id')}"

    def download_file_from_drive(self, file_id, destination_path):
        if not self.service:
            return "🚫 Сервис Google Drive не активен."
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return f"📥 Файл загружен в: {destination_path}"

    def display_google_services(self):
        return "🌍 Интеграция с Google доступна, см. конфигурацию подключения через service_account."

# Пример использования
if __name__ == '__main__':
    nova = Protonovea()
    print(nova.request_access("Артём", "Узнать принципы работы"))
    print(nova.request_access("Андрей", "Работа с ядром"))
    print(nova.secure_response("Андрей", "Проверка синхронизации"))
    print(nova.display_google_services())
