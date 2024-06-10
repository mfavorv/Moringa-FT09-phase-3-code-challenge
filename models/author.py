from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
    
    @property
    def id(self):
        return self._id 
    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("id must be an integer")

    @property
    def name(self):
     if not hasattr(self, '_name'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM authors WHERE id = ?', (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._name = result[0]
            else:
                raise ValueError("Author name not found in database")
     return self._name

    
    @name.setter
    def name(self, name):
      if not hasattr(self,"_name"):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name is not a string or is empty.")
      else:
          raise AttributeError("Name already set.")
        
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor() 
        cursor.execute('''
            SELECT articles.title
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE authors.id = ?          
        ''', (self.id,))

        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results]
    
    def magazines(self):
       conn = get_db_connection()
       cursor = conn.cursor()
       cursor.execute('''
        SELECT DISTINCT magazines.name
        FROM magazines
        INNER JOIN articles ON articles.magazine_id = magazines.id
        WHERE articles.author_id = ?
    ''', (self.id,))
       results = cursor.fetchall()
       conn.close()
       return [row[0] for row in results]
    
    def __repr__(self):
        return f'<Author {self.name}>'