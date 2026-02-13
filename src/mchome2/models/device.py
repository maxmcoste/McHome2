import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, String, Boolean, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mchome2.models.house import Base


class DeviceType(str, enum.Enum):
    temperature_sensor = "temperature_sensor"
    window_sensor = "window_sensor"
    boiler = "boiler"


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    house_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("houses.id", ondelete="CASCADE"), nullable=False)
    room_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=True)
    device_type: Mapped[DeviceType] = mapped_column(Enum(DeviceType), nullable=False)
    driver_name: Mapped[str] = mapped_column(String(100), nullable=False, default="simulator")
    config_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    house: Mapped["House"] = relationship("House", back_populates="devices")
    room: Mapped["Room | None"] = relationship("Room", back_populates="devices")
    temperature_readings: Mapped[list["TemperatureReading"]] = relationship("TemperatureReading", back_populates="device", cascade="all, delete-orphan")
    window_readings: Mapped[list["WindowReading"]] = relationship("WindowReading", back_populates="device", cascade="all, delete-orphan")
    boiler_events: Mapped[list["BoilerEvent"]] = relationship("BoilerEvent", back_populates="device", cascade="all, delete-orphan")


from mchome2.models.house import House  # noqa: E402, F811
from mchome2.models.room import Room  # noqa: E402, F811
from mchome2.models.reading import TemperatureReading, WindowReading, BoilerEvent  # noqa: E402, F811
