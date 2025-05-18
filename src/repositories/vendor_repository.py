# repositories/vendor_repository.py
from src.database.db import SessionLocal
from src.models.vendor import Vendor
from .base_repository import BaseRepository

class VendorRepository(BaseRepository):
    def add(self, supplier: Vendor) -> Vendor:
        session = SessionLocal()
        try:
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier
        finally:
            session.close()

    def get_by_id(self, supplier_id: int) -> Vendor | None:
        session = SessionLocal()
        try:
            return session.query(Vendor).filter(Vendor.id == supplier_id).first()
        finally:
            session.close()

    def list_all(self) -> list[Vendor]:
        session = SessionLocal()
        try:
            return session.query(Vendor).all()
        finally:
            session.close()

    def remove(self, supplier: Vendor) -> None:
        session = SessionLocal()
        try:
            session.delete(supplier)
            session.commit()
        finally:
            session.close()