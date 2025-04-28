import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run database migrations to add missing columns"""
    try:
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            logger.error("DATABASE_URL environment variable not set!")
            return False

        # Create engine
        engine = create_engine(database_url)
        
        # Connect to the database - create separate connections for checking and altering
        with engine.connect() as check_connection:
            # Check if columns exist first to avoid errors
            result = check_connection.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'tax_data' AND column_name = 'life_insurance'"
            ))
            life_insurance_exists = result.fetchone() is not None
            
            result = check_connection.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'tax_data' AND column_name = 'education_loan'"
            ))
            education_loan_exists = result.fetchone() is not None
        
        # Add missing columns if they don't exist
        if not life_insurance_exists or not education_loan_exists:
            with engine.connect() as alter_connection:
                with alter_connection.begin():
                    if not life_insurance_exists:
                        logger.info("Adding life_insurance column to tax_data table")
                        alter_connection.execute(text(
                            "ALTER TABLE tax_data ADD COLUMN life_insurance FLOAT DEFAULT 0"
                        ))
                        
                    if not education_loan_exists:
                        logger.info("Adding education_loan column to tax_data table")
                        alter_connection.execute(text(
                            "ALTER TABLE tax_data ADD COLUMN education_loan FLOAT DEFAULT 0"
                        ))
            
            logger.info("Migration completed successfully!")
            return True
            
    except SQLAlchemyError as e:
        logger.error(f"Database migration error: {str(e)}")
        return False

if __name__ == "__main__":
    run_migrations()