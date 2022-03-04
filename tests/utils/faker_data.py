from faker import Faker

from config.config import settings

faker_data = Faker(locale=settings.FAKER_DATA_LOCATE)
