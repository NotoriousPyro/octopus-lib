Early version of a client using aiohttp and asyncio for Octopus.energy API

For now this is ***not*** properly packaged as a usable python package.

To install:
1. Install Python 3.10 and `git clone` the repo & `cd` into the folder
2. Run `python -m venv env`
3. Run `.\env\Scripts\activate` (Windows) or `source ./env/bin/activate` (Linux)
4. Run `pip install -r requirements-pip.txt`
5. Run `pip-sync requirements-dev.txt requirements.txt`



You can get started with something as simple as (see `main.py`):

```python
import asyncio
import datetime

from octopus.client import OctopusClient
from octopus.models import ConsumptionRequestArgs, OctopusConfig


async def main():
    client = OctopusClient(config=OctopusConfig.parse_file("config.json"))
    async for data in client.get_meter_consumption_data(args=ConsumptionRequestArgs(
        period_from=datetime.datetime.now() - datetime.timedelta(days=7),
        page_size=200
    )):
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
```
