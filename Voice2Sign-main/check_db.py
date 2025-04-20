import sqlite3
import os

# Path to your databases
db_dir = os.path.join(os.getcwd(), "databases")
db_files = {
    "Hindi": "hindi.db",
    "English": "english.db",
    "Marathi": "marathi.db"
}

def check_db(name, file):
    print(f"\n🔍 Checking {name} Database: {file}")
    db_path = os.path.join(db_dir, file)
    
    if not os.path.exists(db_path):
        print(f"❌ {file} does not exist.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Show tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📄 Tables: {tables}")

        # Try to fetch contents from common table
        for table_name in ["language_content", "isl_sign"]:
            try:
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                print(f"\n📑 Content in '{table_name}':")
                for row in rows:
                    print(row)
            except sqlite3.OperationalError:
                print(f"⚠️ Table '{table_name}' not found.")
                
        conn.close()

    except Exception as e:
        print(f"❗ Error with {file}: {e}")

# Run for all DBs
for lang, file in db_files.items():
    check_db(lang, file)
