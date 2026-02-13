import uuid
from datetime import datetime

from sqlalchemy import String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class House(Base):
    __tablename__ = "houses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="UTC")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    rooms: Mapped[list["Room"]] = relationship("Room", back_populates="house", cascade="all, delete-orphan")
    devices: Mapped[list["Device"]] = relationship("Device", back_populates="house", cascade="all, delete-orphan")
    boiler_events: Mapped[list["BoilerEvent"]] = relationship("BoilerEvent", back_populates="house", cascade="all, delete-orphan")
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="house", cascade="all, delete-orphan")


# Import for type resolution - these are resolved at runtime
from mchome2.models.room import Room  # noqa: E402, F811
from mchome2.models.device import Device  # noqa: E402, F811
from mchome2.models.reading import BoilerEvent, Prediction  # noqa: E402, F811
