from .hymnal_lib import HymnalLib
import zipfile as zip
import io
import requests


class HymnalLoader:
    @staticmethod
    async def reload_from_github(i_github_url: str, i_branch: str, i_local_path: str):
        v_github_url = i_github_url.rstrip('/').replace('.git', '')
        v_zip_url = f'{v_github_url}/archive/refs/heads/{i_branch}.zip'

        print(v_zip_url)

        response = requests.get(v_zip_url, stream=True)
        response.raise_for_status()

        print('Pre-extract')

        with zip.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(i_local_path)

        print('Unzipping finished')

