from sqlalchemy import Column, Integer, String, Table, MetaData

metadata = MetaData()

Table("Users", metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('first_name', String(50)),
	Column('last_name', String(50)),
	Column('username', String(50)),
	Column('email', String(50)),
	Column('age', Integer),
	Column('phone_number', Integer),
	Column('country', Integer)
)
