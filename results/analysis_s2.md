# Análise estatística — semente 2

Diferença contra `exp1_baseline_s2` no teste (6869 imagens), IC 95% por bootstrap pareado (2000 reamostragens). `*` = intervalo não contém zero.

## exp2_l1_30_s2

McNemar (acurácia): p = 0.76 (só o baseline acerta: 91; só o experimento acerta: 86)

Contraste raras − demais (ΔF1 médio): +0.3 p.p., IC 95% [-0.8, +1.3] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -0.0 | [-0.5, +0.4] |
| accuracy | -0.1 | [-0.5, +0.3] |
| f1_articulated_truck | -0.6 | [-1.4, +0.3] |
| f1_background | +0.1 | [-0.2, +0.5] |
| f1_bicycle | +0.4 | [-0.9, +1.7] |
| f1_bus | -0.2 | [-0.8, +0.4] |
| f1_car | +0.0 | [-1.0, +1.1] |
| f1_motorcycle | +0.3 | [-1.0, +1.7] |
| f1_non-motorized_vehicle | -0.2 | [-2.4, +2.0] |
| f1_pedestrian | +0.2 | [-0.2, +0.8] |
| f1_pickup_truck | +0.3 | [-0.7, +1.4] |
| f1_single_unit_truck | -0.7 | [-1.8, +0.5] |
| f1_work_van | -0.1 | [-1.0, +0.9] |
| recall_articulated_truck | -2.0 * | [-3.3, -0.9] |
| recall_background | +0.5 * | [+0.1, +1.1] |
| recall_bicycle | +0.9 | [-0.6, +2.4] |
| recall_bus | -0.5 | [-1.5, +0.4] |
| recall_car | +2.4 * | [+1.1, +3.9] |
| recall_motorcycle | +0.3 | [-1.6, +2.3] |
| recall_non-motorized_vehicle | -0.8 | [-3.7, +2.2] |
| recall_pedestrian | -0.1 | [-0.9, +0.7] |
| recall_pickup_truck | -1.1 | [-2.5, +0.4] |
| recall_single_unit_truck | +1.6 * | [+0.4, +3.0] |
| recall_work_van | -1.7 * | [-2.9, -0.6] |

## exp3_l1_60_s2

McNemar (acurácia): p = 0.0079 (só o baseline acerta: 167; só o experimento acerta: 121)

