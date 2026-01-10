"""
Migration script to add crypto payment fields to bounties table
Run this once to add the new columns to existing database
"""

import os
import sys
from sqlalchemy import text, inspect
from app.database import engine, Base
from app.config import settings
from loguru import logger

def migrate_add_crypto_fields():
    """Add crypto payment columns to bounties table if they don't exist"""
    
    logger.info("🔄 Starting migration: Add crypto payment fields to bounties table")
    
    # Check database type
    db_type = "PostgreSQL" if settings.DATABASE_URL.startswith("postgresql") else "SQLite"
    logger.info(f"Database type: {db_type}")
    
    with engine.connect() as conn:
        # Check if columns already exist
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('bounties')]
        
        logger.info(f"Existing columns: {columns}")
        
        # Columns to add
        columns_to_add = {
            'payment_method': "VARCHAR DEFAULT 'fiat'",
            'crypto_type': "VARCHAR",
            'crypto_wallet_address': "VARCHAR",
            'crypto_amount': "FLOAT"
        }
        
        # Add columns that don't exist
        for col_name, col_def in columns_to_add.items():
            if col_name not in columns:
                try:
                    if db_type == "PostgreSQL":
                        # PostgreSQL syntax
                        if col_name == 'payment_method':
                            sql = f"ALTER TABLE bounties ADD COLUMN {col_name} VARCHAR DEFAULT 'fiat'"
                        else:
                            sql = f"ALTER TABLE bounties ADD COLUMN {col_name} {col_def.split()[0]}"
                    else:
                        # SQLite syntax
                        sql = f"ALTER TABLE bounties ADD COLUMN {col_name} {col_def}"
                    
                    logger.info(f"Adding column {col_name}...")
                    conn.execute(text(sql))
                    conn.commit()
                    logger.info(f"✅ Added column: {col_name}")
                except Exception as e:
                    logger.error(f"❌ Error adding column {col_name}: {e}")
                    # Try to continue with other columns
            else:
                logger.info(f"⏭️  Column {col_name} already exists, skipping")
        
        logger.info("✅ Migration complete!")

if __name__ == "__main__":
    try:
        migrate_add_crypto_fields()
        print("✅ Migration completed successfully!")
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

