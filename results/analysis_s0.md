# Análise estatística — semente 0

Diferença contra `exp1_baseline_s0` no teste (6869 imagens), IC 95% por bootstrap pareado (2000 reamostragens). `*` = intervalo não contém zero.

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

