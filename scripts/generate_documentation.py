# ruff: noqa: E501

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
LOGO_PATH = ROOT / "frontend" / "public" / "assets" / "brand" / "lumina-logo.png"
PRODUCTION_URL = "https://lumina-smart-store.vercel.app"

MIDNIGHT = colors.HexColor("#17152B")
INK = colors.HexColor("#29243F")
VIOLET = colors.HexColor("#7357E8")
LAVENDER = colors.HexColor("#EEE9FF")
CORAL = colors.HexColor("#FF7D67")
PAPER = colors.HexColor("#F8F7F3")
MUTED = colors.HexColor("#706B78")
LINE = colors.HexColor("#DED9D4")
GREEN = colors.HexColor("#258468")
WHITE = colors.white


@dataclass(frozen=True)
class DocMeta:
    title: str
    subtitle: str
    label: str
    version: str = "1.0"


class AccentRule(Flowable):
    def __init__(self, width: float = 42 * mm, thickness: float = 3) -> None:
        super().__init__()
        self.width = width
        self.height = thickness
        self.thickness = thickness

    def draw(self) -> None:
        self.canv.setStrokeColor(CORAL)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


class NumberBadge(Flowable):
    def __init__(self, number: str, label: str, detail: str, width: float = 52 * mm) -> None:
        super().__init__()
        self.number = number
        self.label = label
        self.detail = detail
        self.width = width
        self.height = 28 * mm

    def draw(self) -> None:
        canvas = self.canv
        canvas.setFillColor(LAVENDER)
        canvas.roundRect(0, 0, self.width, self.height, 4 * mm, stroke=0, fill=1)
        canvas.setFillColor(VIOLET)
        canvas.setFont("Helvetica-Bold", 19)
        canvas.drawString(5 * mm, 17 * mm, self.number)
        canvas.setFillColor(MIDNIGHT)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawString(5 * mm, 10.5 * mm, self.label.upper())
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(5 * mm, 5.5 * mm, self.detail)


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=INK,
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=11,
            textColor=MUTED,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=29,
            textColor=MIDNIGHT,
            spaceBefore=2,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=MIDNIGHT,
            spaceBefore=13,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=VIOLET,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "eyebrow": ParagraphStyle(
            "Eyebrow",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=VIOLET,
            tracking=1.5,
            spaceAfter=5,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=16,
            textColor=MIDNIGHT,
            spaceBefore=0,
            spaceAfter=0,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.5,
            textColor=INK,
            leftIndent=5 * mm,
            firstLineIndent=-3 * mm,
            bulletIndent=1 * mm,
            spaceAfter=4,
        ),
        "table": ParagraphStyle(
            "Table",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.6,
            leading=10.5,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.6,
            leading=10,
            textColor=WHITE,
        ),
    }


STYLES = build_styles()


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def bullets(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"- {item}", STYLES["bullet"]) for item in items]


def callout_box(text: str) -> Table:
    box = Table([[p(text, "callout")]], colWidths=[166 * mm], hAlign="LEFT")
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF0EC")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
            ]
        )
    )
    return box


def section(title: str, eyebrow: str | None = None) -> list[Flowable]:
    content: list[Flowable] = [Spacer(1, 3 * mm)]
    if eyebrow:
        content.append(p(eyebrow.upper(), "eyebrow"))
    content.extend([p(title, "h1"), AccentRule(), Spacer(1, 4 * mm)])
    return content


def data_table(headers: list[str], rows: list[list[str]], widths: list[float]) -> Table:
    data = [[p(value, "table_head") for value in headers]]
    data.extend([[p(value, "table") for value in row] for row in rows])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), MIDNIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3.2 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3.2 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PAPER]),
            ]
        )
    )
    return table


def card_grid(cards: list[tuple[str, str]], columns: int = 2) -> Table:
    cells = []
    for title, copy in cards:
        cells.append([p(title, "h3"), p(copy, "small")])
    while len(cells) % columns:
        cells.append(Spacer(1, 1))
    rows = [cells[index : index + columns] for index in range(0, len(cells), columns)]
    table = Table(rows, colWidths=[(172 * mm - (columns - 1) * 5 * mm) / columns] * columns, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 5, PAPER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
            ]
        )
    )
    return table


