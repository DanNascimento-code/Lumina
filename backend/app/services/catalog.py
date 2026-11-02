from decimal import Decimal

from backend.app.schemas.commerce import ProductOut

PRODUCTS: tuple[ProductOut, ...] = (
    ProductOut(
        id="aurora-headphones",
        slug="aurora-headphones",
        name="Aurora Headphones",
        short_description="Intelligent silence. Sound that surrounds you.",
        description="Premium headphones with adaptive noise cancellation, spatial audio and 42 hours of battery life.",
        category="Audio",
        price=Decimal("1299.90"),
        old_price=Decimal("1499.90"),
        rating=4.9,
        review_count=328,
        stock=18,
        image_url="/assets/products/aurora-headphones.jpg",
        accent="#f68b70",
        badges=["bestSeller", "-13%"],
        specs={"Battery": "42h", "Connection": "Bluetooth 5.3", "Weight": "268g"},
    ),
    ProductOut(
        id="nimbus-speaker",
        slug="nimbus-speaker",
        name="Nimbus Speaker",
        short_description="Room-filling 360° sound, wherever you go.",
        description="Water-resistant portable speaker with spatial sound and stereo pairing.",
        category="Audio",
        price=Decimal("749.90"),
        rating=4.8,
        review_count=196,
        stock=32,
        image_url="/assets/products/nimbus-speaker.jpg",
        accent="#ad8cff",
        badges=["freeShipping"],
        specs={"Battery": "18h", "Protection": "IP67", "Power": "40W"},
    ),
    ProductOut(
        id="orbit-watch",
        slug="orbit-watch",
        name="Orbit Watch S2",
        short_description="Your rhythm, translated into clarity.",
        description="Titanium smartwatch with dual-band GPS, wellness insights and an AMOLED display.",
        category="Wearables",
        price=Decimal("1599.90"),
        old_price=Decimal("1799.90"),
        rating=4.9,
        review_count=241,
        stock=14,
        image_url="/assets/products/orbit-watch.jpg",
        accent="#83d9c8",
        badges=["new", "-11%"],
        specs={"Battery": "7 days", "Display": "1.43-inch AMOLED", "Protection": "5 ATM"},
    ),
    ProductOut(
        id="halo-lamp",
        slug="halo-lamp",
        name="Halo Light Mini",
        short_description="The right light for every moment.",
        description="Portable smart lamp with 16 million colors and routine-based automations.",
        category="Smart home",
        price=Decimal("389.90"),
        rating=4.7,
        review_count=154,
        stock=46,
        image_url="/assets/products/halo-lamp.jpg",
        accent="#ffd082",
        badges=["smartHome"],
        specs={"Battery": "10h", "Connection": "Wi-Fi + Matter", "Output": "350 lm"},
    ),
    ProductOut(
        id="flow-keyboard",
        slug="flow-keyboard",
        name="Flow Keys Pro",
        short_description="Tactile precision, minimal presence.",
        description="Wireless low-profile mechanical keyboard, hot-swappable and built for three devices.",
        category="Workspace",
        price=Decimal("899.90"),
        rating=4.8,
        review_count=112,
        stock=21,
        image_url="/assets/products/flow-keyboard.jpg",
        accent="#7ea8ff",
        badges=["teamPick"],
        specs={"Battery": "120h", "Switch": "Lumina Linear", "Layout": "ABNT2"},
    ),
    ProductOut(
        id="arc-charger",
        slug="arc-charger",
        name="Arc Charger 3-in-1",
        short_description="One base. Three devices. Zero clutter.",
        description="Foldable magnetic station for phone, watch and earbuds with charging up to 15W.",
        category="Accessories",
        price=Decimal("499.90"),
        old_price=Decimal("579.90"),
        rating=4.7,
        review_count=89,
        stock=37,
        image_url="/assets/products/arc-charger.jpg",
        accent="#ff9db4",
        badges=["-14%"],
        specs={"Power": "15W", "Devices": "3 at once", "Cable": "1.5m USB-C"},
    ),
)


def list_products(category: str | None = None, search: str | None = None) -> list[ProductOut]:
    items = list(PRODUCTS)
    if category and category.lower() != "all":
        items = [item for item in items if item.category.lower() == category.lower()]
    if search:
        needle = search.casefold()
        items = [
            item
            for item in items
            if needle in f"{item.name} {item.short_description} {item.category}".casefold()
        ]
    return items


def get_product(product_id: str) -> ProductOut | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)
