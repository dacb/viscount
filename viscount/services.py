"""
viscount service instances
"""

from .users import UsersService
from .users import RolesService
from .events import EventsService
from .projects import ProjectsService
from .files import FilesService, FileTypesService
from .workflows import WorkflowsService, WorkflowsTaskInstanceService, WorkflowsTaskInstanceIOService
from .tasks import TasksService, TaskInputFilesService, TaskOutputFilesService
from .jobs import JobsService
from .workers import WorkersService

users = UsersService()
roles = RolesService()
events = EventsService()
projects = ProjectsService()
files = FilesService()
file_types = FileTypesService()
workflows = WorkflowsService()
workflow_task_instances = WorkflowsTaskInstanceService()
workflow_task_instances_io = WorkflowsTaskInstanceIOService()
tasks = TasksService()
task_input_files = TaskInputFilesService()
task_output_files = TaskOutputFilesService()
jobs = JobsService()
workers = WorkersService()
