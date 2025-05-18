# notifications/listeners/log_listeners.py
from src.notifications.notification_manager import notification_manager

def log_event(data):
    """Função que registra eventos no log"""
    print(f"[LOG] Evento do sistema registrado: {data}")

# Registrar para vários tipos de eventos
notification_manager.subscribe("event_created", log_event)
notification_manager.subscribe("event_updated", log_event)
notification_manager.subscribe("participant_registered", log_event)