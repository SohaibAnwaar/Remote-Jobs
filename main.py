from scrappers.scrapper.glassdoor import get_scraper
from shared_layer.postgres.database import Database
from datetime import datetime


def main(db_obj):

    scrapper = get_scraper()
    insert_query = """
    INSERT INTO scraper_health (name)
    VALUES (%s) RETURNING id;
    """
    values = (scrapper.name,)
    result = db_obj.execute(insert_query, values)
    scraper_health_id = result[0]
    
    scrapper.scrap(scraper_health_id)
    print(result)


if __name__ == "__main__":
    db_obj = Database()
    main(db_obj)
