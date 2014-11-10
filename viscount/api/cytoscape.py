"""
viscount.api.cytoscape

Workflow rendereding for cytoscape.js json
"""

from flask import jsonify

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


def render_workflow_to_cytoscape(wf, parent=None):
	nodes = []
	edges = []
	for ti in wf.task_instances.all():
		nodes.append( { 'data' : { 'id' : 'ti' + str(ti.id), 'name' : ti.task.name, 'description' : ti.description, 'color' : 'gray' } } )
		for tif in ti.task.inputs.all():
			nodes.append( { 'data' : {
				'id' : 'ti' + str(ti.id) + 'tif' + str(tif.id),
				'parent' : 'ti' + str(ti.id),
				'name' : tif.name,
				'description' : tif.description,
				'file_type' : tif.file_type.name,
				'classes' : 'input',
				'color' : 'cyan'
				} } )
		for tof in ti.task.outputs.all():
			nodes.append( { 'data' : {
				'id' : 'ti' + str(ti.id) + 'tof' + str(tof.id),
				'parent' : 'ti' + str(ti.id),
				'name' : tof.name,
				'description' : tof.description,
				'file_type' : tof.file_type.name,
				'classes' : 'output',
				'color' : 'magenta'
				} } )
		for tii in ti.inputs:
			edges.append( { 'data' : { 'id' : 'tii' + str(tii.id), 'source' : 'ti' + str(tii.output_task_instance.id) + 'tof' + str(tii.output_task_file_id), 'target' : 'ti' + str(ti.id) + 'tif' + str(tii.input_task_file_id), 'color' : 'purple' } } )


	graph = {	'elements' : { 'nodes' : nodes , 'edges' : edges },
				'style' :	[
					{
						'selector' : 'node', 
						'css' : {
							'content' : 'data(name)',
							'text-valign' : 'center',
							'text-halign' : 'center',
							'text-outline-width' : 2,
							'text-outline-color' : 'data(color)',
							'background-color' : 'data(color)',
							'color' : '#fff'
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
							'opacity' : 0.666,
							'target-arrow-shape' : 'triangle',
							'source-arrow-shape' : 'circle',
							'line-color' : 'magenta',
							'source-arrow-color' : 'cyan',
							'target-arrow-color' : 'magenta',
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
