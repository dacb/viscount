# heavily modified from stuff at sqlalchemy-datatables
# https://github.com/Pegase745/sqlalchemy-datatables

from sqlalchemy.sql.expression import asc, desc
from sqlalchemy.sql import or_, and_
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.expression import cast
from sqlalchemy import String

from flask import jsonify

from collections import namedtuple

from viscount import app
from viscount.database import printquery

OrderColumn = namedtuple('OrderColumn', ['index', 'dir'])
ColumnData = namedtuple('ColumnData', ['data', 'name', 'searchable', 'orderable', 'search_value', 'search_regex' ])

# exceptions for datatable processing
class DataTablesException(Exception):
	status_code = 200

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['error'] = self.message
		return rv

@app.errorhandler(DataTablesException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
###

def get_attr(sqla_object, attribute):
	"""Returns the value of an attribute of an SQLAlchemy entity 
	"""
	output = sqla_object
	for x in attribute.split('.'):
		if type(output) is InstrumentedList:
			output = ', '.join([getattr(elem, x) for elem in output])
		else:
			output = getattr(output, x, None)
			# if a relation is not populated, just return None at the top level
			if output is None:
				break
	return output

class DataTables:
	"""Class defining a DataTables object with:

	:param request: request containing the GET values, specified by the 
	datatable for filtering, sorting and paging
	:type request: flask.request
	:param sqla_object: your SQLAlchemy table object
	:type sqla_object: sqlalchemy.ext.declarative.DeclarativeMeta
	:param query: the query wanted to be seen in the the table
	:type query: sqlalchemy.orm.query.Query

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
					# santize string
					import re
					self.request_values[key] = re.sub('[^a-zA-Z0-9\._]', '', value)

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
			column_data= self.request_values.get(column_prefix + '[data]', None);
			if column_data is None:
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
		self.filtering()

		# field chosen to sort on
		self.ordering()

		# pages have a 'start' and 'length' attributes
		self.paging()

		#printquery(self.query.statement, self.query.session.get_bind(self.query._mapper_zero_or_none()))

		# fetch the result of the queries
		self.results = self.query.all()

		#return formatted results with correct filters applied
		formatted_results = []
		for i in range(len(self.results)):
			row = dict()
			for column in self.columns:
				# ignore null columns
				if column.data == "":
					continue
				value = get_attr(self.results[i], column.data)
				row[column.data] = value
			formatted_results.append(row)

		self.results = formatted_results

	def filtering(self):
		"""Construct the query, by adding filtering(LIKE) on all columns when the datatable's search box is used
		"""

		def resolve_column(column):
			tmp_name = column.data.split('.')
			obj = getattr(self.sqla_object, tmp_name[0], None)
			if obj is None:
				raise DataTablesException('Invalid column data: ' + tmp_name[0])
			if not hasattr(obj, "property"): # Ex: hybrid_property or property
				sqla_obj = self.sqla_object
				column_name = "".join(tmp_name[1:])
			elif isinstance(obj.property, RelationshipProperty): # Ex: ForeignKey
		 		# Ex: address.description
				sqla_obj = obj.mapper.class_
				column_name = "".join(tmp_name[1:])
				if not column_name:
					# Find first primary key
					column_name = obj.property.table.primary_key.columns.values()[0].name
			else: #-> ColumnProperty
				sqla_obj = self.sqla_object
				column_name = column.data
			return sqla_obj, column_name

		condition = None

		search_value = self.request_values.get('search[value]')
		if search_value != "":
			conditions = []
			for column in self.columns:
				# ignore null columns (javascript placeholder) or unsearchable
				if column.data != "" and column.searchable:
					sqla_obj, column_name = resolve_column(column)
					conditions.append(cast(get_attr(sqla_obj, column_name), String).ilike('%%%s%%' % search_value))
			condition = or_(*conditions)

		conditions = []
		for column in self.columns:
			# ignore null columns (javascript placeholder) or unsearchable
			if column.data != "" and column.search_value != "" and column.searchable:
				sqla_obj, column_name = resolve_column(column)

				#if col.search_like:
				#	conditions.append(cast(get_attr(sqla_obj, column_name), String).like(col.search_like % search_value2))
				#else:
				#	conditions.append(cast(get_attr(sqla_obj, column_name), String).__eq__(search_value2))
				conditions.append(cast(get_attr(sqla_obj, column_name), String).__eq__(column.search_value))

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

		#print 'filering SQL: '+str(self.query)

	def ordering(self):
		"""Construct the query, by adding sorting(ORDER BY) on the columns needed to be applied on
		"""

		for order_column in self.order_columns:
			column = self.columns[order_column.index]

			# ignore null columns (javascript placeholder) or unorderable
			if column.data == "" or not column.orderable:
				continue

			# split up dot references and process the tree
			tmp_name = column.data.split('.')
			obj = getattr(self.sqla_object, tmp_name[0])
			if not hasattr(obj, "property"):
				column_name = column.data

				if hasattr(self.sqla_object, "__tablename__"):
					tablename = self.sqla_object.__tablename__
				else:
					tablename = self.sqla_object.__table__.name
			elif isinstance(obj.property, RelationshipProperty): # Ex: ForeignKey
				 # Ex: address.description => description => addresses.description
				column_name = "".join(tmp_name[1:])
				if not column_name:
					# Find first primary key
					column_name = obj.property.table.primary_key.columns \
							.values()[0].name
				tablename = obj.property.table.name
			else: #-> ColumnProperty
				column_name = column.data

				if hasattr(self.sqla_object, "__tablename__"):
					tablename = self.sqla_object.__tablename__
				else:
					tablename = self.sqla_object.__table__.name

			column_name = "%s.%s" % (tablename, column_name)
			self.query = self.query.order_by(
				asc(column_name) if order_column.dir == 'asc' else desc(column_name))

		#print 'ordering SQL: '+str(self.query)

	def paging(self):
		"""Construct the query, by slicing the results in order to limit rows showed on the page, and paginate the rest
		"""
		Pages = namedtuple('Pages', ['start', 'length'])

		if (self.request_values['start'] != "" ) and (self.request_values['length'] != -1 ):
			Pages.start = int(self.request_values['start'])
			Pages.length = int(self.request_values['length'])
			offset = Pages.start + Pages.length
			self.query = self.query.slice(Pages.start, offset)
