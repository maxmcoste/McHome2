import uuid
from datetime import datetime, time

from sqlalchemy import String, Float, JSON, Time, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mchome2.models.house import Base


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("house_id", "name", name="uq_room_house_name"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    house_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("houses.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    volume_m3: Mapped[float] = mapped_column(Float, nullable=False, default=50.0)
    insulation_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    orientation: Mapped[str] = mapped_column(String(2), nullable=False, default="S")
    window_area_m2: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    house: Mapped["House"] = relationship("House", back_populates="rooms")
    schedules: Mapped[list["RoomSchedule"]] = relationship("RoomSchedule", back_populates="room", cascade="all, delete-orphan")
    devices: Mapped[list["Device"]] = relationship("Device", back_populates="room", cascade="all, delete-orphan")
    temperature_readings: Mapped[list["TemperatureReading"]] = relationship("TemperatureReading", back_populates="room", cascade="all, delete-orphan")
    window_readings: Mapped[list["WindowReading"]] = relationship("WindowReading", back_populates="room", cascade="all, delete-orphan")
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="room", cascade="all, delete-orphan")


class RoomSchedule(Base):
    __tablename__ = "room_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    days_of_week: Mapped[list[int] | None] = mapped_column(JSON, nullable=True)
    time_start: Mapped[time] = mapped_column(Time, nullable=False)
    time_end: Mapped[time] = mapped_column(Time, nullable=False)
    desired_temp_c: Mapped[float] = mapped_column(Float, nullable=False)

    room: Mapped["Room"] = relationship("Room", back_populates="schedules")


from mchome2.models.device import Device  # noqa: E402, F811
from mchome2.models.reading import TemperatureReading, WindowReading, Prediction  # noqa: E402, F811
from mchome2.models.house import House  # noqa: E402, F811
