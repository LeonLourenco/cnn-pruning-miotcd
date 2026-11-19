# Análise estatística — semente 2

Diferença contra `exp1_baseline_s2` no teste (6869 imagens), IC 95% por bootstrap pareado (2000 reamostragens). `*` = intervalo não contém zero.

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

