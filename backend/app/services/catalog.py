import uuid
from decimal import Decimal

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from backend.app.models.entities import Product
from backend.app.schemas.commerce import ProductOut

CATALOG_NAMESPACE = uuid.UUID("d7b908a7-b990-4d9c-a46d-83b26b5557ce")

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
    ProductOut(
        id="aero-earbuds",
        slug="aero-earbuds",
        name="Aero Buds Pro",
        short_description="Immersive sound that travels light.",
        description=(
            "Compact wireless earbuds with adaptive noise cancellation, multipoint pairing "
            "and a pocket-sized charging case."
        ),
        category="Audio",
        price=Decimal("699.90"),
        old_price=Decimal("799.90"),
        rating=4.8,
        review_count=214,
        stock=41,
        image_url="/assets/products/aero-earbuds.jpg",
        accent="#ffb178",
        badges=["new", "-13%"],
        specs={"Battery": "30h with case", "Protection": "IP54", "Connection": "Bluetooth 5.4"},
    ),
    ProductOut(
        id="vector-mouse",
        slug="vector-mouse",
        name="Vector Mouse S",
        short_description="Precision shaped for long workdays.",
        description=(
            "Ergonomic wireless mouse with a quiet magnetic wheel, programmable controls "
            "and seamless switching between three devices."
        ),
        category="Workspace",
        price=Decimal("429.90"),
        rating=4.8,
        review_count=176,
        stock=29,
        image_url="/assets/products/vector-mouse.jpg",
        accent="#91b9ff",
        badges=["teamPick"],
        specs={"Battery": "90 days", "Sensor": "8000 DPI", "Devices": "3 paired"},
    ),
    ProductOut(
        id="sentinel-camera",
        slug="sentinel-camera",
        name="Sentinel Cam 2K",
        short_description="A clearer view, with privacy built in.",
        description=(
            "Indoor 2K security camera with person detection, a physical privacy shutter "
            "and encrypted local or cloud recording."
        ),
        category="Smart home",
        price=Decimal("549.90"),
        rating=4.7,
        review_count=138,
        stock=34,
        image_url="/assets/products/sentinel-camera.jpg",
        accent="#8ee0cf",
        badges=["smartHome"],
        specs={"Resolution": "2K HDR", "Field of view": "135°", "Connection": "Dual-band Wi-Fi"},
    ),
    ProductOut(
        id="prism-phone",
        slug="prism-phone",
        name="Prism Phone X",
        short_description="Flagship speed without the visual noise.",
        description=(
            "5G smartphone with a 120 Hz OLED display, stabilized dual camera and all-day "
            "battery in a refined aluminum body."
        ),
        category="Mobile",
        price=Decimal("2699.90"),
        old_price=Decimal("2999.90"),
        rating=4.8,
        review_count=302,
        stock=16,
        image_url="/assets/products/prism-phone.jpg",
        accent="#b39cff",
        badges=["new", "-10%"],
        specs={"Storage": "256 GB", "Display": "6.4-inch OLED 120 Hz", "Battery": "4800 mAh"},
    ),
    ProductOut(
        id="slate-tablet",
        slug="slate-tablet",
        name="Slate Tab 11",
        short_description="A flexible canvas for work and play.",
        description=(
            "Thin 11-inch tablet with a 2.5K display, quad speakers, desktop mode and "
            "optional pressure-sensitive pen support."
        ),
        category="Mobile",
        price=Decimal("2199.90"),
        rating=4.7,
        review_count=167,
        stock=23,
        image_url="/assets/products/slate-tablet.jpg",
        accent="#7fd4e7",
        badges=["freeShipping"],
        specs={"Storage": "128 GB", "Display": "11-inch 2.5K", "Battery": "Up to 12h"},
    ),
    ProductOut(
        id="vertex-controller",
        slug="vertex-controller",
        name="Vertex Controller",
        short_description="Console feel across every screen.",
        description=(
            "Low-latency wireless controller with Hall-effect sticks, adjustable triggers "
            "and profiles for PC, mobile and cloud gaming."
        ),
        category="Gaming",
        price=Decimal("459.90"),
        rating=4.9,
        review_count=189,
        stock=38,
        image_url="/assets/products/vertex-controller.jpg",
        accent="#ff9a73",
        badges=["bestSeller"],
        specs={"Battery": "30h", "Compatibility": "PC + Android + iOS", "Connection": "2.4 GHz + Bluetooth"},
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


async def seed_catalog(connection: AsyncConnection) -> None:
    """Keep the PostgreSQL catalog aligned with the versioned storefront fallback."""
    rows = [
        {
            "id": uuid.uuid5(CATALOG_NAMESPACE, product.slug),
            "slug": product.slug,
            "name": product.name,
            "short_description": product.short_description,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "old_price": product.old_price,
            "rating": product.rating,
            "review_count": product.review_count,
            "stock": product.stock,
            "image_url": product.image_url,
            "accent": product.accent,
            "specs": {**product.specs, "badges": product.badges},
        }
        for product in PRODUCTS
    ]
    statement = insert(Product).values(rows)
    update_columns = {
        column: getattr(statement.excluded, column)
        for column in (
            "name",
            "short_description",
            "description",
            "category",
            "price",
            "old_price",
            "rating",
            "review_count",
            "stock",
            "image_url",
            "accent",
            "specs",
        )
    }
    await connection.execute(
        statement.on_conflict_do_update(index_elements=[Product.slug], set_=update_columns)
    )
