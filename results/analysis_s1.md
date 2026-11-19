# Análise estatística — semente 1

Diferença contra `exp1_baseline_s1` no teste (6869 imagens), IC 95% por bootstrap pareado (2000 reamostragens). `*` = intervalo não contém zero.

## exp2_l1_30_s1

McNemar (acurácia): p = 0.0053 (só o baseline acerta: 43; só o experimento acerta: 74)

Contraste raras − demais (ΔF1 médio): -0.9 p.p., IC 95% [-1.7, -0.2] * (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | +0.3 | [-0.0, +0.7] |
| accuracy | +0.5 * | [+0.1, +0.7] |
| f1_articulated_truck | +0.5 | [-0.2, +1.2] |
| f1_background | +0.1 | [-0.3, +0.4] |
| f1_bicycle | -0.8 | [-2.0, +0.2] |
| f1_bus | +0.1 | [-0.3, +0.5] |
| f1_car | +0.2 | [-0.5, +0.9] |
| f1_motorcycle | +0.0 | [-0.9, +1.0] |
| f1_non-motorized_vehicle | -0.3 | [-1.8, +1.3] |
| f1_pedestrian | -0.1 | [-0.6, +0.3] |
| f1_pickup_truck | +2.7 * | [+1.6, +3.8] |
| f1_single_unit_truck | +1.3 * | [+0.5, +2.2] |
| f1_work_van | -0.0 | [-0.7, +0.6] |
| recall_articulated_truck | +0.4 | [-0.5, +1.4] |
| recall_background | -0.1 | [-0.6, +0.3] |
| recall_bicycle | -1.8 * | [-3.3, -0.6] |
| recall_bus | +0.1 | [-0.5, +0.8] |
| recall_car | +0.4 | [-0.4, +1.2] |
| recall_motorcycle | +0.7 | [-0.7, +2.1] |
| recall_non-motorized_vehicle | -0.4 | [-2.4, +1.6] |
| recall_pedestrian | -0.3 | [-0.8, +0.3] |
| recall_pickup_truck | +4.8 * | [+3.1, +6.5] |
| recall_single_unit_truck | +0.3 | [-0.6, +1.2] |
| recall_work_van | -0.8 | [-1.7, +0.0] |

## exp3_l1_60_s1

McNemar (acurácia): p = 0.032 (só o baseline acerta: 144; só o experimento acerta: 109)

Contraste raras − demais (ΔF1 médio): -1.0 p.p., IC 95% [-2.1, -0.0] * (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -0.6 * | [-1.1, -0.1] |
| accuracy | -0.5 * | [-0.9, -0.0] |
| f1_articulated_truck | -0.9 | [-2.2, +0.3] |
| f1_background | -0.1 | [-0.6, +0.5] |
| f1_bicycle | -1.9 * | [-3.6, -0.4] |
| f1_bus | -0.3 | [-1.1, +0.5] |
| f1_car | -0.7 | [-1.8, +0.4] |
| f1_motorcycle | +0.4 | [-0.8, +1.5] |
| f1_non-motorized_vehicle | -2.6 * | [-4.8, -0.3] |
| f1_pedestrian | -0.9 * | [-1.6, -0.3] |
| f1_pickup_truck | +1.3 | [-0.1, +2.7] |
| f1_single_unit_truck | -0.6 | [-1.8, +0.7] |
| f1_work_van | -0.5 | [-1.7, +0.6] |
| recall_articulated_truck | +1.1 | [-0.6, +2.8] |
| recall_background | -0.9 * | [-1.8, -0.3] |
| recall_bicycle | -4.4 * | [-6.7, -2.3] |
| recall_bus | -0.9 | [-2.1, +0.1] |
| recall_car | -0.7 | [-2.0, +0.7] |
| recall_motorcycle | +0.7 | [-0.9, +2.3] |
| recall_non-motorized_vehicle | -1.9 | [-4.6, +0.7] |
| recall_pedestrian | -0.4 | [-1.2, +0.4] |
| recall_pickup_truck | +3.2 * | [+1.3, +5.1] |
| recall_single_unit_truck | -1.2 | [-2.6, +0.1] |
| recall_work_van | -2.4 * | [-4.0, -0.9] |

## exp4_l1_90_s1

McNemar (acurácia): p = 7.8e-28 (só o baseline acerta: 484; só o experimento acerta: 201)

Contraste raras − demais (ΔF1 médio): -0.1 p.p., IC 95% [-2.0, +1.8] (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -4.1 * | [-4.9, -3.3] |
| accuracy | -4.1 * | [-4.8, -3.4] |
| f1_articulated_truck | -3.4 * | [-5.2, -1.5] |
| f1_background | -0.8 * | [-1.7, -0.1] |
| f1_bicycle | -4.0 * | [-6.4, -1.7] |
| f1_bus | -2.3 * | [-3.6, -1.1] |
| f1_car | -3.0 * | [-4.7, -1.2] |
| f1_motorcycle | -2.4 * | [-4.8, -0.1] |
| f1_non-motorized_vehicle | -6.1 * | [-10.0, -2.3] |
| f1_pedestrian | -2.1 * | [-3.3, -1.0] |
| f1_pickup_truck | -10.7 * | [-13.1, -8.4] |
| f1_single_unit_truck | -7.2 * | [-9.1, -5.2] |
| f1_work_van | -3.3 * | [-5.1, -1.6] |
| recall_articulated_truck | -1.1 | [-3.6, +1.3] |
| recall_background | -2.4 * | [-3.7, -1.3] |
| recall_bicycle | -7.9 * | [-11.0, -4.7] |
| recall_bus | -2.5 * | [-4.3, -0.9] |
| recall_car | -4.3 * | [-6.5, -2.2] |
| recall_motorcycle | +0.0 | [-2.8, +2.8] |
| recall_non-motorized_vehicle | -3.8 | [-8.5, +0.8] |
| recall_pedestrian | -2.4 * | [-4.1, -0.8] |
| recall_pickup_truck | -12.2 * | [-15.5, -9.0] |
| recall_single_unit_truck | -4.0 * | [-6.2, -1.8] |
| recall_work_van | -4.0 * | [-6.4, -1.7] |

## exp5_struct_mask_50_s1

McNemar (acurácia): p = 2.9e-25 (só o baseline acerta: 567; só o experimento acerta: 269)

Contraste raras − demais (ΔF1 médio): -2.4 p.p., IC 95% [-4.5, -0.3] * (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -4.7 * | [-5.6, -3.8] |
| accuracy | -4.3 * | [-5.2, -3.5] |
| f1_articulated_truck | -5.0 * | [-7.2, -2.9] |
| f1_background | -2.3 * | [-3.4, -1.3] |
| f1_bicycle | -6.3 * | [-9.2, -3.7] |
| f1_bus | -2.7 * | [-4.2, -1.3] |
| f1_car | -5.5 * | [-7.4, -3.7] |
| f1_motorcycle | -3.5 * | [-5.9, -1.2] |
| f1_non-motorized_vehicle | -9.5 * | [-14.1, -4.9] |
| f1_pedestrian | -3.7 * | [-5.2, -2.4] |
| f1_pickup_truck | -3.2 * | [-5.8, -0.9] |
| f1_single_unit_truck | -2.9 * | [-5.2, -0.5] |
| f1_work_van | -6.9 * | [-8.9, -4.9] |
| recall_articulated_truck | -2.8 | [-5.6, +0.0] |
| recall_background | -3.3 * | [-4.9, -1.9] |
| recall_bicycle | -10.3 * | [-13.9, -7.0] |
| recall_bus | -4.8 * | [-6.9, -2.8] |
| recall_car | -4.8 * | [-7.3, -2.4] |
| recall_motorcycle | -2.7 | [-5.6, +0.3] |
| recall_non-motorized_vehicle | -8.1 * | [-14.0, -2.4] |
| recall_pedestrian | -2.4 * | [-4.4, -0.4] |
| recall_pickup_truck | -2.5 | [-5.9, +0.7] |
| recall_single_unit_truck | -5.9 * | [-8.9, -3.2] |
| recall_work_van | -4.7 * | [-7.2, -2.3] |

## exp6_struct_phys_50_s1

McNemar (acurácia): p = 2.9e-25 (só o baseline acerta: 567; só o experimento acerta: 269)

Contraste raras − demais (ΔF1 médio): -2.4 p.p., IC 95% [-4.5, -0.3] * (negativo = raras perdem mais)

| métrica | Δ (p.p.) | IC 95% |
|---|---:|---|
| f1_macro | -4.7 * | [-5.6, -3.8] |
| accuracy | -4.3 * | [-5.2, -3.5] |
| f1_articulated_truck | -5.0 * | [-7.2, -2.9] |
| f1_background | -2.3 * | [-3.4, -1.3] |
| f1_bicycle | -6.3 * | [-9.2, -3.7] |
| f1_bus | -2.7 * | [-4.2, -1.3] |
| f1_car | -5.5 * | [-7.4, -3.7] |
| f1_motorcycle | -3.5 * | [-5.9, -1.2] |
| f1_non-motorized_vehicle | -9.5 * | [-14.1, -4.9] |
| f1_pedestrian | -3.7 * | [-5.2, -2.4] |
| f1_pickup_truck | -3.2 * | [-5.8, -0.9] |
| f1_single_unit_truck | -2.9 * | [-5.2, -0.5] |
| f1_work_van | -6.9 * | [-8.9, -4.9] |
| recall_articulated_truck | -2.8 | [-5.6, +0.0] |
| recall_background | -3.3 * | [-4.9, -1.9] |
| recall_bicycle | -10.3 * | [-13.9, -7.0] |
| recall_bus | -4.8 * | [-6.9, -2.8] |
| recall_car | -4.8 * | [-7.3, -2.4] |
| recall_motorcycle | -2.7 | [-5.6, +0.3] |
| recall_non-motorized_vehicle | -8.1 * | [-14.0, -2.4] |
| recall_pedestrian | -2.4 * | [-4.4, -0.4] |
| recall_pickup_truck | -2.5 | [-5.9, +0.7] |
| recall_single_unit_truck | -5.9 * | [-8.9, -3.2] |
| recall_work_van | -4.7 * | [-7.2, -2.3] |

