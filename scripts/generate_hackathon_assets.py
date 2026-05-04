from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "hackathon" / "assets"

COLORS = {
    "bg": "#edf1ef",
    "paper": "#fcfdfb",
    "ink": "#17211d",
    "muted": "#63706a",
    "line": "#cbd5d1",
    "green": "#176b4d",
    "green_soft": "#dceee5",
    "red": "#9a342c",
    "red_soft": "#f4dfdc",
    "blue": "#235f82",
    "blue_soft": "#ddeaf0",
    "gold": "#8a671f",
    "gold_soft": "#f3e6bd",
}


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    candidates = {
        "regular": [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ],
        "bold": [
            r"C:\Windows\Fonts\seguisb.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ],
        "mono": [
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\cour.ttf",
        ],
    }
    for candidate in candidates[weight]:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=outline, width=width)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    max_chars: int,
    line_gap: int,
    font_obj: ImageFont.FreeTypeFont,
    fill: str,
) -> int:
    x, y = xy
    for line in wrap(text, max_chars):
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


def draw_background(draw: ImageDraw.ImageDraw, size: tuple[int, int]) -> None:
    width, height = size
    for x in range(0, width, 44):
        draw.line((x, 0, x, height), fill="#dfe6e2", width=1)
    for y in range(0, height, 44):
        draw.line((0, y, width, y), fill="#dfe6e2", width=1)


def draw_status(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, detail: str, accepted: bool) -> None:
    fill = COLORS["green_soft"] if accepted else COLORS["red_soft"]
    color = COLORS["green"] if accepted else COLORS["red"]
    rounded(draw, box, fill=fill, outline=color, width=2)
    x1, y1, _, _ = box
    draw.text((x1 + 28, y1 + 26), label, font=font(52, "bold"), fill=color)
    draw.text((x1 + 30, y1 + 92), detail, font=font(23), fill=COLORS["ink"])


def make_share_card() -> Path:
    size = (1600, 900)
    image = Image.new("RGB", size, COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw_background(draw, size)

    draw.text((82, 70), "0G APAC Hackathon MVP", font=font(28, "bold"), fill=COLORS["blue"])
    draw.text((78, 112), "PrivyGate", font=font(110, "bold"), fill=COLORS["ink"])
    y = draw_wrapped(
        draw,
        "Privacy-preserving multi-authority attribute authorization for autonomous agents on 0G.",
        (86, 250),
        64,
        8,
        font(34),
        COLORS["muted"],
    )

    rounded(draw, (82, y + 28, 780, y + 212), fill=COLORS["paper"], outline=COLORS["line"])
    draw.text((114, y + 58), "POLICY", font=font(24, "bold"), fill=COLORS["blue"])
    draw.text((114, y + 98), "University:role:student", font=font(28, "mono"), fill=COLORS["ink"])
    draw.text((114, y + 138), "AND Lab:role:researcher", font=font(28, "mono"), fill=COLORS["ink"])

    draw_status(draw, (840, 96, 1508, 250), "ALICE ACCEPTED", "student + researcher attributes satisfy the policy", True)
    draw_status(draw, (840, 288, 1508, 442), "BOB REJECTED", "student-only credential cannot satisfy the policy", False)
    draw_status(draw, (840, 480, 1508, 634), "REVOKED REJECTED", "old signatures fail after credential revocation", False)

    rounded(draw, (82, 654, 1508, 814), fill=COLORS["paper"], outline=COLORS["line"])
    draw.text((114, 684), "0G Chain Registry", font=font(36, "bold"), fill=COLORS["gold"])
    proof = "authority key hashes -> policy hashes -> revocation state -> verification events"
    draw.text((114, 738), proof, font=font(31), fill=COLORS["ink"])
    draw.text((114, 784), "Off-chain symbolic attribute-signature prototype; on-chain audit evidence layer.", font=font(23), fill=COLORS["muted"])

    output = ASSET_DIR / "privygate-share-card.png"
    image.save(output, optimize=True)
    return output


def make_mobile_story() -> Path:
    size = (1080, 1920)
    image = Image.new("RGB", size, COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw_background(draw, size)

    draw.text((70, 96), "PrivyGate", font=font(96, "bold"), fill=COLORS["ink"])
    y = draw_wrapped(
        draw,
        "Private multi-authority authorization for AI agent tool access on 0G.",
        (76, 226),
        31,
        12,
        font(46),
        COLORS["muted"],
    )

    rounded(draw, (70, y + 58, 1010, y + 306), fill=COLORS["paper"], outline=COLORS["line"])
    draw.text((112, y + 98), "Policy", font=font(32, "bold"), fill=COLORS["blue"])
    draw.text((112, y + 152), "University:role:student", font=font(34, "mono"), fill=COLORS["ink"])
    draw.text((112, y + 204), "AND Lab:role:researcher", font=font(34, "mono"), fill=COLORS["ink"])

    start = y + 370
    draw_status(draw, (70, start, 1010, start + 190), "ACCEPT", "Alice has both required attributes.", True)
    draw_status(draw, (70, start + 238, 1010, start + 428), "REJECT", "Bob is missing Lab:role:researcher.", False)
    draw_status(draw, (70, start + 476, 1010, start + 666), "REVOKED", "Alice's old signature fails after revocation.", False)

    rounded(draw, (70, 1582, 1010, 1780), fill=COLORS["gold_soft"], outline="#cbb677")
    draw.text((112, 1624), "0G Registry Evidence", font=font(42, "bold"), fill=COLORS["gold"])
    draw.text((112, 1690), "authorities / policies / revocations / events", font=font(31), fill=COLORS["ink"])
    draw.text((112, 1738), "Final submission replaces placeholders with mainnet links.", font=font(25), fill=COLORS["muted"])

    output = ASSET_DIR / "privygate-mobile-story.png"
    image.save(output, optimize=True)
    return output


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [make_share_card(), make_mobile_story()]
    for output in outputs:
        print(f"generated {output.relative_to(ROOT)} {output.stat().st_size} bytes")


if __name__ == "__main__":
    main()
