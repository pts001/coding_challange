import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


# removes duplicate spaces
def remove_duplicate(value):
    return re.sub(' +', ' ', value)

def remove_newline(values):
    return re.sub(r'\n|\t|\r',"",values)

# removes duplicate spaces at start and end
def remove_whitespaces(value):
    return value.strip()

#clean address from sos spider
def clean_sos_address(value):
    return re.sub('Entity Mailing Address|Entity Mailing City, State, Zip','',value)

def clean_gtc(value):
    return value.split(':')[1]

#item processors for GTC spider
class GtcItems(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    address = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    reg_yr = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    license_no = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    license_type = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    ownership_type = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    status = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    county = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

    effective_date = scrapy.Field(
        input_processor = MapCompose(clean_gtc,remove_duplicate, remove_newline, remove_whitespaces),
        output_processor=TakeFirst()
    )

# item processors for SOS spider
class SosItem(scrapy.Item):
    # define the fields for your item here like:
    entity_mailing_address = scrapy.Field(
        input_processor = MapCompose(remove_tags, clean_sos_address,remove_whitespaces, remove_newline, remove_duplicate),
        output_processor=TakeFirst()
    )
