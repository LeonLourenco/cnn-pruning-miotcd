# Análise estatística — semente 1

Diferença contra `exp1_baseline_s1` no teste (6869 imagens), IC 95% por bootstrap pareado (2000 reamostragens). `*` = intervalo não contém zero.

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

