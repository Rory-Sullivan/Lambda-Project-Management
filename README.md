# Lambda

Lambda is a project management web application built with Python and Django.
Check out a live version [here](https://rorysullivan.pythonanywhere.com/).

## Framework

There are three main types of objects in Lambda; teams, projects and tasks.
Projects are assigned to a team and tasks are assigned to a project.

### Teams

Teams are made up of members (users of the system), and every team has a leader.
Team leaders have special privileges like being able to assign tasks to other
team members and editing the members of the team.

### Projects

Every project is assigned to a team and thus has members and a leader associated
with it. A project can only be assigned to one team but a team can have many
projects.

### Tasks

Tasks are assigned to projects. Once a task has been assigned to a project it
can be assigned to a member of the project's team, it will then appear on a list
of their active tasks. Tasks can be assigned by team members to themselves or by
the team leader to anyone in the team. Any member of a project's team can create
a task for the project. Tasks can be marked as completed when they are done,
this is generally done by the user the task is assigned to but may also be done
by the team leader.
