# services/vendor_service.py
from src.services.base_service import BaseService
from src.repositories.vendor_repository import VendorRepository
from src.repositories.event_repository import EventRepository
from src.factory.entity_factory import EntityFactory

class VendorService(BaseService):
    def __init__(self, vendor_repository=None, event_repository=None):
        self.repo = vendor_repository or VendorRepository()
        self.event_repo = event_repository or EventRepository()

    def create(self, name, services_offered, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        v = EntityFactory.create_vendor(name, services_offered, event_id)
        saved = self.repo.add(v)
        return saved.to_dict()

    def update(self, vendor_id, new_name=None, new_services=None):
        v = self.repo.get_by_id(vendor_id)
        if not v:
            return None
        if new_name and new_name.strip():
            v.name = new_name
        if new_services and new_services.strip():
            v.services = new_services
        updated = self.repo.add(v)
        return updated.to_dict()

    def delete(self, vendor_id):
        v = self.repo.get_by_id(vendor_id)
        if not v:
            return False
        self.repo.remove(v)
        return True

    def list_vendors(self, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        
        return [
            {
                "id": v.id,
                "display_name": f"{v.id}: {v.name}",
                "name": v.name,
                "services": v.services,
                "event_id": v.event_id,
                "event_name": event.name
            }
            for v in event.vendors
        ]