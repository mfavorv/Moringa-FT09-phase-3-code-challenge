from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       (self._title, self._content, self._author_id, self._magazine_id))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
     
    @property
    def title(self):
        if not hasattr(self, "_title"):
            self.connection = get_db_connection()
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT title FROM articles WHERE id = ?', (self.id,))
            result = self.cursor.fetchone() 

            if result:
                self._title = result[0]
            else:
                raise ValueError("Title not found in database")
        
        return self._title
    
    @title.setter
    def title(self, title):
       if not hasattr(self,"_title"):
        if isinstance(title, str) and (5 <= len(title) <= 50):
            self._title = title
        else:
            raise ValueError("Title is not a string or it does not have 5-50 characters")
       else:
           print("Title already set")
    
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()     
        cursor.execute('''
            SELECT authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.id = ?
        ''', (self.id,))

        result = cursor.fetchone()
        conn.close()
        print(result)
        return result[0] if result else None
        
    
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor() 
        cursor.execute('''
             SELECT magazines.name
             FROM articles
             INNER JOIN magazines ON articles.magazine_id = magazines.id
             WHERE articles.id = ?
      ''', (self.id,))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def __repr__(self):
        return f'<Article {self.title}>'
