DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'inventory') THEN
        CREATE DATABASE inventory;
    END IF;
END $$;
