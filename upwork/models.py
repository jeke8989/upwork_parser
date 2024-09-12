from datetime import datetime
from pydantic import BaseModel



class Job(BaseModel):
    id: int
    title: str
    description: str
    link: str
    price: str
    
    def __init__(self, **data) -> None:
        try:
            super().__init__(**data)
        except Exception as e:
            print(f"Error creating Job: {e}")
            raise
        
    def __str__(self) -> str:
        return f'Title = {self.title}, Description = {self.description}, Price = {self.price}\n\nLink = {self.link}'
    
    def to_dict(self): 
        return { 
            'title': self.title, 
            'description': self.description, 
            'price': self.price, 
            'link': self.link 
        } 

class Client(BaseModel):
    location: str
    job_info: str
    job_rate: str
    
    def __init__(self, **data) -> None:
        try:
            super().__init__(**data)
        except Exception as e:
            print(f"Error creating Job: {e}")
            raise
    
    
    def __str__(self) -> str:
        return f'Location = {self.location}, Info = {self.job_info}, Rate = {self.job_rate}'
    
    def to_dict(self): 
        return { 
            'location': self.location, 
            'job_info': self.job_info, 
            'job_rate': self.job_rate,  
        } 
        

class Job_Advance(BaseModel):
    title: str
    description: str
    price: str
    location_freelancer: str
    posted_date: str
    link: str
    client: Client
        
    def to_dict(self): 
        return { 
            'title': self.title, 
            'description': self.description, 
            'price': self.price, 
            'location_freelancer': self.location_freelancer, 
            'posted_date': self.posted_date, 
            'link': self.link, 
            'client': self.client.to_dict() # Вложенный объект сериализуется через его собственный метод to_dict 
        }