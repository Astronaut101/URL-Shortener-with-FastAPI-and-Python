# url_shortener/schemas.py

from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str
    
class URL(URLBase):
    """Inherits our target_url field from the URLBase class.

    Args:
        is_active (bool): allows us to deactivate shortened URLS.
        clicks (int): counts how many times a shortened URL has
        been visited.
    """
    is_active: bool
    clicks: int
    
    class Config:
        """By setting the orm_mode = True setting will tell
        pydantic that we are working with a database model."""
        orm_mode = True
        
class URLInfo(URL):
    url: str
    admin_url: str