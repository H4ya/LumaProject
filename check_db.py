import psycopg2

try:
    conn = psycopg2.connect(
        dbname='lumaDB',
        user='postgres',
        password='0262',
        host='127.0.0.1',
        port='5432'
    )
    cur = conn.cursor()
    
    # Check which tables exist
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public'
        ORDER BY table_name
    """)
    
    tables = cur.fetchall()
    print("\n=== TABLES IN DATABASE ===")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check if our specific tables exist
    required_tables = ['students', 'topics', 'saves', 'likes', 'notes']
    print("\n=== CHECKING REQUIRED TABLES ===")
    for table_name in required_tables:
        cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema='public' AND table_name='{table_name}')")
        exists = cur.fetchone()[0]
        status = "✓ EXISTS" if exists else "✗ MISSING"
        print(f"  {table_name}: {status}")
        
        if exists:
            cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table_name}' ORDER BY ordinal_position")
            columns = cur.fetchall()
            for col in columns:
                print(f"      - {col[0]} ({col[1]})")
    
    cur.close()
    conn.close()
    print("\n✓ Database connection successful!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
