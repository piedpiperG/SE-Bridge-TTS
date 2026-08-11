<h1 align="center">Bridging the Stability-Expressivity Gap</h1>

<h3 align="center">
  Synthetic Data Scaling and Preference Alignment<br>
  for Low-Resource Spoken Language Models
</h3>

<p align="center"><strong>SE-Bridge-TTS | ICML 2026</strong></p>

<p align="center">
  <a href="https://insiderx-pro.github.io/SE-Bridge-TTS/">
    <img alt="Project page" src="https://img.shields.io/badge/Project_Page-Open_Demo-0f766e?style=for-the-badge">
  </a>
  <a href="https://arxiv.org/abs/2605.27383">
    <img alt="arXiv paper" src="https://img.shields.io/badge/Paper-arXiv_2605.27383-b31b1b?style=for-the-badge">
  </a>
  <a href="https://huggingface.co/InsiderX-Pro/SE-Bridge-TTS">
    <img alt="Hugging Face weights" src="https://img.shields.io/badge/Weights-Hugging_Face-f59e0b?style=for-the-badge">
  </a>
  <a href="https://github.com/InsiderX-Pro/SE-Bridge-TTS">
    <img alt="GitHub repository" src="https://img.shields.io/badge/Code-GitHub-24292f?style=for-the-badge">
  </a>
</p>

SE-Bridge-TTS is a low-resource Thai and Lao speech synthesis project. It studies a practical failure mode in spoken language models: synthetic data improves pronunciation stability, but too much flat synthetic speech erodes prosody and speaker expressivity. The release provides public Thai and Lao CosyVoice2-compatible checkpoints on Hugging Face.

## What This Work Does

| Capability | What it enables |
| --- | --- |
| Thai DGSA | Recovers expressive speech at high synthetic-data ratios while preserving intelligibility and speaker identity. |
| Lao TDSC | Builds a pure-synthetic self-improvement loop for Lao TTS and zero-shot voice cloning without authentic target-language recordings. |
| Open checkpoints | Provides public Thai and Lao CosyVoice2-compatible weights, audio demos, a project page, and Hugging Face inference guidance. |

## Methods

### DGSA: Disentanglement-Guided Self-Alignment

<p align="center">
  <img src="assets/figures/dgsa.png" alt="Disentanglement-Guided Self-Alignment method overview" width="860">
</p>

DGSA uses the prosody-timbre separation in flow-matching SLMs to build preference pairs that reward stable, expressive speech without collapsing speaker identity.

### TDSC: Temperature-Driven Self-Critique

<p align="center">
  <img src="assets/figures/tdsc.png" alt="Temperature-Driven Self-Critique method overview" width="860">
</p>

TDSC samples candidates across conservative-to-expressive temperatures, filters them with automatic quality checks, and iteratively improves low-resource synthesis when real target-language speech is unavailable.

## Main Results

Paper accuracy is reported as `Accuracy = 100 - WER`, so higher is
better. Higher SIM, NMOS, and SMOS are also better.

| Paper setting | SE-Bridge-TTS | Strong comparison | Takeaway |
| --- | --- | --- | --- |
| Thai standard TTS | **61.1% accuracy** (38.9 WER), **4.51 NMOS** | Azure: 63.5% accuracy (36.5 WER), 4.01 NMOS; ElevenLabs-v3: 59.4% accuracy, 4.21 NMOS | Comparable intelligibility with stronger naturalness. |
| Lao standard TTS | **70.2% accuracy** (29.8 WER), **4.53 NMOS** | Gemini Flash: 65.8% accuracy, 4.12 NMOS; MMS-TTS: 55.2% accuracy, 3.52 NMOS | Best accuracy and naturalness among tested systems. |
| Thai zero-shot cloning | **61.1% accuracy** (38.9 WER), **0.84 SIM**, **4.51 SMOS** | ElevenLabs-v3: 57.7% accuracy (42.3 WER), 0.78 SIM, 4.23 SMOS | Better intelligibility and speaker preservation. |
| Lao zero-shot cloning | **70.2% accuracy** (29.8 WER), **0.81 SIM**, **4.32 SMOS** | Other tested systems: not supported | Public Lao voice cloning capability. |

