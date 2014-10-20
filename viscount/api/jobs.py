"""
viscount.api.jobs

Job related endpoints
"""

from flask import Blueprint, request

from ..forms import NewJobForm, UpdateJobForm
from ..services import jobs as _jobs
from . import ViscountFormException, route

bp = Blueprint('jobs', __name__, url_prefix='/jobs')


@route(bp, '/')
def list():
	"""Returns a list of job instances."""
	return _jobs.all()


@route(bp, '/<job_id>')
def show(job_id):
	"""Returns a job instance."""
	return _jobs.get_or_404(job_id)

@route(bp, '/<job_id>', methods=['PUT'])
def update(job_id):
	"""Updates a job. Returns the updated job instance."""
	form = UpdateJobForm()
	if form.validate_on_submit():
		return _jobs.update(jobs.get_or_404(job_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<job_id>', methods=['DELETE'])
def delete(job_id):
	"""Deletes a job. Returns a 204 response."""
	_jobs.delete(jobs.get_or_404(job_id))
	return None, 204