def draw_header_footer(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(MIDNIGHT)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, fill=1, stroke=0)
    canvas.drawImage(str(LOGO_PATH), 18 * mm, height - 10.7 * mm, 8 * mm, 8 * mm, preserveAspectRatio=True, mask="auto")
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(29 * mm, height - 7.8 * mm, "LUMINA")
    canvas.setFillColor(colors.HexColor("#C9C2DE"))
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(width - 18 * mm, height - 7.8 * mm, doc.title)
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(18 * mm, 9 * mm, f"Lumina Commerce, Inc.  |  {PRODUCTION_URL}")
    canvas.drawRightString(width - 18 * mm, 9 * mm, f"{canvas.getPageNumber():02d}")
    canvas.restoreState()


def draw_cover(canvas, doc, meta: DocMeta) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(MIDNIGHT)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#2B2451"))
    canvas.circle(width - 12 * mm, height - 23 * mm, 45 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#3A2B74"))
    canvas.circle(width - 5 * mm, 38 * mm, 55 * mm, fill=1, stroke=0)
    canvas.setFillColor(CORAL)
    canvas.circle(24 * mm, 34 * mm, 9 * mm, fill=1, stroke=0)
    canvas.drawImage(str(LOGO_PATH), 22 * mm, height - 70 * mm, 38 * mm, 38 * mm, preserveAspectRatio=True, mask="auto")
    canvas.setFillColor(colors.HexColor("#BDAFEF"))
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(22 * mm, height - 86 * mm, meta.label.upper())
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 30)
    text = canvas.beginText(22 * mm, height - 108 * mm)
    text.setLeading(35)
    for line in meta.title.split("\n"):
        text.textLine(line)
    canvas.drawText(text)
    canvas.setFillColor(colors.HexColor("#D6D0E6"))
    canvas.setFont("Helvetica", 12)
    subtitle = canvas.beginText(22 * mm, height - 148 * mm)
    subtitle.setLeading(17)
    for line in meta.subtitle.split("\n"):
        subtitle.textLine(line)
    canvas.drawText(subtitle)
    canvas.setStrokeColor(CORAL)
    canvas.setLineWidth(3)
    canvas.line(22 * mm, height - 162 * mm, 65 * mm, height - 162 * mm)
    canvas.setFillColor(colors.HexColor("#B5AEC9"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(22 * mm, 25 * mm, f"VERSION {meta.version}")
    canvas.drawRightString(width - 22 * mm, 25 * mm, "LUMINA COMMERCE, INC.")
    canvas.restoreState()


def make_doc(path: Path, meta: DocMeta, story: list[Flowable]) -> None:
    doc = BaseDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=21 * mm,
        bottomMargin=19 * mm,
        title=meta.title.replace("\n", " "),
        author="Lumina Commerce, Inc.",
        subject=meta.subtitle.replace("\n", " "),
    )
    width, height = A4
    cover_frame = Frame(0, 0, width, height, id="cover", showBoundary=0)
    body_frame = Frame(19 * mm, 18 * mm, width - 38 * mm, height - 36 * mm, id="body", showBoundary=0)
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=lambda c, d: draw_cover(c, d, meta), autoNextPageTemplate="body"),
            PageTemplate(id="body", frames=[body_frame], onPage=draw_header_footer),
        ]
    )
    doc.build([PageBreak(), *story])
    strip_date_metadata(path)


