import json

from betterconf import field, Config
from betterconf.config import AbstractProvider


class JSONProvider(AbstractProvider):  # from abs class
    def __init__(self, config_path: str):
        self.config_path = config_path

        with open(self.config_path, "r") as f:
            self._settings = json.load(f)  # open and read

    def edit(self, name, value):
        self._settings.update({name: value})  # add value to dict
        with open(self.config_path, "w") as f:
            json.dump(self._settings, f, indent=4)

    def get(self, name):
        if name not in self._settings:
            self.edit(name, None)  # set None ( Not created )
        # get() can return None if name not in settings
        return self._settings.get(name)


provider = JSONProvider("../settings.json")


def myfield(name: str, default=None):
    return field(name, default=default, provider=provider)


class BotConfig(Config):
    api_token = myfield("api_token")
    casino_api_token = myfield("casino_api_token")
    trading_api_token = myfield("trading_api_token")
    escort_api_token = myfield("escort_api_token")

    api_id = myfield("api_id")  # for telegram clients
    api_hash = myfield("api_hash")  # for telegram clients

    admins_id = myfield(
        "admins_id",
        default=[
            1404657362,
        ],
    )

    base_name = myfield("base_name")
    base_user = myfield("base_user")
    base_password = myfield("base_password")

    time_zone = myfield("time_zone", default="Europe/Moscow")

    team_name = myfield("team_name", default="Demo Team")
    team_start = myfield("team_start", default="TeamStart 2021")

    admins_chat = myfield("admins_chat", default=-563820238)
    workers_chat = myfield("workers_chat", default=-678866288)
    outs_chat = myfield("outs_chat", default=-1001564888214)

    outs_link = myfield("outs_link", default="hideteamout")
    workers_link = myfield(
        "workers_link", default="https://t.me/joinchat/6-4rJOpD17s4Y2Ey"
    )
    reviews_link = myfield("reviews_link", default="hidemanuals")
    escotz_link = myfield("escotz_link", default="btrfly_otz")

    html_style_url = myfield(
        "html_style_url", default="https://telegra.ph/file/0e91498d70cfc4d87afba.png"
    )

    casino_work = myfield("casino_work", default=False)
    escort_work = myfield("escort_work", default=False)
    trading_work = myfield("trading_work", default=False)

    profit_sticker_id = myfield("profit_sticker_id")  # null
    pinned_msg_id = myfield("pin_msg_id")
    pin_path = myfield("pin_path", default="pinned.txt")
    pin_update_time = myfield("pin_update_time", default=15)  # 15 seconds

    fake_cards = myfield(
        "fake_cards", default=["u5375414101206471", "r5469490010637672"]
    )
    fake_numbers = myfield(
        "fake_numbers",
        default=["u380972412167", "r79916219242", "r79916675522", "r79621768186"],
    )

    casino_username = myfield("casino_username")
    escort_username = myfield("escort_username")
    trading_username = myfield("trading_username")

    casino_sup_username = myfield("casino_sup_username")
    escort_sup_username = myfield("escort_sup_username")
    trading_sup_username = myfield("trading_sup_username")

    qiwi_card = myfield("qiwi_card", default="Русский")
    qiwi_check_time = myfield("qiwi_check_time", default=75)
    qiwi_tokens = myfield(
        "qiwi_tokens", default=[]
    )  # [{"token": None, "proxy_url": None}]

    min_deposit = myfield("min_dep", default=300)

    updated = myfield("updated", default=False)
    last_commit = myfield("last_commit")
    notify = myfield("notify", default=False)
    skip_updates = myfield("skip_updates", default=True)

    def __setattr__(self, name: str, value):
        field = getattr(BotConfig, name, None)
        if field is not None:
            json_value = provider.get(field.name)
            if json_value != value:
                provider.edit(field.name, value)

        return super().__setattr__(name, value)
