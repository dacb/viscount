"""
viscount service instances
"""

from .users import UsersService
from .users import RolesService
from .events import EventsService
from .projects import ProjectsService
from .files import FilesService
from .workflows import WorkflowsService
from .tasks import TasksService
from .jobs import JobsService
from .workers import WorkersService

users = UsersService()
roles = RolesService()
events = EventsService()
projects = ProjectsService()
files = FilesService()
workflows = WorkflowsService()
tasks = TasksService()
jobs = JobsService()
workers = WorkersService()
