import miru


class UrlButton(miru.Button):
    def __init__(self, label: str, url: str):
        super().__init__(label=label, url=url)

    async def callback(self, ctx: miru.ViewContext) -> None:
        pass
