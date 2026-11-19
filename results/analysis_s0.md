# Análise estatística — semente 0

Diferença contra `exp1_baseline_s0` no teste (6869 imagens), IC 95% por bootstrap pareado (2000 reamostragens). `*` = intervalo não contém zero.

## exp2_l1_30_s0

McNemar (acurácia): p = 0.2 (só o baseline acerta: 68; só o experimento acerta: 53)

Contraste raras − demais (ΔF1 médio): +0.5 p.p., IC 95% [-0.3, +1.2] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -0.2 | [-0.5, +0.2] |
| accuracy | -0.2 | [-0.5, +0.1] |
| f1_articulated_truck | -0.3 | [-1.1, +0.5] |
| f1_background | +0.0 | [-0.3, +0.3] |
| f1_bicycle | +0.1 | [-0.8, +1.1] |
| f1_bus | +0.3 | [-0.1, +0.8] |
| f1_car | -0.7 | [-1.6, +0.1] |
| f1_motorcycle | +0.1 | [-0.6, +0.8] |
| f1_non-motorized_vehicle | +0.3 | [-1.2, +2.0] |
| f1_pedestrian | +0.0 | [-0.5, +0.6] |
| f1_pickup_truck | -1.3 * | [-2.3, -0.3] |
| f1_single_unit_truck | -0.1 | [-1.0, +0.8] |
| f1_work_van | -0.3 | [-1.1, +0.4] |
| recall_articulated_truck | +0.5 | [-0.5, +1.6] |
| recall_background | +0.0 | [-0.5, +0.5] |
| recall_bicycle | +0.0 | [-1.2, +1.2] |
| recall_bus | +0.1 | [-0.4, +0.8] |
| recall_car | +0.4 | [-0.4, +1.2] |
| recall_motorcycle | -0.7 | [-1.7, +0.0] |
| recall_non-motorized_vehicle | +1.9 | [+0.0, +4.1] |
| recall_pedestrian | +0.8 * | [+0.1, +1.6] |
| recall_pickup_truck | -1.3 | [-2.8, +0.0] |
| recall_single_unit_truck | -2.2 * | [-3.4, -1.1] |
| recall_work_van | -0.8 | [-1.9, +0.3] |

## exp3_l1_60_s0

McNemar (acurácia): p = 0.19 (só o baseline acerta: 116; só o experimento acerta: 138)

Contraste raras − demais (ΔF1 médio): -0.3 p.p., IC 95% [-1.3, +0.8] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | +0.2 | [-0.2, +0.7] |
| accuracy | +0.3 | [-0.1, +0.8] |
| f1_articulated_truck | -0.5 | [-1.7, +0.7] |
| f1_background | -0.5 * | [-0.9, -0.1] |
| f1_bicycle | +1.3 | [-0.2, +2.7] |
| f1_bus | +0.9 * | [+0.3, +1.5] |
| f1_car | +1.7 * | [+0.5, +2.8] |
| f1_motorcycle | +0.3 | [-1.0, +1.6] |
| f1_non-motorized_vehicle | -1.4 | [-3.8, +0.9] |
| f1_pedestrian | -0.1 | [-0.8, +0.6] |
| f1_pickup_truck | +1.8 * | [+0.3, +3.2] |
| f1_single_unit_truck | +0.2 | [-1.3, +1.6] |
| f1_work_van | -0.9 | [-2.1, +0.2] |
| recall_articulated_truck | +0.8 | [-0.8, +2.4] |
| recall_background | -0.5 | [-1.2, +0.0] |
| recall_bicycle | +0.6 | [-1.0, +2.3] |
| recall_bus | +1.2 * | [+0.4, +2.1] |
| recall_car | -0.4 | [-1.8, +1.0] |
| recall_motorcycle | -0.7 | [-2.1, +0.6] |
| recall_non-motorized_vehicle | +0.8 | [-2.0, +3.6] |
| recall_pedestrian | +0.7 | [-0.5, +1.9] |
| recall_pickup_truck | +4.8 * | [+2.9, +6.8] |
| recall_single_unit_truck | -3.9 * | [-5.7, -2.3] |
| recall_work_van | +0.0 | [-1.4, +1.4] |

## exp4_l1_90_s0

McNemar (acurácia): p = 2e-14 (só o baseline acerta: 439; só o experimento acerta: 240)

