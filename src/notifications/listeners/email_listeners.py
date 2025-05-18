# notifications/listeners/email_listeners.py
from src.notifications.notification_manager import notification_manager

def send_event_created_email(event):
    """Função que será chamada quando um evento for criado"""
    print(f"[EMAIL] Novo evento criado: {event.name}")
    # Aqui deve ser conectado a um serviço real de email

def send_participant_registered_email(data):
    """Função que será chamada quando um participante se registrar"""
    event = data.get("event")
    participant = data.get("participant")
    print(f"[EMAIL] Confirmação para {participant.name} no evento {event.name}")

# Registrar as funções no gerenciador de notificações
notification_manager.subscribe("event_created", send_event_created_email)
notification_manager.subscribe("participant_registered", send_participant_registered_email)