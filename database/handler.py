from sqlalchemy import inspect, create_engine, Column, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker


from sqlalchemy.dialects.postgresql.base import PGDialect
PGDialect._get_server_version_info = lambda *_: (24, 2, 0) 



class DatabaseHandler:

	def __init__(self, host, username, password, port):
		self.host = host
		self.username = username
		self.password = password
		self.port = port
		self.database_name = 'instamine'
		
		self.engine = create_engine(
			f"postgresql://{username}:{password}@{host}:{port}/{self.database_name}",
			connect_args={"sslmode": "require"}
		)
		self.metadata = MetaData()

	def connect(self):
		try:
			self.engine = create_engine(
				f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}",
				connect_args={"sslmode": "require"}
			)
			connection = self.engine.connect()
			print(f"Connected to the database '{self.database_name}' successfully.")
			connection.close()
		except SQLAlchemyError as e:
			raise Exception(f"Unable to connect to the database: {e}")

	def is_connected(self):
		try:
			with self.engine.connect() as conn:
				return True
			return False
		except SQLAlchemyError as e:
			print(e)
			return False

	def create_table(self, table_name, columns):
		try:
			columns = [Column(name, dtype) for name, dtype in columns.items()]
			table = Table(table_name, self.metadata, *columns, extend_existing=True)
			self.metadata.create_all(self.engine)
		except SQLAlchemyError as e:
			raise Exception(f"Unable to create table: {e}")

	def drop_table(self, table_name):
		try:
			table = Table(table_name, self.metadata, autoload_with=self.engine)
			table.drop(self.engine)
		except SQLAlchemyError as e:
			raise Exception(f"Unable to drop table: {e}")

	def add_column(self, table_name, column_name, column_type):
		try:
			with self.engine.connect() as conn:
				conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
		except SQLAlchemyError as e:
			raise Exception(f"Unable to add column: {e}")

	def drop_column(self, table_name, column_name):
		try:
			with self.engine.connect() as conn:
				conn.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name}"))
		except SQLAlchemyError as e:
			raise Exception(f"Unable to drop column: {e}")

	def insert_data(self, insert_statement, values):
		try:
			Session = sessionmaker(bind=self.engine)
			session = Session()
			session.execute(insert_statement, values)
			session.commit()
		except SQLAlchemyError as e:
			raise Exception(f"Unable to insert example user: {e}")

	def get_column(self, table_name):
		try:
			inspector = inspect(self.engine)
			columns = inspector.get_columns(table_name)
			return columns
		except SQLAlchemyError as e:
			raise Exception(f"Error retrieving columns: {e}")

	def delete_data(self, to_delete):
		Session = sessionmaker(bind=self.engine)
		session = Session()
		try:
			session.execute(text(f"DELETE FROM {to_delete}"))
			session.commit()
		except SQLAlchemyError as e:
			raise Exception(f"Unable to delete users: {e}")

	def select_data(self, to_select, target="*"):
		try:
			with self.engine.connect() as connection:
				result = connection.execute(text(f"SELECT {target} FROM {to_select}"))
				return result.fetchall()
		except SQLAlchemyError as e:
			raise Exception(f"Unable to select users: {e}")

# db_handler = DatabaseHandler(
# 	host=os.getenv("DB_HOST"),
# 	username=os.getenv("DB_USER"),
# 	password=os.getenv("DB_PASS"),
# 	port=os.getenv("DB_PORT")
# )

# # Drop and create the database, connect, create the table, and insert an example user
# # db_handler.drop_database()
# # db_handler.create_database()
# db_handler.connect()

# db_handler.create_user_table()
# # db_handler.drop_table("User")

# # db_handler.create_user_table()
# # db_handler.delete_data('"User"')

# # db_handler.insert_example_user()
# # db_handler.insert_example_user()
# # db_handler.insert_example_user()
# # db_handler.insert_example_user()
# # db_handler.insert_example_user()
# db_handler.select_data('"User"')
