from django.core.management.base import BaseCommand
from django.db import transaction
import os
import random
from decimal import Decimal
from rooms.models import Room, Amenity, RoomImage
from django.core.files.base import ContentFile
from PIL import Image as PILImage
from io import BytesIO
class Command(BaseCommand):
    help = 'Populates the database with demo hotel room data.'
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population for rooms...'))
        room_types = ['Single', 'Double', 'Deluxe', 'Suite']
        room_type_prices = {
            'Single': (3000, 6000),
            'Double': (6000, 9000),
            'Deluxe': (9000, 14000),
            'Suite': (14000, 20000),
        }
        common_amenities = [
            'WiFi', 'AC', 'TV', 'Room Service', 'Balcony', 'Breakfast',
            'Mini Bar', 'Ocean View', 'City View', 'Private Bathroom'
        ]
        room_descriptions = {
            'Single': "Cozy single room perfect for solo travelers, offering comfort and all essential amenities for a pleasant stay.",
            'Double': "Spacious double room designed for couples, featuring a comfortable bed and a serene ambiance.",
            'Deluxe': "Elegant deluxe room with premium furnishings and extra space, ideal for a luxurious experience.",
            'Suite': "Luxurious suite offering expansive living areas, a separate bedroom, and breathtaking views.",
        }
        self.stdout.write('Ensuring amenities exist...')
        amenities_objects = {}
        for amenity_name in common_amenities:
            amenity, created = Amenity.objects.get_or_create(name=amenity_name)
            amenities_objects[amenity_name] = amenity
            if created:
                self.stdout.write(f'Created amenity: {amenity_name}')
        num_rooms_to_create = 40
        rooms_per_type = num_rooms_to_create // len(room_types)
        room_counter = 1
        created_room_count = 0
        image_dir = 'media/rooms/'
        gallery_image_dir = 'media/rooms/gallery/'
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(gallery_image_dir, exist_ok=True)
        existing_room_images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        existing_gallery_images = [f for f in os.listdir(gallery_image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        with transaction.atomic():
            for room_type in room_types:
                price_min, price_max = room_type_prices[room_type]
                description = room_descriptions[room_type]
                for i in range(rooms_per_type):
                    room_number = f"{room_type[0].upper()}{room_counter:03d}"
                    room_name = f"{room_type} Room {room_counter}"
                    if Room.objects.filter(room_number=room_number).exists():
                        self.stdout.write(self.style.NOTICE(f'Room {room_number} already exists. Skipping.'))
                        room_counter += 1
                        continue
                    price = Decimal(random.uniform(price_min, price_max)).quantize(Decimal('0.01'))
                    max_guests = random.randint(1, 4) if room_type != 'Single' else 1
                    room = Room.objects.create(
                        room_number=room_number,
                        room_name=room_name,
                        room_type=room_type,
                        price_per_night=price,
                        description=description,
                        max_guests=max_guests,
                    )
                    selected_amenities = random.sample(common_amenities, random.randint(3, len(common_amenities)))
                    for amenity_name in selected_amenities:
                        room.amenities.add(amenities_objects[amenity_name])
                    if existing_room_images:
                        main_image_name = random.choice(existing_room_images)
                        main_image_path = os.path.join(image_dir, main_image_name)
                        with open(main_image_path, 'rb') as f:
                            room.image.save(main_image_name, ContentFile(f.read()), save=True)
                        self.stdout.write(f'Attached existing main image {main_image_name} to room {room.room_name}')
                    else:
                        placeholder_image = PILImage.new('RGB', (800, 600), color = (73, 109, 137))
                        d = PILImage.ImageDraw.Draw(placeholder_image)
                        d.text((10,10), f"Room {room_number} - No Image", fill=(255,255,0))
                        buffer = BytesIO()
                        placeholder_image.save(buffer, format="PNG")
                        file_name = f"placeholder_room_{room_number}.png"
                        room.image.save(file_name, ContentFile(buffer.getvalue()), save=True)
                        self.stdout.write(self.style.WARNING(f'Generated placeholder main image for room {room.room_name}'))
                    num_gallery_images = random.randint(1, 2)
                    if existing_gallery_images:
                        selected_gallery_images = random.sample(existing_gallery_images, min(num_gallery_images, len(existing_gallery_images)))
                        for img_name in selected_gallery_images:
                            img_path = os.path.join(gallery_image_dir, img_name)
                            with open(img_path, 'rb') as f:
                                RoomImage.objects.create(room=room, image=ContentFile(f.read(), name=img_name))
                            self.stdout.write(f'Attached existing gallery image {img_name} to room {room.room_name}')
                    else:
                        for j in range(num_gallery_images):
                            placeholder_image = PILImage.new('RGB', (800, 600), color = (100, 150, 180))
                            d = PILImage.ImageDraw.Draw(placeholder_image)
                            d.text((10,10), f"Room {room_number} Gallery {j+1}", fill=(255,255,255))
                            buffer = BytesIO()
                            placeholder_image.save(buffer, format="PNG")
                            file_name = f"placeholder_gallery_{room_number}_{j+1}.png"
                            RoomImage.objects.create(room=room, image=ContentFile(buffer.getvalue(), name=file_name))
                            self.stdout.write(self.style.WARNING(f'Generated placeholder gallery image {j+1} for room {room.room_name}'))
                    self.stdout.write(f'Created room: {room_name} ({room_number})')
                    created_room_count += 1
                    room_counter += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {created_room_count} rooms.'))
