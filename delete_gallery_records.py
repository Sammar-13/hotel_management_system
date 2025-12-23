from rooms.models import RoomImage

print("Deleting all RoomImage records...")
count, deleted_details = RoomImage.objects.all().delete()
print(f"Deleted {count} RoomImage objects.")
print("Details:", deleted_details)
