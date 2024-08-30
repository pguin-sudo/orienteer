from orienteer.general.data.products.products import shop, boosty
from orienteer.general.data.products.products.abstract import AbstractProduct


def get_product(id_: int) -> AbstractProduct | None:
    for product in get_all_products():
        if product.id == id_:
            return product
    return None


def get_all_products() -> tuple[AbstractProduct]:
    return (shop.ColoredNick, shop.GigachatAccess,  # noqa
            shop.PriorityQueue, shop.Orientalink, shop.BanAnnulment, shop.SevenNewSlots, shop.SevenOrientiks,)


boosty_levels: dict[str, tuple[AbstractProduct]] = {  # noqa
    'Космический курсант': (boosty.BoostyRole, boosty.Orientiks10, shop.ColoredNick, shop.GigachatAccess),
    'Капитан': (boosty.Orientiks10, shop.ColoredNick, shop.GigachatAccess, shop.Orientalink, boosty.Whitelist),
    'Адмирал': (boosty.Orientiks10, shop.ColoredNick, shop.GigachatAccess, shop.Orientalink, boosty.Whitelist,
                shop.SevenNewSlots, shop.PriorityQueue, boosty.AllRoles),
    'Директор': (boosty.Orientiks10, shop.ColoredNick, shop.GigachatAccess, shop.Orientalink, boosty.Whitelist,
                 boosty.AllRoles, boosty.NewItems)}
