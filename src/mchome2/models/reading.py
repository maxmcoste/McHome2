import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, String, Float, Boolean, Integer, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mchome2.models.house import Base


class BoilerAction(str, enum.Enum):
    on = "on"
    off = "off"


class TemperatureReading(Base):
    __tablename__ = "temperature_readings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    device: Mapped["Device"] = relationship("Device", back_populates="temperature_readings")
    room: Mapped["Room"] = relationship("Room", back_populates="temperature_readings")


class WindowReading(Base):
    __tablename__ = "window_readings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    device: Mapped["Device"] = relationship("Device", back_populates="window_readings")
    room: Mapped["Room"] = relationship("Room", back_populates="window_readings")


class BoilerEvent(Base):
    __tablename__ = "boiler_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    house_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("houses.id", ondelete="CASCADE"), nullable=False)
    action: Mapped[BoilerAction] = mapped_column(Enum(BoilerAction), nullable=False)
    triggered_by: Mapped[str] = mapped_column(String(50), nullable=False, default="prediction")
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    device: Mapped["Device"] = relationship("Device", back_populates="boiler_events")
    house: Mapped["House"] = relationship("House", back_populates="boiler_events")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    house_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("houses.id", ondelete="CASCADE"), nullable=False)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    predicted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    schedule_json: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    horizon_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=240)

    house: Mapped["House"] = relationship("House", back_populates="predictions")
    room: Mapped["Room"] = relationship("Room", back_populates="predictions")


from mchome2.models.device import Device  # noqa: E402, F811
from mchome2.models.room import Room  # noqa: E402, F811
from mchome2.models.house import House  # noqa: E402, F811