Selected demos are available on the [project page](https://insiderx-pro.github.io/SE-Bridge-TTS/#audio-demo), including [Thai standard TTS](assets/audio/benchmarks/thai/ours-dgsa-sample1.wav), [Lao standard TTS](assets/audio/benchmarks/lao/ours-tdsc-sample1.wav), [Thai cloning](assets/audio/cloning/thai/ours-th-9804.wav), and [Lao cloning](assets/audio/cloning/lao/ours-common-voice-lo.wav).

## Open FLEURS Evaluation

We also publish a reproducible FLEURS benchmark comparing the released
SE-Bridge-TTS checkpoints with three recent open multilingual TTS
systems: Higgs Audio v3, OmniVoice, and X-Voice Stage1. The evaluation
uses 255 paired Lao/Thai target sentences and reference prompts from
Lao, Thai, Chinese, and English. It tests whether a model can synthesize
Lao/Thai speech while preserving the prompt speaker.

Although SE-Bridge-TTS was developed before these newer open systems,
it still reaches the best overall calibrated accuracy in the
Chinese/English prompt -> Lao/Thai target setting, while remaining
competitive on speaker similarity.

Accuracy keeps the CER signal but makes it easier to read:

```text
calibrated CER = max(0, generated CER - ground-truth CER)
Accuracy = 1 - calibrated CER
```

Ground-truth CER is the ASR error measured on original FLEURS target
audio, so the metric discounts recognizer baseline errors and focuses on
synthesis degradation. Higher is better for Accuracy and speaker
similarity.

Best results are **bold**. Second-best results are <u>underlined</u>.

| Model | Supported samples | Accuracy | Speaker similarity |
| --- | --- | --- | --- |
| Higgs Audio v3 | 1020/1020 | <u>78.2%</u> | 0.520 |
| OmniVoice | 1020/1020 | 75.9% | **0.645** |
| SE-Bridge-TTS | 1020/1020 | **83.4%** | <u>0.593</u> |
| X-Voice Stage1 | 510/1020 | 53.7% | 0.361 |

Each detail cell below is `Cal. CER↓ / SIM↑`.

| Target | Prompt | Higgs Audio v3 | OmniVoice | SE-Bridge-TTS | X-Voice Stage1 |
| --- | --- | --- | --- | --- | --- |
| Lao | Lao | <u>0.2330</u> / <u>0.699</u> | 0.3912 / **0.771** | **0.2170** / 0.694 | - / - |
| Lao | English | <u>0.4491</u> / <u>0.492</u> | 0.4532 / **0.537** | **0.3408** / 0.459 | - / - |
| Lao | Chinese | <u>0.3828</u> / 0.651 | 0.4306 / <u>0.711</u> | **0.2603** / **0.726** | - / - |
| Thai | Thai | **0.0095** / 0.761 | <u>0.0210</u> / **0.794** | 0.0264 / 0.763 | 0.1879 / <u>0.774</u> |
| Thai | English | 0.0310 / 0.263 | <u>0.0307</u> / **0.586** | **0.0268** / <u>0.452</u> | 0.8227 / -0.019 |
| Thai | Chinese | **0.0089** / 0.674 | 0.0497 / **0.745** | <u>0.0356</u> / 0.736 | 0.1035 / <u>0.741</u> |

This public run covers same-language Lao/Thai prompts plus Chinese and
English prompts to Lao/Thai targets. Unsupported Lao directions for
X-Voice Stage1 are counted as coverage failures and excluded from
quality averages.

The full protocol, machine-readable results, and table renderer are in
[`evaluation/fleurs-lo-th-255pair`](evaluation/fleurs-lo-th-255pair/).

## Use the Weights

The release checkpoints are hosted at:

https://huggingface.co/InsiderX-Pro/SE-Bridge-TTS

For inference:

1. Open the Hugging Face model card above.
2. Download `thai_tts.pt` or `lao_tts.pt` from the model repository.
3. Follow the CosyVoice2 loading example in the model card.

| File | Language | Recommended use |
| --- | --- | --- |
| `thai_tts.pt` | Thai | CosyVoice2 cross-lingual inference by default; optional zero-shot use with caution |
| `lao_tts.pt` | Lao | CosyVoice2 cross-lingual inference |

This GitHub repository is intentionally lightweight: it hosts the project page, audio demos, paper links, and release pointers; the runnable checkpoint package lives on Hugging Face.

## Links

| Resource | Link |
| --- | --- |
| Project page and audio browser | https://insiderx-pro.github.io/SE-Bridge-TTS/ |
| Paper | https://arxiv.org/abs/2605.27383 |
| Weights and inference notes | https://huggingface.co/InsiderX-Pro/SE-Bridge-TTS |
| FLEURS evaluation protocol and results | `evaluation/fleurs-lo-th-255pair/` |
| Demo metadata | `assets/data/demo-data.json` |

## Citation

```bibtex
@inproceedings{geng2026bridging,
  title = {Bridging the Stability-Expressivity Gap: Synthetic Data Scaling and Preference Alignment for Low-Resource Spoken Language Models},
  author = {Geng, Yizhong and Li, Yanliang and Yang, Jinghan and Jiang, Tianhan and An, Boxun and Li, Ya and Shen, Xiaoyu},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year = {2026}
}
```

## Acknowledgements

SE-Bridge-TTS thanks the following open-source projects:

- [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice), which provides the CosyVoice2 toolkit and inference stack used by the released checkpoints.
- [facebook/mms-tts](https://huggingface.co/facebook/mms-tts), a multilingual open-source TTS baseline included in the project demos.
- [Higgs Audio v3](https://github.com/boson-ai/higgs-audio), [OmniVoice](https://github.com/k2-fsa/OmniVoice), and [X-Voice](https://github.com/sunnyxrxrx/X-Voice), recent open multilingual speech generation systems referenced in the public FLEURS evaluation.

We thank the maintainers and contributors of these projects for making multilingual and low-resource speech synthesis research easier to reproduce, compare, and extend.
