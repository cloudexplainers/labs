# Off camera: the job board's data (made up), and two users: Ben (the owner, a superuser) and Ana (crew).
import os
from django.contrib.auth.models import User
from jobs.models import Job, Task

User.objects.create_superuser("ben", "ben@renovations.example", os.environ["BEN_PW"])
ana = User.objects.create_user("ana", "ana@renovations.example", os.environ["ANA_PW"])
JOBS = [
    ("3 Birch Lane", "Ortiz", [("Kitchen", "Tile the backsplash"), ("Kitchen", "Fit the sink"), ("Hall", "Paint the ceiling")]),
    ("12 Elm Street", "Walsh", [("Bathroom", "Grout <b>all</b> tiles"), ("Bathroom", "Seal the shower"), ("Bedroom", "Sand the floor")]),
    ("27 Oak Avenue", "Patel", [("Living room", "Patch the plaster"), ("Living room", "Paint two walls")]),
    ("5 Mill Road", "Nguyen", [("Kitchen", "Hang the cabinets"), ("Porch", "Replace two boards"), ("Porch", "Stain the rail")]),
    ("40 Pine Court", "Brooks", [("Attic", "Lay insulation"), ("Attic", "Fit a loft ladder")]),
    ("9 River View", "Kowalski", [("Bathroom", "Fit the vanity"), ("Hall", "Hang the new door")]),
    ("18 Station Road", "Adams", [("Bedroom", "Paint the trim"), ("Bedroom", "Fit wardrobe doors"), ("Kitchen", "Fix the leak")]),
    ("61 Hill Street", "Silva", [("Garage", "Fit shelving"), ("Garage", "Paint the floor")]),
]
DONE = [("3 Birch Lane", "Hall", "Strip the wallpaper"), ("12 Elm Street", "Bathroom", "Remove the old tub"),
        ("5 Mill Road", "Kitchen", "Rewire the lights"), ("27 Oak Avenue", "Living room", "Move the furniture"),
        ("40 Pine Court", "Attic", "Clear the boxes"), ("61 Hill Street", "Garage", "Empty the garage")]
for address, client, tasks in JOBS:
    job = Job.objects.create(address=address, client=client)
    for room, title in tasks:
        Task.objects.create(job=job, room=room, title=title)
for address, room, title in DONE:
    Task.objects.create(job=Job.objects.get(address=address), room=room, title=title, done=True)
for title in ["Tile the backsplash", "Seal the shower", "Hang the new door"]:
    Task.objects.filter(title=title).update(assigned_to=ana)
print(Task.objects.filter(done=False).count(), "open tasks,", Job.objects.count(), "jobs")
