# Database connection parameters
import os
import pandas as pd

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = int(os.getenv('POSTGRES_PORT'))
database = os.getenv('POSTGRES_DATABASE')

# Create a connection string
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

def save_to_database(df, table_name, primary_key_column, foreign_keys=None):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Successfully saved '{str(len(df))}' records to '{table_name}' in PostgreSQL.")
        # Add primary key constraint
        conn = engine.connect()

        # Step 1: Ensure the column is NOT NULL and unique
        conn.execute(text(f"ALTER TABLE {table_name} ALTER COLUMN {primary_key_column} SET NOT NULL;"))
        conn.execute(text(f"CREATE UNIQUE INDEX IF NOT EXISTS {primary_key_column}_unique_idx ON {table_name}({primary_key_column});"))

        # Step 2: Create a sequence and link it to the column
        sequence_name = f"{table_name}_{primary_key_column}_seq"
        conn.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {sequence_name} OWNED BY {table_name}.{primary_key_column};"))
        conn.execute(text(f"ALTER TABLE {table_name} ALTER COLUMN {primary_key_column} SET DEFAULT nextval('{sequence_name}');"))

        # Step 3: Sync the sequence with the current max value of the column
        conn.execute(text(f"SELECT setval('{sequence_name}', COALESCE(MAX({primary_key_column}), 1)) FROM {table_name};"))

        # Step 4: Add the primary key constraint
        conn.execute(text(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({primary_key_column});"))

        print(f"Auto-increment and primary key added to column {primary_key_column} in table {table_name}.")

        print(f"Primary key added on column '{primary_key_column}'.")
        
        if foreign_keys:
            for fk in foreign_keys:
                conn.execute(text(
                    f"ALTER TABLE {table_name} "
                    f"ADD CONSTRAINT fk_{fk['column']} "
                    f"FOREIGN KEY ({fk['column']}) "
                    f"REFERENCES {fk['referenced_table']} ({fk['referenced_column']});"
                ))
                print(f"Foreign key constraint added: '{fk['column']}' references '{fk['referenced_table']}({fk['referenced_column']})'.")
        conn.commit()
    except Exception as e:
        print("Error while saving DataFrame in chunks:", e)
    finally:
        conn.close()


def create_dataframe_for_table(table_name):
    try:
        conn = engine.connect()
        query = f"SELECT * FROM {table_name};"  # Replace 'doctors' with your table name

        # Load data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def select_one_row(query):
    try:
        conn = engine.connect()
        result = conn.execute(query)
        data = result.fetchone()
        return data
    except Exception as e:
        print("Database error:", e)
        return None
    finally:
        conn.close()