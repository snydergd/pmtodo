# pmtodo
Django todo list with flexible repeat system for preventative maintenance (PM).

## Features

1.  Extremely flexible repeats based on this: http://george.gdsnyder.info/specifying-complex-date-repeats/ which can represent
    practically any schedule possible in combination with a starting date.
2.  Flexible preventative maintenance tracking using a system of statuses.  You can post a status and have it automatically
    timestamped to keep track of when a task was partially done, any issues with doing it, any comments on the equipment, or
    when a task was finished until next time.

## How to Use

1.  Clone the master branch with: `git clone https://github.com/snydergd/pmtodo.git`
2.  Change into the directory created by the clone with `cd pmtodo`
3.  Install requirements with `python -m pip install -r requirements.txt`
4.  Run the server with `python manage.py runserver`
5.  Go to the address shown by running that command in your web browser (e.g. http://localhost:8000)

## Contributing

If there's a problem small or large with the software, go ahead and create an issue for it, or fork this repository and
send a pull request.  I'll be happy to pull contributions.

## Screenshots

![Task List](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/tasks.png)
![Posting a Status](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/tasks_post.PNG)
![Editing/Viewing a Task](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/edit_task.PNG)
![Schedule List](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/schedule_list.PNG)
![Creating a Schedule](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/schedule_create.PNG)
![Repeat List](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/repeat_list.PNG)
![Modifying a Repeat](https://raw.githubusercontent.com/snydergd/pmtodo/master/doc/repeat_mod.PNG)