Contraste raras − demais (ΔF1 médio): +1.6 p.p., IC 95% [+0.4, +2.8] * (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -0.5 | [-1.0, +0.1] |
| accuracy | -0.7 * | [-1.2, -0.2] |
| f1_articulated_truck | -1.0 | [-2.1, +0.1] |
| f1_background | -0.1 | [-0.5, +0.4] |
| f1_bicycle | +0.7 | [-0.5, +2.0] |
| f1_bus | -0.0 | [-0.7, +0.7] |
| f1_car | -0.3 | [-1.6, +1.0] |
| f1_motorcycle | +0.5 | [-0.9, +1.9] |
| f1_non-motorized_vehicle | +1.0 | [-1.7, +3.6] |
| f1_pedestrian | +0.4 | [-0.2, +1.1] |
| f1_pickup_truck | -3.6 * | [-5.1, -1.9] |
| f1_single_unit_truck | -1.4 * | [-2.7, -0.0] |
| f1_work_van | -1.3 | [-2.6, +0.1] |
| recall_articulated_truck | -2.3 * | [-3.8, -0.8] |
| recall_background | +0.3 | [-0.4, +1.0] |
| recall_bicycle | -0.3 | [-1.7, +1.2] |
| recall_bus | -0.1 | [-1.1, +0.9] |
| recall_car | +3.7 * | [+2.0, +5.5] |
| recall_motorcycle | +0.7 | [-1.1, +2.7] |
| recall_non-motorized_vehicle | +0.8 | [-2.4, +4.2] |
| recall_pedestrian | +0.8 | [-0.1, +1.8] |
| recall_pickup_truck | -8.6 * | [-10.8, -6.3] |
| recall_single_unit_truck | +1.5 | [+0.0, +2.9] |
| recall_work_van | -1.9 * | [-3.4, -0.4] |

## exp4_l1_90_s2

McNemar (acurácia): p = 8.4e-44 (só o baseline acerta: 584; só o experimento acerta: 202)

Contraste raras − demais (ΔF1 médio): +2.1 p.p., IC 95% [+0.2, +4.0] * (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -5.3 * | [-6.1, -4.5] |
| accuracy | -5.6 * | [-6.4, -4.8] |
| f1_articulated_truck | -3.8 * | [-5.7, -2.0] |
| f1_background | -1.6 * | [-2.4, -0.8] |
| f1_bicycle | -3.7 * | [-6.2, -1.4] |
| f1_bus | -1.7 * | [-2.7, -0.6] |
| f1_car | -2.1 * | [-3.8, -0.4] |
| f1_motorcycle | -1.7 | [-3.8, +0.3] |
| f1_non-motorized_vehicle | -5.8 * | [-10.1, -2.0] |
| f1_pedestrian | -1.9 * | [-3.2, -0.7] |
| f1_pickup_truck | -19.9 * | [-22.9, -16.9] |
| f1_single_unit_truck | -12.9 * | [-15.2, -10.9] |
| f1_work_van | -3.2 * | [-5.0, -1.3] |
| recall_articulated_truck | -5.0 * | [-7.6, -2.6] |
| recall_background | -1.6 * | [-2.8, -0.5] |
| recall_bicycle | -5.3 * | [-8.1, -2.5] |
| recall_bus | -2.1 * | [-3.7, -0.6] |
| recall_car | -0.1 | [-2.4, +2.3] |
| recall_motorcycle | -0.3 | [-2.9, +2.3] |
| recall_non-motorized_vehicle | -7.3 * | [-12.5, -2.5] |
| recall_pedestrian | -2.0 * | [-3.9, -0.1] |
| recall_pickup_truck | -28.7 * | [-32.4, -24.9] |
| recall_single_unit_truck | +0.0 | [-2.3, +2.2] |
| recall_work_van | -6.6 * | [-8.9, -4.2] |

## exp5_struct_mask_50_s2

McNemar (acurácia): p = 7.6e-54 (só o baseline acerta: 711; só o experimento acerta: 243)

Contraste raras − demais (ΔF1 médio): +1.1 p.p., IC 95% [-0.9, +3.2] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -6.7 * | [-7.7, -5.8] |
| accuracy | -6.8 * | [-7.7, -6.0] |
| f1_articulated_truck | -14.9 * | [-17.4, -12.3] |
| f1_background | -1.9 * | [-3.0, -0.9] |
| f1_bicycle | -4.8 * | [-7.6, -2.1] |
| f1_bus | -3.9 * | [-5.3, -2.5] |
| f1_car | -4.6 * | [-6.7, -2.6] |
| f1_motorcycle | -4.5 * | [-6.8, -2.2] |
| f1_non-motorized_vehicle | -8.5 * | [-13.2, -3.8] |
| f1_pedestrian | -2.5 * | [-3.9, -1.2] |
| f1_pickup_truck | -12.0 * | [-14.8, -9.3] |
| f1_single_unit_truck | -8.8 * | [-11.2, -6.6] |
| f1_work_van | -7.7 * | [-9.9, -5.6] |
| recall_articulated_truck | -18.0 * | [-21.4, -14.8] |
| recall_background | -2.3 * | [-3.8, -0.8] |
| recall_bicycle | -7.3 * | [-11.0, -4.0] |
| recall_bus | -5.7 * | [-7.7, -3.8] |
| recall_car | -0.4 | [-3.0, +2.2] |
| recall_motorcycle | -1.7 | [-4.1, +0.6] |
| recall_non-motorized_vehicle | -10.0 * | [-15.6, -4.3] |
| recall_pedestrian | -1.5 | [-3.4, +0.4] |
| recall_pickup_truck | -18.5 * | [-22.1, -14.8] |
| recall_single_unit_truck | -2.7 * | [-5.4, -0.1] |
| recall_work_van | -6.2 * | [-8.9, -3.6] |

## exp6_struct_phys_50_s2

McNemar (acurácia): p = 7.6e-54 (só o baseline acerta: 711; só o experimento acerta: 243)

Contraste raras − demais (ΔF1 médio): +1.1 p.p., IC 95% [-0.9, +3.2] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -6.7 * | [-7.7, -5.8] |
| accuracy | -6.8 * | [-7.7, -6.0] |
| f1_articulated_truck | -14.9 * | [-17.4, -12.3] |
| f1_background | -1.9 * | [-3.0, -0.9] |
| f1_bicycle | -4.8 * | [-7.6, -2.1] |
| f1_bus | -3.9 * | [-5.3, -2.5] |
| f1_car | -4.6 * | [-6.7, -2.6] |
| f1_motorcycle | -4.5 * | [-6.8, -2.2] |
| f1_non-motorized_vehicle | -8.5 * | [-13.2, -3.8] |
| f1_pedestrian | -2.5 * | [-3.9, -1.2] |
| f1_pickup_truck | -12.0 * | [-14.8, -9.3] |
| f1_single_unit_truck | -8.8 * | [-11.2, -6.6] |
| f1_work_van | -7.7 * | [-9.9, -5.6] |
| recall_articulated_truck | -18.0 * | [-21.4, -14.8] |
| recall_background | -2.3 * | [-3.8, -0.8] |
| recall_bicycle | -7.3 * | [-11.0, -4.0] |
| recall_bus | -5.7 * | [-7.7, -3.8] |
| recall_car | -0.4 | [-3.0, +2.2] |
| recall_motorcycle | -1.7 | [-4.1, +0.6] |
| recall_non-motorized_vehicle | -10.0 * | [-15.6, -4.3] |
| recall_pedestrian | -1.5 | [-3.4, +0.4] |
| recall_pickup_truck | -18.5 * | [-22.1, -14.8] |
| recall_single_unit_truck | -2.7 * | [-5.4, -0.1] |
| recall_work_van | -6.2 * | [-8.9, -3.6] |

