from database.db import SessionLocal
from models.vendor import Vendor
from models.event import Event
from services.base_service import BaseService

class VendorService(BaseService):
    def create(self, event_id, name, services_offered):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            vendor = Vendor(name=name, services=services_offered, event_id=event_id)
            session.add(vendor)
            session.commit()
            session.refresh(vendor)
            return vendor.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update(self, vendor_id, new_name=None, new_services=None):
        session = SessionLocal()
        try:
            vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
            if not vendor:
                return None
            if new_name and new_name.strip():
                vendor.name = new_name
            if new_services and new_services.strip():
                vendor.services = new_services
            session.commit()
            return vendor.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, vendor_id):
        session = SessionLocal()
        try:
            vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
            if not vendor:
                return False
            session.delete(vendor)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Método adicional para listar vendors de um evento:
    def list_vendors(self, event_id):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            return [vendor.to_dict() for vendor in event.vendors]
        finally:
            session.close()
