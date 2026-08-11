import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARXIV_PAPER_URL = "https://arxiv.org/abs/2605.27383"
LEGACY_LOCAL_PDF_URL = "paper/MultiLanTTS_camera_v0.1.pdf"


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"link", "script"}:
            self.links.append(attrs.get("href") or attrs.get("src"))


def test_required_pages_assets_and_data_exist():
    expected_files = [
        "index.html",
        "README.md",
        "assets/data/demo-data.json",
        "assets/figures/dgsa.png",
        "assets/figures/tdsc.png",
    ]

    missing = [path for path in expected_files if not (ROOT / path).exists()]

    assert missing == []


def test_demo_data_references_existing_assets():
    data = json.loads((ROOT / "assets/data/demo-data.json").read_text(encoding="utf-8"))

    assert data["paper"]["title"].startswith("Bridging the Stability-Expressivity Gap")
    assert data["paper"]["venue"] == "ICML 2026"
    assert {section["id"] for section in data["sections"]} == {
        "benchmarks",
        "cloning",
        "erosion",
        "dgsa",
        "tdsc",
    }

    missing = []
    for figure in data["figures"]:
        if not (ROOT / figure["src"]).exists():
            missing.append(figure["src"])
    for section in data["sections"]:
        for group in section["groups"]:
            for sample in group["samples"]:
                for audio in sample["audios"]:
                    if not (ROOT / audio["src"]).exists():
                        missing.append(audio["src"])

    assert missing == []


def test_index_contains_academic_project_sections():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = IdCollector()
    parser.feed(html)

    for section_id in [
        "overview",
        "key-idea",
        "methods",
        "audio-demo",
        "results",
        "citation",
    ]:
        assert section_id in parser.ids

    assert "assets/data/demo-data.json" in html
    assert "Code coming soon" in html


def test_public_pages_are_cross_linked():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    demo_data_text = (ROOT / "assets/data/demo-data.json").read_text(encoding="utf-8")
    demo_data = json.loads(demo_data_text)

    expected_urls = [
        "https://insiderx-pro.github.io/SE-Bridge-TTS/",
        "https://github.com/InsiderX-Pro/SE-Bridge-TTS",
        "https://huggingface.co/InsiderX-Pro/SE-Bridge-TTS",
    ]

    assert expected_urls[1] in html
    assert expected_urls[2] in html
    assert demo_data["paper"]["codeUrl"] == expected_urls[1]
    for url in expected_urls:
        assert url in readme

    for public_text in [html, readme, demo_data_text]:
        assert "https://github.com/piedpiperG/SE-Bridge-TTS" not in public_text
        assert "https://piedpiperg.github.io/SE-Bridge-TTS/" not in public_text


def test_public_paper_links_use_arxiv_entry():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    demo_data_text = (ROOT / "assets/data/demo-data.json").read_text(encoding="utf-8")
    demo_data = json.loads(demo_data_text)

    assert demo_data["paper"]["paperUrl"] == ARXIV_PAPER_URL

    for public_text in [html, readme, demo_data_text]:
        assert ARXIV_PAPER_URL in public_text
        assert LEGACY_LOCAL_PDF_URL not in public_text


