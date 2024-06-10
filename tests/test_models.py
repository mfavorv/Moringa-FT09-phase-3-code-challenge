import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_articles(self):
        author = Author(1, "John Doe")
        author_articles = author.articles()
        self.assertIsInstance(author_articles, list) 

    def test_magazine_articles(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        magazine_articles = magazine.articles()
        self.assertIsInstance(magazine_articles, list)

    def test_magazine_article_titles(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        article_titles = magazine.article_titles()
        self.assertIsInstance(article_titles, list)

    def test_magazine_contributing_authors(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        contributing_authors = magazine.contributing_authors()
        if contributing_authors is not None:
           for author in contributing_authors:
            self.assertIsInstance(author, Author)

if __name__ == "__main__":
    unittest.main()