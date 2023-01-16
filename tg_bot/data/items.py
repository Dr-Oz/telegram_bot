from dataclasses import dataclass

@dataclass
class Item:
    item_id: int
    title: str
    photo_link: str

Pineapple = Item(
    item_id=1,
    title="Pineapple",
    photo_link="https://dostavka.dixy.ru/upload/iblock/fbc/fbc326c8b5a523907953a34b579ad778.jpg"

)

Watermelon = Item(
    item_id=2,
    title="Watermelon",
    photo_link="https://agrosemfond.ru/upload/iblock/a15/3b37a923816311e4b04d441ea16eccfc_8efa8a1e19ba11eb80e20cc47a28e351.resize1.jpg"
)

items = (Pineapple, Watermelon)