# based on stuff from sqlalchemy-datatables
# https://github.com/Pegase745/sqlalchemy-datatables

from sqlalchemy.sql.expression import asc, desc
from sqlalchemy.sql import or_, and_
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.expression import cast
from sqlalchemy import String

from collections import namedtuple

OrderColumn = namedtuple('OrderColumn', ['index', 'dir'])
ColumnData = namedtuple('ColumnData', ['data', 'name', 'searchable', 'orderable', 'search_value', 'search_regex' ])

class DataTables:
	"""Class defining a DataTables object with:

	:param request: request containing the GET values, specified by the 
	datatable for filtering, sorting and paging
	:type request: flask.request
	:param sqla_object: your SQLAlchemy table object
	:type sqla_object: sqlalchemy.ext.declarative.DeclarativeMeta
	:param query: the query wanted to be seen in the the table
	:type query: sqlalchemy.orm.query.Query
	:param columns: columns specification for the datatables
	:type columns: list

	:returns: a DataTables object
	"""
	def __init__(self, request, sqla_object, query):
		"""Initializes the object with the attributes needed, and runs the query
		"""
		self.request_values = { }
		for key in request.form.keys():
			value = request.form.get(key)
			#print key+' = '+value
			# cast to int to limit security issues
			try:
				self.request_values[key] = int(value)
			except ValueError:
				if value in ("true", "false"):
					self.request_values[key] = value == "true"
				else:
					self.request_values[key] = value

		# process column data from request values
		self.order_columns = []
		i = 0
		while True:
			order_prefix = 'order[%d]' % i
			column_index = self.request_values.get(order_prefix + '[column]', None)
			if column_index is None:
				break;
			self.order_columns.append(OrderColumn(column_index, self.request_values.get(order_prefix + '[dir]', 'asc')))
			i += 1

		self.columns = []
		i = 0
		while True:
			column_prefix = 'columns[%d]' % i
			print column_prefix
			column_data= self.request_values.get(column_prefix + '[data]', None);
			if column_data is None:
				print 'no data'
				break;
			column_name = self.request_values.get(column_prefix + '[name]', None);
			column_searchable = self.request_values.get(column_prefix + '[searchable]', None);
			column_orderable = self.request_values.get(column_prefix + '[orderable]', None);
			self.columns.append(ColumnData(column_data, 
				self.request_values.get(column_prefix + '[name]', None),
				self.request_values.get(column_prefix + '[searchable]', None),
				self.request_values.get(column_prefix + '[orderable]', None),
				self.request_values.get(column_prefix + '[search][value]', None),
				self.request_values.get(column_prefix + '[search][regex]', None)
			))
			i += 1
	
		assert len(self.order_columns) <= len(self.columns)
		assert len(self.columns) > 0
				
		self.sqla_object = sqla_object
		self.query = query
		self.results = None

		# total in the table after filtering
		self.cardinality_filtered = 0

		# total in the table unfiltered
		self.cardinality = 0

		self.run()

	def output_result(self):
		"""Outputs the results in the format needed by DataTables
		"""
		output = {}
		output['draw'] = str(int(self.request_values['draw']))
		output['recordsTotal'] = str(self.cardinality)
		output['recordsFiltered'] = str(self.cardinality_filtered)
		output['data'] = self.results

		return output

	def run(self):
		"""Launch filtering, sorting and paging processes to output results
		"""
		# count before filtering
		self.cardinality = self.query.count()
		
		# the term entered in the datatable's search box
		#self.filtering()

		# field chosen to sort on
		self.ordering()

		# pages have a 'start' and 'length' attributes
		self.paging()

		# fetch the result of the queries
		self.results = self.query.all()

		#return formatted results with correct filters applied
		formatted_results = []
		for i in range(len(self.results)):
			row = dict()
			for j in range(len(self.columns)):
				col = self.columns[j]
				tmp_row = get_attr(self.results[i], col.column_name)
				if col.filter:
					if isinstance(tmp_row, unicode):
						tmp_row = col.filter(tmp_row.encode('utf-8'))
					else:
						tmp_row = col.filter(tmp_row)
				row[col.mData if col.mData else str(j)] = tmp_row
			formatted_results.append(row)

		self.results = formatted_results

	def filtering(self):
		"""Construct the query, by adding filtering(LIKE) on all columns when the datatable's search box is used
		"""
		search_value = self.request_values.get('search[value]')
		condition = None
		def search(idx, col):
			tmp_column_name = col.column_name.split('.')
			obj = getattr(self.sqla_object, tmp_column_name[0])
			if not hasattr(obj, "property"): # Ex: hybrid_property or property
				sqla_obj = self.sqla_object
				column_name = col.column_name
			elif isinstance(obj.property, RelationshipProperty): #Ex: ForeignKey
				# Ex: address.description
				sqla_obj = obj.mapper.class_
				column_name = "".join(tmp_column_name[1:])
				if not column_name:
					# find first primary key
					column_name = obj.property.table.primary_key.columns \
						.values()[0].name
			else:
				sqla_obj = self.sqla_object
				column_name = col.column_name
			return sqla_obj, column_name

		if search_value:
			conditions = []
			for idx, col in enumerate(self.columns):
				if self.request_values.get('columns[%s][searchable]' % idx) in (
						True, 'true'):
					sqla_obj, column_name = search(idx, col)
					conditions.append(cast(get_attr(sqla_obj, column_name), String).ilike('%%%s%%' % search_value))
			condition = or_(*conditions)
		conditions = []
		for idx, col in enumerate(self.columns):
			if self.request_values.get('columns[%s][search][value]' % idx) in (True, 'true'):
				search_value2 = self.request_values.get('columns[%s][search][value]' % idx)
				sqla_obj, column_name = search(idx, col)

				if col.search_like:
					conditions.append(cast(get_attr(sqla_obj, column_name), String).like(col.search_like % search_value2))
				else:
					conditions.append(cast(get_attr(sqla_obj, column_name), String).__eq__(search_value2))

				if condition is not None:
					condition = and_(condition, and_(*conditions))
				else:
					condition= and_(*conditions)


		if condition is not None:
			self.query = self.query.filter(condition)
			# count after filtering
			self.cardinality_filtered = self.query.count()
		else:
			self.cardinality_filtered = self.cardinality

	def ordering(self):
		"""Construct the query, by adding sorting(ORDER BY) on the columns needed to be applied on
		"""

		ordering = []
		Order = namedtuple('Order', ['name', 'dir'])
		for order_column in self.order_columns:
			print order_column.index
			print order_column.dir
			print len(self.columns)
			ordering.append(Order(self.columns[order_column.index].data, order_column.dir))

		for order in ordering:
			tmp_name = order.name.split('.')
			obj = getattr(self.sqla_object, tmp_name[0])
			if not hasattr(obj, "property"):
				order_name = order.name

				if hasattr(self.sqla_object, "__tablename__"):
					tablename = self.sqla_object.__tablename__
				else:
					tablename = self.sqla_object.__table__.name
			elif isinstance(obj.property, RelationshipProperty): # Ex: ForeignKey
				 # Ex: address.description => description => addresses.description
				order_name = "".join(tmp_order_name[1:])
				if not order_name:
					# Find first primary key
					order_name = obj.property.table.primary_key.columns \
							.values()[0].name
				tablename = obj.property.table.name
			else: #-> ColumnProperty
				order_name = order.name

				if hasattr(self.sqla_object, "__tablename__"):
					tablename = self.sqla_object.__tablename__
				else:
					tablename = self.sqla_object.__table__.name

			order_name = "%s.%s" % (tablename, order_name)
			self.query = self.query.order_by(
				asc(order_name) if order.dir == 'asc' else desc(order_name))
			print 'ordering SQL: '+str(self.query)

	def paging(self):
		"""Construct the query, by slicing the results in order to limit rows showed on the page, and paginate the rest
		"""
		Pages = namedtuple('Pages', ['start', 'length'])

		if (self.request_values['start'] != "" ) \
			and (self.request_values['length'] != -1 ):
			Pages.start = int(self.request_values['start'])
			Pages.length = int(self.request_values['length'])
			offset = Pages.start + Pages.length
			self.query = self.query.slice(Pages.start, offset)
