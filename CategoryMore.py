from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database_set_FinalProject import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///CategoryUsers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Category 1 - and its items
Category1 = Category(name="Soccer")
session.add(Category1)
session.commit()


CategoryItem4 = CategoryItem(name="Jersey", category=Category1)
session.add(CategoryItem4)
session.commit()

CategoryItem5 = CategoryItem(name="Shorts", category=Category1)
session.add(CategoryItem5)
session.commit()



Category2 = Category(name="BaseBall")
session.add(Category1)
session.commit()


CategoryItem4 = CategoryItem(name="Bat", category=Category2)
session.add(CategoryItem4)
session.commit()

CategoryItem5 = CategoryItem(name="Shoes", category=Category2)
session.add(CategoryItem5)
session.commit()


Category2 = Category(name="Basketball")
session.add(Category1)
session.commit()


CategoryItem4 = CategoryItem(name="shoes", category=Category2)
session.add(CategoryItem4)
session.commit()

CategoryItem5 = CategoryItem(name="Ball", category=Category2)
session.add(CategoryItem5)
session.commit()

#
#
# # Category 2 - and its items
# Category2 = Category(name="BasketBall")
#
# session.add(Category2)
# session.commit()
#
# CategoryItem2 = CategoryItem(name="BasketBall", category=Category2)
#
# session.add(CategoryItem2)
# session.commit()
#
#
# CategoryItem3 = CategoryItem(name="Jersye", category=Category2)
#
# session.add(CategoryItem3)
# session.commit()
#
#
# # Category 3 - and its items
# Category3 = Category(name="BasketBall")
#
# session.add(Category3)
# session.commit()
#
# CategoryItem2 = CategoryItem(name="BaseBall", category=Category3)
#
# session.add(CategoryItem3)
# session.commit()
#
#
# CategoryItem3 = CategoryItem(name="Bat", category=Category3)
#
# session.add(CategoryItem3)
# session.commit()
#
#
#
# # Category 4 - and its items
# Category4 = Category(name="Skating")
#
# session.add(Category4)
# session.commit()
#
# CategoryItem2 = CategoryItem(name="Warm Cloths", category=Category4)
#
# session.add(CategoryItem2)
# session.commit()
#
#
# CategoryItem3 = CategoryItem(name="Skates", category=Category4)
#
# session.add(CategoryItem3)
# session.commit()

print "added menu items!"