Contraste raras − demais (ΔF1 médio): -1.9 p.p., IC 95% [-3.7, +0.0] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -3.2 * | [-3.9, -2.3] |
| accuracy | -2.9 * | [-3.6, -2.1] |
| f1_articulated_truck | -5.9 * | [-8.0, -3.8] |
| f1_background | -2.4 * | [-3.3, -1.5] |
| f1_bicycle | -4.1 * | [-6.6, -1.8] |
| f1_bus | -2.1 * | [-3.2, -0.9] |
| f1_car | -2.4 * | [-4.2, -0.6] |
| f1_motorcycle | -2.0 | [-4.1, +0.1] |
| f1_non-motorized_vehicle | -7.5 * | [-11.5, -3.2] |
| f1_pedestrian | -2.0 * | [-3.2, -0.9] |
| f1_pickup_truck | +1.6 | [-0.5, +3.7] |
| f1_single_unit_truck | -3.4 * | [-5.5, -1.4] |
| f1_work_van | -4.6 * | [-6.4, -2.9] |
| recall_articulated_truck | -5.4 * | [-8.2, -2.6] |
| recall_background | -3.1 * | [-4.5, -1.7] |
| recall_bicycle | -4.1 * | [-7.1, -1.4] |
| recall_bus | -2.5 * | [-4.2, -0.9] |
| recall_car | -3.9 * | [-6.1, -1.8] |
| recall_motorcycle | -2.7 | [-5.4, +0.0] |
| recall_non-motorized_vehicle | -4.6 | [-9.4, +0.4] |
| recall_pedestrian | -1.7 | [-3.5, +0.0] |
| recall_pickup_truck | +5.9 * | [+2.9, +9.0] |
| recall_single_unit_truck | -4.8 * | [-7.4, -2.6] |
| recall_work_van | -6.6 * | [-9.2, -4.2] |

## exp5_struct_mask_50_s0

McNemar (acurácia): p = 1.3e-25 (só o baseline acerta: 561; só o experimento acerta: 263)

Contraste raras − demais (ΔF1 médio): -0.9 p.p., IC 95% [-3.0, +1.1] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -4.5 * | [-5.3, -3.6] |
| accuracy | -4.3 * | [-5.1, -3.6] |
| f1_articulated_truck | -7.2 * | [-9.5, -5.2] |
| f1_background | -1.8 * | [-2.7, -1.0] |
| f1_bicycle | -5.3 * | [-8.3, -2.5] |
| f1_bus | -3.5 * | [-5.0, -2.2] |
| f1_car | -5.2 * | [-7.3, -3.3] |
| f1_motorcycle | -2.9 * | [-5.5, -0.3] |
| f1_non-motorized_vehicle | -7.2 * | [-11.2, -3.0] |
| f1_pedestrian | -3.5 * | [-5.0, -2.1] |
| f1_pickup_truck | +1.1 | [-1.1, +3.4] |
| f1_single_unit_truck | -4.7 * | [-6.9, -2.6] |
| f1_work_van | -8.8 * | [-10.8, -6.9] |
| recall_articulated_truck | -8.7 * | [-11.8, -5.8] |
| recall_background | -2.1 * | [-3.4, -0.9] |
| recall_bicycle | -5.6 * | [-9.2, -2.1] |
| recall_bus | -5.9 * | [-7.9, -3.9] |
| recall_car | -5.0 * | [-7.6, -2.5] |
| recall_motorcycle | -3.7 * | [-6.9, -0.7] |
| recall_non-motorized_vehicle | -5.0 | [-9.9, +0.0] |
| recall_pedestrian | -1.7 | [-3.7, +0.3] |
| recall_pickup_truck | +4.3 * | [+1.1, +7.5] |
| recall_single_unit_truck | -7.4 * | [-9.9, -4.9] |
| recall_work_van | -7.7 * | [-10.3, -5.1] |

## exp6_struct_phys_50_s0

McNemar (acurácia): p = 1.3e-25 (só o baseline acerta: 561; só o experimento acerta: 263)

Contraste raras − demais (ΔF1 médio): -0.9 p.p., IC 95% [-3.0, +1.1] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -4.5 * | [-5.3, -3.6] |
| accuracy | -4.3 * | [-5.1, -3.6] |
| f1_articulated_truck | -7.2 * | [-9.5, -5.2] |
| f1_background | -1.8 * | [-2.7, -1.0] |
| f1_bicycle | -5.3 * | [-8.3, -2.5] |
| f1_bus | -3.5 * | [-5.0, -2.2] |
| f1_car | -5.2 * | [-7.3, -3.3] |
| f1_motorcycle | -2.9 * | [-5.5, -0.3] |
| f1_non-motorized_vehicle | -7.2 * | [-11.2, -3.0] |
| f1_pedestrian | -3.5 * | [-5.0, -2.1] |
| f1_pickup_truck | +1.1 | [-1.1, +3.4] |
| f1_single_unit_truck | -4.7 * | [-6.9, -2.6] |
| f1_work_van | -8.8 * | [-10.8, -6.9] |
| recall_articulated_truck | -8.7 * | [-11.8, -5.8] |
| recall_background | -2.1 * | [-3.4, -0.9] |
| recall_bicycle | -5.6 * | [-9.2, -2.1] |
| recall_bus | -5.9 * | [-7.9, -3.9] |
| recall_car | -5.0 * | [-7.6, -2.5] |
| recall_motorcycle | -3.7 * | [-6.9, -0.7] |
| recall_non-motorized_vehicle | -5.0 | [-9.9, +0.0] |
| recall_pedestrian | -1.7 | [-3.7, +0.3] |
| recall_pickup_truck | +4.3 * | [+1.1, +7.5] |
| recall_single_unit_truck | -7.4 * | [-9.9, -4.9] |
| recall_work_van | -7.7 * | [-10.3, -5.1] |

