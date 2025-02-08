import sqlite3

class DatabaseManager:
    def __init__(self, db_name="app.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        c = self.conn.cursor()
        # Users table: includes role and landlord_id (if tenant)
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE,
                name TEXT,
                profile_pic TEXT,
                role TEXT,
                landlord_id INTEGER
            )
        """)
        # Migration: add password column if it doesn't exist
        c.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in c.fetchall()]
        if "password" not in columns:
            c.execute("ALTER TABLE users ADD COLUMN password TEXT")
        # Messages table: store sender and recipient
        c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                recipient_id INTEGER,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(sender_id) REFERENCES users(id),
                FOREIGN KEY(recipient_id) REFERENCES users(id)
            )
        """)
        # Statuses: for landlords
        c.execute("""
            CREATE TABLE IF NOT EXISTS statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        # Groups: each landlord has one group
        c.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                owner_id INTEGER,
                FOREIGN KEY(owner_id) REFERENCES users(id)
            )
        """)
        # Group members linking tenants to a landlord’s group
        c.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                group_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(group_id) REFERENCES groups(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        # Rooms for apartment management
        c.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE,
                tenant_id INTEGER,
                FOREIGN KEY(tenant_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()
    
    # User functions
    def add_user(self, phone, name, role, landlord_id=None, password=None):
        c = self.conn.cursor()
        if role == "landlord" and not password:
            raise ValueError("Password required for landlord")
        try:
            c.execute("INSERT INTO users (phone, name, password, role, landlord_id) VALUES (?, ?, ?, ?, ?)", 
                      (phone, name, password, role, landlord_id))
            self.conn.commit()
            user_id = c.lastrowid
            is_new = True
        except sqlite3.IntegrityError:
            c.execute("SELECT id, password FROM users WHERE phone = ?", (phone,))
            row = c.fetchone()
            if row:
                user_id, stored_pwd = row
                is_new = False
                if role == "landlord" and stored_pwd != password:
                    raise ValueError("Incorrect password for landlord")
            else:
                raise
        if role == "landlord" and is_new:
            c.execute("SELECT id FROM groups WHERE owner_id = ?", (user_id,))
            if not c.fetchone():
                group_name = f"Group of {name}"
                c.execute("INSERT INTO groups (name, owner_id) VALUES (?, ?)", (group_name, user_id))
                self.conn.commit()
                group_id = c.lastrowid
                self.add_user_to_group(group_id, user_id)
        return user_id
    
    def update_user_profile(self, user_id, name=None, profile_pic=None):
        c = self.conn.cursor()
        if name:
            c.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
        if profile_pic:
            c.execute("UPDATE users SET profile_pic = ? WHERE id = ?", (profile_pic, user_id))
        self.conn.commit()
    
    def get_user(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT id, phone, name, profile_pic, role, landlord_id FROM users WHERE id = ?", (user_id,))
        return c.fetchone()
    
    def get_user_by_phone(self, phone):
        c = self.conn.cursor()
        c.execute("SELECT id, phone, name, role FROM users WHERE phone = ?", (phone,))
        return c.fetchone()
    
    # Messaging functions
    def add_message(self, sender_id, recipient_id, content):
        c = self.conn.cursor()
        c.execute("INSERT INTO messages (sender_id, recipient_id, content) VALUES (?, ?, ?)",
                  (sender_id, recipient_id, content))
        self.conn.commit()
    
    def get_messages_between(self, user_id, target_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT m.timestamp, m.content, u.name
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE (m.sender_id = ? AND m.recipient_id = ?)
               OR (m.sender_id = ? AND m.recipient_id = ?)
            ORDER BY m.timestamp
        """, (user_id, target_id, target_id, user_id))
        return c.fetchall()
    
    def get_conversation_partners(self, user_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT DISTINCT
                CASE WHEN sender_id = ? THEN recipient_id ELSE sender_id END AS partner_id
            FROM messages
            WHERE sender_id = ? OR recipient_id = ?
        """, (user_id, user_id, user_id))
        rows = c.fetchall()
        partners = []
        for row in rows:
            partner_id = row[0]
            c.execute("SELECT id, phone, name FROM users WHERE id = ?", (partner_id,))
            partner = c.fetchone()
            if partner:
                partners.append(partner)
        return partners
    
    # Status functions
    def add_status(self, user_id, status):
        c = self.conn.cursor()
        c.execute("INSERT INTO statuses (user_id, status) VALUES (?, ?)", (user_id, status))
        self.conn.commit()
    
    def get_statuses_for_group(self, owner_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT s.timestamp, s.status, u.name
            FROM statuses s
            JOIN users u ON s.user_id = u.id
            WHERE u.id = ?
            ORDER BY s.timestamp DESC
        """, (owner_id,))
        return c.fetchall()
    
    # Group functions
    def add_group(self, name, owner_id):
        c = self.conn.cursor()
        c.execute("INSERT INTO groups (name, owner_id) VALUES (?, ?)", (name, owner_id))
        self.conn.commit()
        return c.lastrowid
    
    def add_user_to_group(self, group_id, user_id):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO group_members (group_id, user_id) VALUES (?, ?)", (group_id, user_id))
        self.conn.commit()
    
    def get_group_by_owner(self, owner_id):
        c = self.conn.cursor()
        c.execute("SELECT id FROM groups WHERE owner_id = ?", (owner_id,))
        row = c.fetchone()
        return row[0] if row else None
    
    def get_group_members(self, group_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT u.id, u.name
            FROM group_members gm
            JOIN users u ON gm.user_id = u.id
            WHERE gm.group_id = ?
        """, (group_id,))
        return c.fetchall()
    
    def get_groups(self):
        c = self.conn.cursor()
        c.execute("SELECT id, name FROM groups")
        return c.fetchall()
    
    # Apartment management functions
    def initialize_rooms(self, num_rooms):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM rooms")
        count = c.fetchone()[0]
        if count < num_rooms:
            for i in range(count + 1, num_rooms + 1):
                room_number = str(i)
                c.execute("INSERT OR IGNORE INTO rooms (room_number) VALUES (?)", (room_number,))
            self.conn.commit()
    
    def assign_tenant_to_room_by_name(self, room_number, tenant_name):
        c = self.conn.cursor()
        c.execute("SELECT id FROM users WHERE name = ? AND role = 'tenant'", (tenant_name,))
        row = c.fetchone()
        if row:
            tenant_id = row[0]
            c.execute("UPDATE rooms SET tenant_id = ? WHERE room_number = ?", (tenant_id, room_number))
            self.conn.commit()
            return True
        return False
    
    def get_rooms(self):
        c = self.conn.cursor()
        c.execute("SELECT room_number, tenant_id FROM rooms ORDER BY CAST(room_number AS INTEGER)")
        return c.fetchall()
