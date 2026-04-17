import io

from PIL import Image

from app import main as app_main


def _make_png(width=128, height=128):
    image = Image.new("RGB", (width, height), color=(0, 180, 0))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    data = buf.getvalue()

    class UploadedFile:
        name = "leaf.png"

        def getvalue(self):
            return data

    return UploadedFile()


def test_validate_land_budget_accepts_normal_values(monkeypatch):
    monkeypatch.setattr(app_main.st, "error", lambda *_args, **_kwargs: None)
    assert app_main._validate_land_budget(5.0, 50000) is True


def test_validate_land_budget_rejects_out_of_range(monkeypatch):
    errors = []
    monkeypatch.setattr(app_main.st, "error", lambda msg, **_kwargs: errors.append(msg))

    assert app_main._validate_land_budget(0.01, 99999999) is False
    assert len(errors) >= 1


def test_validate_crop_choice_checks_whitelist(monkeypatch):
    monkeypatch.setattr(app_main.st, "error", lambda *_args, **_kwargs: None)
    allowed = ["rice", "wheat", "cotton"]

    assert app_main._validate_crop_choice("rice", allowed, "crop") is True
    assert app_main._validate_crop_choice("banana", allowed, "crop") is False


def test_validate_uploaded_image_accepts_valid_file(monkeypatch):
    monkeypatch.setattr(app_main.st, "error", lambda *_args, **_kwargs: None)
    uploaded = _make_png()

    assert app_main._validate_uploaded_image(uploaded) is True
