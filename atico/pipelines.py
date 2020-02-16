# -*- coding: utf-8 -*-
import json
from collections import defaultdict
import json
import logging

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker

from .models import (
    connect_db, create_schema, create_tables,
    Property, Price, Details, Multimedia, Agents, Additional, Resource
)

class RealEstateScrapersPipeline(object):
    def open_spider(self, spider):
        self.file = open('scraped_items.json', 'w')
        # Your scraped items will be saved in the file 'scraped_items.json'.
        # You can change the filename to whatever you want.
        self.file.write("[")

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(
            dict(item),
            indent=4,
            sort_keys=True,
            separators=(',', ': ')
        ) + ",\n"
        self.file.write(line)
        return item


class PostgresDBPipeline(object):

    def __init__(self):
        engine = connect_db()
        create_schema(engine, "real_estate")
        create_tables(engine)
        self.session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.session()

        # Process Resource
        try:
            # Check if Resource already exists
            resource = session.query(Resource).filter(
                Resource.url == item['resource_url']
            ).filter(
                Resource.title == item['resource_title']
            ).first()
            if not resource:
                # Create resource object with basic fields
                resource = Resource(
                    url=item["resource_url"],
                    title=item["resource_title"],
                    country=item["resource_country"]
                )
                session.add(resource)
                session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        # Process Property
        try:
            # Check if Property already exists
            property = session.query(Property).filter(
                Property.url == item['url']
            ).filter(
                Property.title == item['title']
            ).first()
            if not property:
                # Create property object with basic fields
                property = Property(
                    resource_id=resource.id,
                    active=item["active"],
                    url=item["url"],
                    title=item["title"],
                    subtitle=item["subtitle"],
                    location=item["location"],
                    extra_location=item["extra_location"],
                    body=item["body"]
                )
                session.add(property)
                session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        # Process Price
        try:
            price = Price(
                property_id=property.id,
                current_price=item['current_price'],
                original_price=item['original_price'],
                price_m2=item['price_m2'],
                area_market_price=item['area_market_price'],
                square_meters=item['square_meters']
            )
            session.add(price)
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        # Process Details
        try:
            details = Details(
                property_id=property.id,
                area=item['area'],
                tags=item['tags'],
                bedrooms=item['bedrooms'],
                bathrooms=item['bathrooms'],
                last_update=item['last_update'],
                certification_status=item['certification_status'],
                consumption=item['consumption'],
                emissions=item['emissions'],
            )
            session.add(details)
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        # Process Multimedia
        try:
            multimedia = Multimedia(
                property_id=property.id,
                main_image_url=item['main_image_url'],
                image_urls=item['image_urls'],
                floor_plan=item['floor_plan'],
                energy_certificate=item['energy_certificate'],
                video=item['video'],
            )
            session.add(multimedia)
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        # Process Agents
        try:
            agents = Agents(
                property_id=property.id,
                seller_type=item['seller_type'],
                agent=item['agent'],
                ref_agent=item['ref_agent'],
                source=item['source'],
                ref_source=item['ref_source'],
                phone_number=item['phone_number'],
            )
            session.add(agents)
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        # Process Additional
        try:
            additional = Additional(
                property_id=property.id,
                additional_url=item['additional_url'],
                published=item['published'],
                scraped_ts=item['scraped_ts'],
            )
            session.add(additional)
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            logging.error(e)
            return item

        session.close()
        return item

