---
layout: default
title: Mushroom identification with photos and weather
permalink: /mushroom-identification/
---

[← Back to portfolio](../)

# Does recent weather help identify mushrooms from photos?

**Photos plus field metadata gave the most accurate species identifications.** On 4,687 FungiTastic-Mini validation sightings from 2022, a frozen DINOv2-Base image model reached 79.50% top-1 accuracy. Adjusting its species scores using habitat, substrate, and calendar month raised accuracy to 80.71%.

I tested whether the previous 30 days of weather could help identify the same specimens. I matched each sighting to daily ERA5 temperature lows, highs, and precipitation. In PyTorch, I trained a two-layer weather encoder and used cross-attention to let each photo draw on those 30 days before pooling the photos into one prediction per sighting.

| Inputs | Sighting top-1 | macro-F1 over 193 observed categories |
|---|---:|---:|
| Photos | 79.50% | 55.22% |
| Photos + field metadata | **80.71%** | 58.79% |
| Photos + weather | 77.90% | 55.50% |
| Photos + weather + field metadata | 78.90% | **58.97%** |

All four comparisons used the same sightings and ranked all 215 species. Compared with photos alone, the weather model corrected 253 identifications and introduced 328 errors. That left it 1.60 percentage points behind (paired 95% bootstrap interval for the difference, −2.62 to −0.62 points).

I selected photos plus field metadata using sighting top-1, the metric chosen before training. The weather result covers one training seed and measures the weather inputs and fusion architecture together.

[Dataset and benchmark · FungiTastic](https://github.com/BohemianVRA/FungiTastic)
