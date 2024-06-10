from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
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
            raise ValueError("id is not an integer")     

    @property
    def name(self):
        if not hasattr(self, '_name'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM magazines WHERE id = ?', (self.id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                self._name = result[0]
            else:
                raise ValueError("name not found in database")
        
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and (2<= len(name) <= 16):
            self._name = name
        else:
            raise ValueError("name is not a string or does not have 2-16 characters")
        
        
    @property
    def category(self):
        if not hasattr(self, '_category'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT category FROM magazines WHERE id = ?', (self.id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                self._category = result[0]
            else:
                self._category = None
        return self._category
    
    @category.setter
    def category(self, category):
        if isinstance(category, str) and  len(category) > 0 :
            self._category = category
        else:
            raise ValueError("category is not a string or is empty")
        
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.title
            FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE magazines.id = ?
        ''', (self.id,))

        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results]
    
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
                       ''',(self.id))
        
        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results]
    
    def article_titles(self):
       conn = get_db_connection()
       cursor = conn.cursor()
       cursor.execute('''
         SELECT  articles.title
         FROM articles
         WHERE magazine_id  = ?
        ''', (self.id,))
       results = cursor.fetchall()
       conn.close()
       return [row[0] for row in results] if results else None

    def contributing_authors(self):
       conn = get_db_connection()
       cursor = conn.cursor()
       cursor.execute('''
            SELECT authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
           ''', (self.id,))
       results = cursor.fetchall()
       counts = {}
       
       for row in results:
           name = row[0]
           counts[name] = counts.get(name, 0) + 1
           
       authors = {author: count for author, count in counts.items() if count > 2}

       if authors:
           for author in authors:
               if isinstance(author, Author):
                   return authors
               else:
                   raise ValueError("author is not an instance of Author")
       else:
           return None

    def __repr__(self):
        return f'<Magazine {self.name}>'      



