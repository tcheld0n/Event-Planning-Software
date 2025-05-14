# notifications/notification_manager.py

class NotificationManager:
    def __init__(self):
        # Dicionário onde as chaves são tipos de eventos e os valores são listas de funções
        self.listeners = {}
    
    def subscribe(self, event_type, listener_function):
        """Adiciona um ouvinte para um tipo de evento"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener_function)
    
    def notify(self, event_type, data=None):
        """Notifica todos os ouvintes interessados em um evento"""
        if event_type in self.listeners:
            for listener_function in self.listeners[event_type]:
                listener_function(data)

# Criando uma única instância global
notification_manager = NotificationManager()