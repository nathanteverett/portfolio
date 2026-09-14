---
layout: default
title: Video Overlay Detector
permalink: /video-overlay-detector/
---

[← Back to portfolio](../)

# Video Overlay Detector

**Applied computer vision · Model training · Evaluation**

[View code on GitHub](https://github.com/nathanteverett/video-overlay-detector)

A compact detector for identifying digital overlays in video frames: whether an overlay is present, where it appears, and which of seven categories it belongs to.

Built as a time-constrained technical assessment prototype. The work covers data auditing, source-separated splits, GPU fine-tuning, experiment comparison, inference exports, and error analysis.

## Approach

I fine-tuned a COCO-pretrained **YOLO11s** detector using Python and PyTorch. One model predicts bounding boxes and types; a frame is marked positive when at least one detection meets the confidence threshold. The categories are watermark, banner, logo, graphic, subtitle, text, and other. Signs and logos physically present in the scene fall outside the intended overlay definition.

The annotation catalog contained **156,211 frames from 7,579 videos**. I separated videos across training, validation, and test and preserved two fixed 5,000-frame holdouts. The selected model trained on **19,646 frames from 5,998 videos**, with at most four frames per video to broaden source coverage.

The pipeline preserves original records, records coordinate conversions and preprocessing, and keeps positive frames without boxes out of box supervision without relabeling them as negatives. Inference exports frame labels and normalized bounding boxes in CSV format.

## Results

| Metric | Local test |
| --- | ---: |
| Frame-level F1 | **92.01%** |
| Frame-level precision / recall | 94.23% / 89.90% |
| Detection mAP (IoU 0.50), including type | 32.17% |
| Detection mAP (IoU 0.50–0.95), including type | 19.07% |
| Macro F1 across seven types | 41.11% |

Binary metrics cover all 5,000 test frames. Box and type metrics cover 4,926 frames with known localization. These are local evaluation results, not an employer's hidden benchmark. The local test was assessed twice; revised inference settings were selected on validation before the second assessment.

## What the experiments showed

- **Source coverage mattered.** At the same training frame budget and shared inference settings, source-balanced sampling improved validation typed mAP (IoU 0.50–0.95) from **23.25% to 25.23%**.
- **More training did not automatically help.** Expanding to 123,998 training frames or training the source-balanced sample for ten epochs performed worse on validation. The selected run used five epochs, AdamW, a 0.0003 learning rate, and mixed precision.
- **Presence detection was stronger than detailed detection.** Small-overlay AP was only **5.57%**. Watermark/logo confusion and the gap between type-aware and class-agnostic detection scores identified specific weaknesses.

These were single-seed comparisons. Sampling changed both image membership and class prevalence, so the improvement does not isolate one causal factor.

## Error analysis and next experiment

**The investigation confirmed dataset-quality problems affecting the training annotations.** A random review of **50 training frames** identified **16 requiring annotation review or correction**, all among the **23 supplied positive frames**. All **27 supplied negatives** were accepted. The review documented inconsistent overlay types, missing or misplaced boxes, and native game content incorrectly annotated as digital overlays.

**Data quality was a substantive project finding.** The investigation moved beyond aggregate model scores to inspect the supervision itself, confirmed concrete defects, and identified specific label and localization corrections. This established annotation quality as a limitation of the supplied dataset and made correcting the supervision the priority for further model development.

My next experiment would compare original and corrected training annotations using the same images, initialization, training budget, and unchanged holdouts. Production readiness would also require deployment benchmarks and an aligned quality comparison before claiming savings over a VLM.

*This case study summarizes the prototype. The supplied assessment dataset, private infrastructure details, and model weights are not distributed here.*
