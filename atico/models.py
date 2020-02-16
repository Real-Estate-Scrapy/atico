from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    BigInteger, create_engine, Date, DateTime, Float,
    ForeignKey, Integer, String, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from scrapy.utils.project import get_project_settings
from sqlalchemy.sql.ddl import CreateSchema

Base = declarative_base()


def connect_db():
    s = get_project_settings()
    return create_engine(URL(**s['DATABASE']))


def create_tables(engine, drop_tables=False):
    if drop_tables:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_schema(engine, schema_name):
    if not engine.dialect.has_schema(engine, schema_name):
        engine.execute(CreateSchema(schema_name))


class Resource(Base):
    __tablename__ = 'resource'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
            UUID(as_uuid=True),
            primary_key=True,
            unique=True,
            default=uuid.uuid4
        )

    url = Column(String)
    title = Column(String)
    country = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


class Property(Base):
    __tablename__ = 'property'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    resource_id = Column(UUID(as_uuid=True), ForeignKey('real_estate.resource.id'))

    active = Column(Boolean, unique=False)
    url = Column(String)
    title = Column(String)
    subtitle = Column(String)
    location = Column(String)
    extra_location = Column(String)
    body = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


class Price(Base):
    __tablename__ = 'property_price'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )
    property_id = Column(UUID(as_uuid=True), ForeignKey('real_estate.property.id'))
    current_price = Column(String)
    original_price = Column(String)
    price_m2 = Column(String)
    area_market_price = Column(String)
    square_meters = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


class Details(Base):
    __tablename__ = 'property_details'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )
    property_id = Column(UUID(as_uuid=True), ForeignKey('real_estate.property.id'))
    area = Column(String)
    tags = Column(String)
    bedrooms = Column(String)
    bathrooms = Column(String)
    last_update = Column(String)
    certification_status = Column(String)
    consumption = Column(String)
    emissions = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


class Multimedia(Base):
    __tablename__ = 'property_multimedia'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )
    property_id = Column(UUID(as_uuid=True), ForeignKey('real_estate.property.id'))
    main_image_url = Column(String)
    image_urls = Column(String)
    floor_plan = Column(String)
    energy_certificate = Column(String)
    video = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


class Agents(Base):
    __tablename__ = 'property_agents'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )
    property_id = Column(UUID(as_uuid=True), ForeignKey('real_estate.property.id'))
    seller_type = Column(String)
    agent = Column(String)
    ref_agent = Column(String)
    source = Column(String)
    ref_source = Column(String)
    phone_number = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


class Additional(Base):
    __tablename__ = 'property_aditional'
    __table_args__ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )
    property_id = Column(UUID(as_uuid=True), ForeignKey('real_estate.property.id'))
    additional_url = Column(String)
    published = Column(String)
    scraped_ts = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)