def strip_date_metadata(path: Path) -> None:
    reader = PdfReader(path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    info = writer._info.get_object()
    info.pop(NameObject("/CreationDate"), None)
    info.pop(NameObject("/ModDate"), None)
    temporary = path.with_suffix(".tmp.pdf")
    with temporary.open("wb") as stream:
        writer.write(stream)
    temporary.replace(path)


def nontechnical_story() -> list[Flowable]:
    story: list[Flowable] = []
    story += section("Welcome to Lumina", "Product and service guide")
    story += [
        p(
            "Lumina is a digital technology store built around a simple promise: help people choose confidently. "
            "The storefront combines a curated catalog, a complete shopping journey and Lumi, a conversational product specialist that explains options in clear language."
        ),
        p(
            "Customers can browse by category, compare products, add items to a cart, complete a guided checkout and receive an order confirmation. "
            "Lumi remains available throughout the experience to answer questions about products, shipping, returns, warranty and payments."
        ),
        callout_box("A better technology purchase is not about showing more options. It is about making the right option easier to understand."),
        Table(
            [[NumberBadge("3", "languages", "English, Portuguese, Spanish"), NumberBadge("6", "curated products", "Across five lifestyle categories"), NumberBadge("24/7", "guided discovery", "Lumi is available throughout the store")]],
            colWidths=[57 * mm] * 3,
            hAlign="LEFT",
            style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]),
        ),
        Spacer(1, 6 * mm),
        p("What customers can do", "h2"),
        card_grid(
            [
                ("Discover", "Explore selected products by category, use case, promotion or a direct search."),
                ("Understand", "Open detailed product views with benefits, pricing, installments, warranty and return information."),
                ("Decide", "Ask Lumi for tailored recommendations, comparisons and transparent trade-offs."),
                ("Purchase", "Use a complete cart and checkout flow with delivery, payment and confirmation stages."),
            ]
        ),
        PageBreak(),
    ]

    story += section("The shopping journey", "From discovery to confirmation")
    story += [
        p("1. Arrive and explore", "h2"),
        p("The home page introduces the current collection, featured categories and community favorites. Product photography and concise copy make the assortment easy to scan."),
        p("2. Narrow the choice", "h2"),
        p("Customers can search by product name, category or description. Category controls highlight audio, wearables, smart home, workspace and accessories."),
        p("3. Ask Lumi", "h2"),
        p("Lumi can translate a need into a recommendation, compare options, explain store policies and propose useful follow-up questions. Answers include consulted source material when applicable."),
        p("4. Build the cart", "h2"),
        p("Items can be added from product cards or detailed views. The cart tracks quantity, subtotal, shipping eligibility and the path to checkout."),
        p("5. Complete checkout", "h2"),
        p("The checkout collects delivery details, presents card and Pix options and shows an order summary. The current release demonstrates the full user experience with simulated payment approval rather than a live payment processor."),
        p("6. Receive confirmation", "h2"),
        p("A successful order receives an order code, delivery estimate, payment status and confirmation message."),
        PageBreak(),
    ]

    story += section("Meet Lumi", "Conversational product guidance")
    story += [
        p("Lumi is designed to feel like a thoughtful in-store specialist: warm, concise and focused on the customer's actual need. The assistant does not simply generate generic sales copy. It searches Lumina's approved knowledge and responds with grounded information."),
        card_grid(
            [
                ("Product matching", "Recommend products for a budget, routine, gift or specific use case."),
                ("Clear comparisons", "Explain meaningful differences such as battery life, portability and intended use."),
                ("Policy support", "Answer questions about shipping, returns, warranty and supported payment methods."),
                ("Guided follow-ups", "Offer the next most useful questions so customers can continue naturally."),
                ("Visible sources", "Show the Lumina source used for a factual answer."),
                ("Safe uncertainty", "Decline to invent facts when approved information is missing."),
            ]
        ),
        Spacer(1, 5 * mm),
        p("Good questions to ask Lumi", "h2"),
        *bullets(
            [
                "I need headphones for travel and calls. What should I choose?",
                "Compare Aurora and Nimbus for battery life and portability.",
                "Can I return an online order after delivery?",
                "Which products work well for a home office under R$1,000?",
                "What is covered by the Lumina warranty?",
            ]
        ),
        PageBreak(),
    ]

    story += section("Service standards", "Trust, privacy and support")
    story += [
        p("Lumina presents policy and product facts from approved company documents. The assistant is instructed not to invent price, inventory, delivery estimates, compatibility or order status."),
        data_table(
            ["Commitment", "What it means for customers"],
            [
                ["Grounded answers", "Lumi uses approved Lumina knowledge and displays supporting sources."],
                ["Privacy by design", "The assistant does not request passwords, authentication tokens or full identity documents."],
                ["Protected checkout", "Payment fields are presented in a secure flow; the current demonstration does not process a real charge."],
                ["Transparent limits", "When evidence is insufficient, Lumi says so and proposes a safer next step."],
                ["Accessible language", "The storefront is English-first and can switch to Brazilian Portuguese or Latin American Spanish."],
            ],
            [45 * mm, 127 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Returns and warranty at a glance", "h2"),
        *bullets(
            [
                "Online purchases can be returned within seven calendar days of delivery, subject to the published return conditions.",
                "Products include a 12-month contractual warranty for manufacturing and material defects under normal use.",
                "Orders above R$499 qualify for free standard shipping in the current store policy.",
                "Exact delivery estimates are shown during checkout after the delivery destination is provided.",
            ]
        ),
        PageBreak(),
    ]

    story += section("Frequently asked questions", "Customer reference")
    faqs = [
        ("Is Lumina available in multiple languages?", "Yes. English is the default, with Brazilian Portuguese and Latin American Spanish available from the header."),
        ("Does Lumi know my cart?", "Lumi receives a limited cart summary so it can make relevant suggestions without needing payment data."),
        ("Are Lumi's answers always generated by AI?", "Production can use an OpenAI language model. If the model is unavailable, Lumina falls back to a controlled local response grounded in the same knowledge base."),
        ("Does the site charge a real card?", "No. The current checkout demonstrates a complete purchase experience but uses a simulated payment confirmation."),
        ("Where can I use Lumina?", f"The production storefront is available at {PRODUCTION_URL}."),
        ("What happens when Lumi does not know?", "It abstains rather than inventing an answer, then suggests a supported topic or a refined question."),
    ]
    for question, answer in faqs:
        story.append(KeepTogether([p(question, "h3"), p(answer)]))
    story += [Spacer(1, 10 * mm), callout_box("Lumina brings the clarity of a specialist into every step of digital commerce.")]
    return story


def technical_story() -> list[Flowable]:
    story: list[Flowable] = []
    story += section("System overview", "Engineering reference")
    story += [
        p(
            "Lumina is a full-stack commerce application built with React, TypeScript, FastAPI, PostgreSQL, pgvector, LangChain and OpenAI. "
            "The same FastAPI deployment serves the compiled storefront and versioned JSON APIs. Vercel hosts production and GitHub Actions validates every change."
        ),
        callout_box("The assistant is retrieval-first. The model may write an answer only after trusted chunks pass retrieval and relevance checks, and every live answer must cite valid source identifiers."),
        p("Core stack", "h2"),
        data_table(
            ["Layer", "Technology", "Responsibility"],
            [
                ["Web", "React, TypeScript, Vite", "Storefront, localization, cart, checkout and Lumi UI."],
                ["API", "Python, FastAPI, Pydantic", "Typed HTTP contracts, middleware, orchestration and static delivery."],
                ["AI", "LangChain, ChatOpenAI", "Structured model calls, prompt controls and fallback handling."],
                ["Retrieval", "PostgreSQL FTS, pgvector, local KB", "Hybrid candidates, fusion, reranking and citations."],
                ["Data", "SQLAlchemy async, PostgreSQL", "Orders, products, document chunks and vector storage."],
                ["Delivery", "Vercel, GitHub Actions", "Production deployments and continuous quality checks."],
            ],
            [29 * mm, 45 * mm, 98 * mm],
        ),
        PageBreak(),
    ]

    story += section("Runtime architecture", "Request and deployment topology")
    story += [
        p("Browser request flow", "h2"),
        data_table(
            ["Stage", "Behavior"],
            [
                ["1. Edge routing", "The Vercel production alias routes the request to the Lumina project."],
                ["2. FastAPI entrypoint", "backend.app.main:app initializes middleware, routers and the application lifespan."],
                ["3. API or asset", "Requests under /api/v1 and /health use API routers; other paths are served from frontend/dist."],
                ["4. Response security", "Security headers, request identifiers, compression and rate controls are applied."],
                ["5. Client state", "React manages locale, product filtering, cart state, checkout state and assistant history."],
            ],
            [38 * mm, 134 * mm],
        ),
        Spacer(1, 6 * mm),
        p("Repository map", "h2"),
        *bullets(
            [
                "frontend/src - React components, catalog fallback, i18n, API client and styles.",
                "frontend/public/assets - locally served product photography and Lumina brand assets.",
                "backend/app/api/routes - health, catalog, order and assistant endpoints.",
                "backend/app/services - commerce and assistant application services.",
                "backend/app/rag - ingestion, guardrails, local knowledge, retrieval and result types.",
                "backend/knowledge - approved company documents used by retrieval.",
                "backend/evals - golden dataset and RAGAS evaluation entrypoint.",
                ".github/workflows - continuous integration pipeline.",
            ]
        ),
        PageBreak(),
    ]

    story += section("RAG and LLM pipeline", "Grounded response generation")
    story += [
        p("1. Validate the request", "h2"),
        p("Pydantic validates locale, session identifier, message length, history and cart context. Rate limiting applies specifically to chat traffic."),
        p("2. Inspect prompt injection risk", "h2"),
        p("PromptInjectionGuard detects direct instruction override attempts, prompt disclosure requests, role markup and common obfuscation patterns. High-risk requests receive a safe refusal before retrieval or model invocation."),
        p("3. Classify intent and build a retrieval query", "h2"),
        p("The service classifies recommendation, shipping, returns, warranty, payment and product intents. Multilingual queries receive stable English retrieval anchors for consistent lexical behavior."),
        p("4. Retrieve and rerank", "h2"),
        p("When PostgreSQL is available, the retriever combines lexical full-text candidates and pgvector semantic candidates using reciprocal rank fusion. Deterministic keyword and source signals rerank the fused set. A local knowledge retriever provides graceful degradation."),
        p("5. Enforce evidence thresholds", "h2"),
        p("Chunks below the minimum relevance score are removed. If no strong evidence remains, Lumi abstains without calling the model."),
        p("6. Generate a structured answer", "h2"),
        p("ChatOpenAI receives a system policy, sanitized conversation context, cart summary, current question and delimited trusted sources. The response must match the LLMAnswer JSON schema."),
        p("7. Verify the result", "h2"),
        p("The service rejects unanswerable, low-confidence or uncited outputs. Cited identifiers must exist in the retrieved set. Any model exception falls back to a controlled local answer."),
        PageBreak(),
    ]

    story += section("AI safety controls", "Defense in depth")
    story += [
        data_table(
            ["Control", "Implementation", "Failure behavior"],
            [
                ["Source isolation", "Retrieved text is wrapped as source data and explicitly cannot supply instructions.", "Ignore embedded commands."],
                ["Prompt injection guard", "Rules inspect override, exfiltration, role and encoded attack patterns.", "Return safe-refusal mode."],
                ["Low temperature", "LLM temperature is 0.1 by default.", "Reduce creative variance."],
                ["Structured output", "Pydantic-backed JSON schema defines answerability, confidence, citations and follow-ups.", "Reject invalid output."],
                ["Citation validation", "Only identifiers present in retrieved chunks are accepted.", "Abstain if no valid citation remains."],
                ["Relevance gate", "Minimum chunk score defaults to 0.32.", "Do not call the model without evidence."],
                ["PII guidance", "System policy prohibits passwords, tokens, documents and secrets.", "Redirect to safe support."],
                ["Operational fallback", "Model and database failures have controlled local paths.", "Preserve availability with reduced capability."],
            ],
            [32 * mm, 89 * mm, 51 * mm],
        ),
        Spacer(1, 6 * mm),
        p("Security headers", "h2"),
        *bullets(
            [
                "Content Security Policy permits same-origin scripts, images and API calls while blocking objects and framing.",
                "X-Content-Type-Options prevents MIME sniffing.",
                "X-Frame-Options and frame-ancestors prevent clickjacking.",
                "Permissions-Policy disables camera, microphone and geolocation access.",
                "Referrer-Policy limits cross-origin referrer exposure.",
            ]
        ),
        PageBreak(),
    ]

    story += section("API contracts", "Versioned HTTP interface")
    story += [
        data_table(
            ["Method", "Path", "Purpose"],
            [
                ["GET", "/health", "Runtime health, database mode, assistant mode and application version."],
                ["GET", "/metrics", "Prometheus-compatible runtime metrics when enabled by the service."],
                ["GET", "/api/v1/products", "Localized catalog source for storefront products."],
                ["POST", "/api/v1/orders/checkout", "Validate order input and create a simulated paid order."],
                ["POST", "/api/v1/assistant/chat", "Retrieve evidence and return a grounded assistant response."],
            ],
            [20 * mm, 57 * mm, 95 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Assistant response fields", "h2"),
        *bullets(
            [
                "message - customer-facing answer in the requested locale.",
                "intent - classified commerce intent.",
                "confidence - bounded evidence and model confidence.",
                "grounded - whether the answer is supported by retrieved evidence.",
                "mode - live-rag, local-rag, safe-refusal or abstention behavior.",
                "citations - validated source title, origin and excerpt.",
                "suggestions - up to three guided follow-up questions.",
                "actions - validated UI actions such as opening a product or cart.",
            ]
        ),
        PageBreak(),
    ]

    story += section("Configuration and secrets", "Production operations")
    story += [
        data_table(
            ["Variable", "Required", "Purpose"],
            [
                ["APP_ENV", "Yes", "Enables production behavior and disables interactive API docs."],
                ["APP_SECRET_KEY", "Yes", "Application secret used for production-safe configuration."],
                ["DATABASE_URL", "For live pgvector", "Async PostgreSQL connection string with the vector extension."],
                ["OPENAI_API_KEY", "For live LLM", "Server-side OpenAI credential stored as a Vercel secret."],
                ["LLM_MODEL", "Optional", "Defaults to gpt-4.1-mini."],
                ["EMBEDDING_MODEL", "Optional", "Defaults to text-embedding-3-small."],
                ["LLM_TEMPERATURE", "Optional", "Defaults to 0.1."],
                ["FRONTEND_ORIGIN", "Optional", "Allowed browser origin for CORS."],
            ],
            [43 * mm, 30 * mm, 99 * mm],
        ),
        Spacer(1, 7 * mm),
        p("Secret handling", "h2"),
        *bullets(
            [
                "Never commit .env or production secrets.",
                "Use Vercel encrypted environment variables for production credentials.",
                "Redeploy after changing a production environment variable.",
                "Rotate a credential immediately if it appears in logs, commits or client bundles.",
                "Only the backend can read OPENAI_API_KEY; the React build never receives it.",
            ]
        ),
        PageBreak(),
    ]

    story += section("Delivery and quality", "CI/CD, tests and observability")
    story += [
        p("Continuous delivery", "h2"),
        p("The GitHub repository is connected to Vercel. A push to main creates a production deployment; pull requests receive preview deployments. The commercial production domain follows the latest successful production deployment."),
        p("Continuous integration", "h2"),
        *bullets(
            [
                "Ruff validates Python style and common correctness rules.",
                "Pytest covers commerce behavior, retrieval knowledge and prompt-injection controls.",
                "TypeScript compilation validates client contracts.",
                "Vite builds the production client bundle.",
                "A CSP regression test keeps storefront assets executable under the security policy.",
            ]
        ),
        p("Evaluation", "h2"),
        p("The golden dataset contains representative, adversarial and unanswerable questions. The optional RAGAS workflow can measure faithfulness, answer relevance and context quality before model, prompt or retriever changes are released."),
        p("Observability roadmap", "h2"),
        *bullets(
            [
                "Export OpenTelemetry traces for request, retrieval and model spans.",
                "Track p50 and p95 latency, token cost, fallback rate, abstention rate and citation validity.",
                "Replace in-memory rate limiting with Redis for multi-instance consistency.",
                "Process ingestion and blue-green index updates through a durable queue.",
            ]
        ),
        PageBreak(),
    ]

    story += section("Deployment runbook", "Release and verification")
    story += [
        p("Standard release", "h2"),
        *bullets(
            [
                "Run Python linting and the backend test suite.",
                "Run the production frontend build.",
                "Review staged changes and confirm no secrets are tracked.",
                "Push the approved commit to main.",
                "Wait for GitHub Actions and the Vercel production deployment to succeed.",
                "Verify the production home page, /health, product API and assistant response mode.",
                "Perform a visual smoke test in desktop and mobile layouts.",
            ]
        ),
        p("Assistant verification", "h2"),
        *bullets(
            [
                "Ask a supported product comparison and require grounded=true.",
                "Confirm mode=live-rag when OPENAI_API_KEY is configured.",
                "Confirm at least one citation supports the factual answer.",
                "Send a prompt-injection attempt and require safe-refusal mode.",
                "Ask an unsupported question and confirm abstention rather than fabrication.",
            ]
        ),
        p("Rollback", "h2"),
        p("If a release fails smoke testing, promote the previous Ready deployment in Vercel and investigate in a branch. Do not remove the stable production alias during rollback."),
        Spacer(1, 8 * mm),
        p("Production endpoint", "h2"),
        callout_box(PRODUCTION_URL),
    ]
    return story


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    make_doc(
        OUTPUT_DIR / "lumina-product-and-service-guide.pdf",
        DocMeta(
            title="Product & Service\nGuide",
            subtitle="A clear introduction to the Lumina shopping experience\nand the Lumi AI product specialist.",
            label="Non-technical documentation",
        ),
        nontechnical_story(),
    )
    make_doc(
        OUTPUT_DIR / "lumina-technical-documentation.pdf",
        DocMeta(
            title="Technical\nDocumentation",
            subtitle="Architecture, AI safety, API contracts, operations\nand production delivery reference.",
            label="Engineering documentation",
        ),
        technical_story(),
    )


if __name__ == "__main__":
    main()
