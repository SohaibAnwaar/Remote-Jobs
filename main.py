# Description: This is the main file for the scraper. It will be called by the cron job.
from threading import Thread
from shared_layer.kafka.consumer import KafkaConsumerBridge
from scrappers.scrapper.glassdoor import get_scraper
from shared_layer.postgres.database import Database
from datetime import datetime
from shared_layer.variables import in_progress
import json
import importlib.util
import sys, time
    

scrappers = []

def get_scraper():
    """
    Get available scrappers from the `scrappers/scrapper/available_scrappers.json` file.
    import the scrapers and return the scrapper object
    """
    global scrappers
    with open("scrappers/scrapper/available_scrappers.json") as f:
        available_scrappers = json.load(f)
    for name, path in available_scrappers.items():
        spec = importlib.util.spec_from_file_location(name, path)
        foo = importlib.util.module_from_spec(spec)
        sys.modules[name] = foo
        spec.loader.exec_module(foo)
        available_scrappers[name] = foo.get_scraper()
    return available_scrappers

def main(db_obj):
    global scrappers, available_scrappers
    # Get available scrappers
    available_scrappers = get_scraper()
    # simutaniously run 5 scrapers
    while True:
        
        for name in available_scrappers:
            insert_query = """
            INSERT INTO scraper_health (name)
            VALUES (%s) RETURNING id;
            """
            values = (name,)
            result = db_obj.execute(insert_query, values)
            scraper_health_id = result[0]
            scrapper_object= available_scrappers[name]
            if scrapper_object:
                
                print("in Progress", in_progress.get_jobs())
                # If the scrapper is already running then skip it
                if in_progress.get_job_count() > 5:
                    print(f"Already in progress {name}")
                    break
                
                thread = Thread(target = scrapper_object.scrap, args = (scraper_health_id, ))
                thread.start()

                print(scrapper_object)
        time.sleep(3)
        
if __name__ == "__main__":
    # Initilizing Kafka Consumer
    kafka_bridge = KafkaConsumerBridge()
    # Run the function in background
    Thread(target=kafka_bridge.kafka_to_postgres).start()

    db_obj = Database()
    main(db_obj)