def test_readme_presents_project_homepage_methods_results_and_weights():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    expected_snippets = [
        "assets/figures/dgsa.png",
        "assets/figures/tdsc.png",
        '<h1 align="center">Bridging the Stability-Expressivity Gap</h1>',
        "for Low-Resource Spoken Language Models",
        "SE-Bridge-TTS | ICML 2026",
        "https://img.shields.io/badge/Project_Page-Open_Demo",
        "https://img.shields.io/badge/Paper-arXiv_2605.27383",
        "https://img.shields.io/badge/Weights-Hugging_Face",
        "## Methods",
        "## Main Results",
        "## Open FLEURS Evaluation",
        "## Use the Weights",
        "Accuracy = 100 - WER",
        "Thai standard TTS",
        "Azure: 63.5% accuracy",
        "Lao zero-shot cloning",
        "Other tested systems: not supported",
        "calibrated CER = max(0, generated CER - ground-truth CER)",
        "Accuracy = 1 - calibrated CER",
        "Higgs Audio v3",
        "OmniVoice",
        "X-Voice Stage1",
        "<u>78.2%</u>",
        "**83.4%**",
        "Each detail cell below is `Cal. CER↓ / SIM↑`.",
        "Lao | Chinese",
        "**0.2603** / **0.726**",
        "Thai | English",
        "<u>0.0307</u> / **0.586**",
        "evaluation/fleurs-lo-th-255pair/",
        "`thai_tts.pt`",
        "`lao_tts.pt`",
        "CosyVoice2 cross-lingual inference by default; optional zero-shot use with caution",
        "CosyVoice2 cross-lingual inference",
        "## Acknowledgements",
        "SE-Bridge-TTS thanks the following open-source projects:",
        "FunAudioLLM/CosyVoice",
        "facebook/mms-tts",
        "Higgs Audio v3",
        "OmniVoice",
        "X-Voice",
        "assets/audio/benchmarks/thai/ours-dgsa-sample1.wav",
        "assets/audio/benchmarks/lao/ours-tdsc-sample1.wav",
        "assets/audio/cloning/thai/ours-th-9804.wav",
        "assets/audio/cloning/lao/ours-common-voice-lo.wav",
    ]

    for snippet in expected_snippets:
        assert snippet in readme


def test_public_fleurs_evaluation_files_and_results_are_present():
    eval_root = ROOT / "evaluation" / "fleurs-lo-th-255pair"
    expected_files = [
        "README.md",
        "results.json",
        "summary_same_language.csv",
        "summary_cross_prompt_by_model.csv",
        "summary_cross_prompt_by_direction.csv",
        "scripts/render_results.py",
    ]

    missing = [path for path in expected_files if not (eval_root / path).exists()]
    assert missing == []

    results = json.loads((eval_root / "results.json").read_text(encoding="utf-8"))
    assert results["metadata"]["benchmark"] == "FLEURS Lao/Thai 255-pair multilingual prompt benchmark"
    assert results["metadata"]["metrics"]["accuracy"] == "1 - calibrated_cer_mean"

    by_model = {row["model"]: row for row in results["cross_language_prompt_by_model"]}
    se_bridge = by_model["SE-Bridge-TTS"]
    assert se_bridge["ok"] == 1020
    assert se_bridge["total"] == 1020
    assert round(se_bridge["accuracy_percent"], 1) == 83.4
    assert round(se_bridge["speaker_similarity_mean"], 3) == 0.593

    xvoice = by_model["X-Voice Stage1"]
    assert xvoice["ok"] == 510
    assert xvoice["total"] == 1020

    same_by_model_language = {
        (row["model"], row["language_id"]): row
        for row in results["same_language_prompt_by_model_language"]
    }
    xvoice_lao = same_by_model_language[("X-Voice Stage1", "lo")]
    assert xvoice_lao["ok"] == 0
    assert xvoice_lao["total"] == 255
    assert xvoice_lao["accuracy_percent"] is None

    eval_readme = (eval_root / "README.md").read_text(encoding="utf-8")
    expected_eval_snippets = [
        "accuracy = 1 - calibrated_cer",
        "Best results are **bold**. Second-best results are <u>underlined</u>.",
        "| SE-Bridge-TTS | 1020/1020 | **83.4%** | <u>0.593</u> |",
        "Each cell is `Cal. CER↓ / SIM↑`.",
        "| Lao | Lao | <u>0.2330</u> / <u>0.699</u> |",
        "| Thai | Chinese | **0.0089** / 0.674 |",
    ]
    for snippet in expected_eval_snippets:
        assert snippet in eval_readme
