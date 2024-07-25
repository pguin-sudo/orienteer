import asyncio
from orienteer.general.data.orienteer.services.sponsors import get_sponsor_as_dict
from uuid import UUID


mocviu = UUID('ffc80662-6c8d-4c67-a729-658717508eb1')

if __name__ == '__main__':
    print(asyncio.run(get_sponsor_as_dict(mocviu)))
