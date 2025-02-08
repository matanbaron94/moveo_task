from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from src.local_config import config
from pydantic import BaseModel
import random





####################################################
###################### INIT ########################
####################################################

DATABASE_URL = f"postgresql://{config['DATABASE_USERNAME']}:{config['DATABASE_PASSWORD']}@{config['DATABASE_HOST_NAME']}:{config['DATABASE_PORT']}/{config['DATABASE_NAME']}" 
ENGINE = create_engine(DATABASE_URL)
Base = declarative_base()




####################################################
###################### ITEM ########################
####################################################

class ItemScheme(BaseModel):
    name: str
    description: str 



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)


    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



 

####################################################
################# ITEM CONTROLLER ##################
####################################################

class ItemsController():
    def __init__(self):
        # CREATE DB TABLE
        Base.metadata.create_all(bind=ENGINE)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
        
        self.db = SessionLocal()

        self.db.close()

        # BUILD SOME DATA
        datalist = self.get_all_items()
        if(len(datalist) == 0):
            self.create_item("Classic Cotton T-Shirt","A soft and breathable cotton T-shirt with a timeless fit. Perfect for casual wear or layering under jackets.")
            self.create_item("Premium Denim Jacket","A stylish denim jacket made from high-quality cotton, featuring a classic button-down front and durable stitching.")
            self.create_item("Woolen Beanie Hat","A cozy and warm beanie hat made from soft wool, designed to keep your head comfortable during colder months.")
            self.create_item("Athletic Joggers","Lightweight and flexible joggers with an elastic waistband, perfect for workouts or casual outings.")
            self.create_item("Hooded Sweatshirt","A comfortable pullover hoodie with a large front pocket and adjustable drawstrings for a relaxed fit.")
            self.create_item("Casual Linen Shirt","A breathable linen shirt with a relaxed fit, ideal for warm weather and stylish everyday wear.")

            self.create_item("Classic Baseball Cap","A structured baseball cap with an adjustable strap, available in various colors to match any outfit.")
            self.create_item("Leather Belt","A genuine leather belt with a sturdy metal buckle, designed to add a touch of sophistication to any outfit.")
            self.create_item("Cotton Cargo Shorts","Durable and stylish cargo shorts with multiple pockets, offering both comfort and functionality for outdoor activities.")
            self.create_item("Slim-Fit Chinos","Versatile slim-fit chinos made from stretchable fabric, perfect for both casual and semi-formal occasions")

    def __generate_unique_id__(self):
        """Generates a unique 7-digit integer ID for SQLAlchemy."""
        while True:
            unique_id = random.randint(100, 999)
            existing_entry = self.db.query(Item).filter_by(id=unique_id).first()
            if not existing_entry:
                return unique_id




    def get_all_items(self):
        all_items = self.db.query(Item).all()
        return all_items
 

    def get_item(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    def create_item(self,name,description):
        
        db_item = Item(name=name, description=description, id=self.__generate_unique_id__())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)

        return self.get_item(db_item.id)
    
    
    def delete_item(self, item_id: int):
        item_to_delete = self.db.query(Item).filter(Item.id == item_id).first()
        if not item_to_delete:
            return None

        self.db.delete(item_to_delete)
        self.db.commit()
        return item_to_delete
    

    def update_item(self, item_id: int, item: ItemScheme):
        db_item = self.db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return None  

        db_item.name = item.name
        db_item.description = item.description
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
