"""
viscount.api.cytoscape

Workflow rendereding for cytoscape.js json
"""

from ..services import workflows as _workflows, tasks as _tasks
from ..models import Workflow
from ..core import db

from ..core import ViscountException


# exceptions for cytoscape rendering
class CytoscapeException(ViscountException):
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


def handle_CytoscapeException(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


def render_workflow_to_cytoscape(obj, parent=None):
	graph = { 'elements' : {
				'nodes' : [
					{ 'data' : { 'id' : 'a', 'parent' : 'b' } },
					{ 'data' : { 'id' : 'b' } },
					{ 'data' : { 'id' : 'c', 'parent' : 'b' } },
					{ 'data' : { 'id' : 'd' } },
					{ 'data' : { 'id' : 'e' } },
					{ 'data' : { 'id' : 'f', 'parent' : 'e' } },
				],
				'edges': [
					{ 'data' : { 'id' : 'ad', 'source' : 'a', 'target' : 'd' } },
					{ 'data' : { 'id' : 'eb', 'source' : 'e', 'target' : 'b' } },
				]
			},
			'style' : [
					{
						'selector' : 'node', 
						'css' : {
							'content' : 'data(id)',
							'text-valign' : 'center',
							'text-halign' : 'center',
						},
					}, {
						'selector' : '$node > node',
						'css' : {
							'padding-top' : '10px',
							'padding-left' : '10px',
							'padding-bottom' : '10px',
							'padding-right' : '10px',
							'text-valign' : 'top',
							'text-halign' : 'center',
						}
					}, {
						'selector' : 'edge',
						'css' : {
							'target-arrow-shape' : 'triange',
						}
					}, {
						'selector' : ':selected',
						'css' : {
							'background-color' : 'black',
							'line-color' : 'black',
							'target-arrow-color' : 'black',
							'source-arrow-color' : 'black',
						}
					}
				],
			'layout' : {
				'name' : 'breadthfirst',
				'padding' : 5
			}
		}
	return graph


def render_to_cytoscape(obj):
	"""renders an object in the ORM to a cytoscape.js json"""
	
	if isinstance(obj, Workflow):
		return render_workflow_to_cytoscape(obj)
	elif isinstance(obj, Project):
		# for workflows, render each workflow with a parent compound node
		raise CytoscapeException('not implemented')
	else:
		raise CytoscapeException('Cytoscape rendering not supported for object type ' + str(type(obj)))
