import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from shared_layer.postgres.database import Database

db = Database()


# Create leads Table
db.execute('''
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    title TEXT ,
    city VARCHAR(255) ,
    state VARCHAR(255) ,
    country VARCHAR(255) ,
    lead_date VARCHAR(255) ,
    lead_url TEXT ,
    company_url TEXT ,
    description TEXT ,
    platform VARCHAR(255) ,
    created_at TIMESTAMPTZ  DEFAULT NOW(),
    updated_at TIMESTAMPTZ  DEFAULT NOW()

);''')


# Create Scrapper Health Table
db.execute('''
CREATE TABLE IF NOT EXISTS scraper_health (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) ,
    leads_collected VARCHAR(255) ,
    time_taken VARCHAR(255) ,
    created_at TIMESTAMPTZ  DEFAULT NOW(),
    updated_at TIMESTAMPTZ  DEFAULT NOW()
    )
'''
)

# SQL Function query for created at and updated at
db.execute('''
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now(); 
    RETURN NEW;
END;
$$ language 'plpgsql';
''')



# Creating Trigger to update updated_at column
db.execute('''
CREATE TRIGGER update_scraper_health_modtime
BEFORE UPDATE ON scraper_health
FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();
''')

# Creating Trigger to update updated_at column
db.execute('''
CREATE TRIGGER leads_modtime
BEFORE UPDATE ON leads
FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();
''')



