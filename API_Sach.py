import requests
import json
from tkinter import messagebox

class APIBook:
    def __init__(self):
        # Sử dụng Google Books API (miễn phí)
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        
    def tim_kiem_sach(self, keyword, max_results=20):
        """Tìm kiếm sách qua Google Books API"""
        try:
            # Tham số tìm kiếm
            params = {
                'q': keyword,
                'maxResults': max_results,
                'printType': 'books',
                'langRestrict': 'vi'  # Ưu tiên sách tiếng Việt
            }
            
            # Gửi request
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                books = []
                
                if 'items' in data:
                    for item in data['items']:
                        book_info = self.extract_book_info(item)
                        if book_info:
                            books.append(book_info)
                
                return books
            else:
                print(f"Lỗi API: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {e}")
            return []
        except Exception as e:
            print(f"Lỗi: {e}")
            return []
    
    def extract_book_info(self, item):
        """Trích xuất thông tin sách từ API response"""
        try:
            volume_info = item.get('volumeInfo', {})
            
            # Lấy thông tin cơ bản
            title = volume_info.get('title', 'Không có tiêu đề')
            authors = volume_info.get('authors', ['Không rõ tác giả'])
            author = ', '.join(authors) if isinstance(authors, list) else str(authors)
            
            # Thể loại
            categories = volume_info.get('categories', ['Chung'])
            category = categories[0] if categories else 'Chung'
            
            # Thông tin khác
            published_date = volume_info.get('publishedDate', 'Không rõ')
            description = volume_info.get('description', 'Không có mô tả')
            page_count = volume_info.get('pageCount', 0)
            
            # ISBN
            industry_identifiers = volume_info.get('industryIdentifiers', [])
            isbn = ''
            for identifier in industry_identifiers:
                if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                    isbn = identifier.get('identifier', '')
                    break
            
            # Hình ảnh
            image_links = volume_info.get('imageLinks', {})
            thumbnail = image_links.get('thumbnail', '')
            
            return {
                'id': item.get('id', ''),
                'title': title,
                'author': author,
                'category': category,
                'published_date': published_date,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'page_count': page_count,
                'isbn': isbn,
                'thumbnail': thumbnail
            }
            
        except Exception as e:
            print(f"Lỗi trích xuất thông tin: {e}")
            return None

    def get_book_detail(self, book_id):
        """Lấy thông tin chi tiết của một cuốn sách"""
        try:
            url = f"{self.base_url}/{book_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self.extract_book_info(data)
            
        except Exception as e:
            print(f"Lỗi lấy chi tiết sách: {e}")
        
        return None

# API cho Open Library (backup)
class OpenLibraryAPI:
    def __init__(self):
        self.search_url = "https://openlibrary.org/search.json"
        
    def tim_kiem_sach(self, keyword, limit=20):
        """Tìm kiếm sách qua Open Library API"""
        try:
            params = {
                'q': keyword,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,publisher,isbn,cover_i'
            }
            
            response = requests.get(self.search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                books = []
                
                if 'docs' in data:
                    for doc in data['docs']:
                        book_info = {
                            'title': doc.get('title', 'Không có tiêu đề'),
                            'author': ', '.join(doc.get('author_name', ['Không rõ tác giả'])),
                            'category': 'Chung',
                            'published_date': str(doc.get('first_publish_year', 'Không rõ')),
                            'isbn': ', '.join(doc.get('isbn', [''])[:3]) if doc.get('isbn') else '',
                            'publisher': ', '.join(doc.get('publisher', [''])[:2]) if doc.get('publisher') else ''
                        }
                        books.append(book_info)
                
                return books
            
        except Exception as e:
            print(f"Lỗi Open Library API: {e}")
        
        return []