# SPEC — Protocolo experimental

Fonte única de verdade do trabalho. Qualquer mudança aqui vale para os 6 experimentos e precisa ser combinada entre Leon e Gabriel. Os valores numéricos ficam em `configs/default.yaml`; este documento explica o porquê.

**Apresentação:** quinta-feira, 19/11/2026.

## 1. Objetivo

Avaliar como diferentes técnicas e intensidades de pruning afetam uma CNN de classificação num problema real: classificar veículos em imagens de câmeras de tráfego (MIO-TCD). Medimos a relação entre compressão, custo computacional e desempenho preditivo.

**Pergunta central:** o pruning degrada mais as classes raras (bicicleta, moto, não motorizado) do que as frequentes?

**Fora do escopo:** detecção ou contagem de veículos em vídeo; afirmações sobre desempenho em dispositivos embarcados (a latência é medida em CPU de notebook e isso é declarado).

## 2. Experimentos

| Exp | Técnica | Intensidade | Responsável | Nome dos arquivos |
|---|---|---|---|---|
| 1 | Modelo denso (baseline) | 0% | Leon | `exp1_baseline_s<seed>` |
| 2 | L1 não estruturado | 30% | Gabriel | `exp2_l1_30_s<seed>` |
| 3 | L1 não estruturado | 60% | Gabriel | `exp3_l1_60_s<seed>` |
| 4 | L1 não estruturado | 90% | Gabriel | `exp4_l1_90_s<seed>` |
| 5 | Estruturado por canais, máscara | 50% | Leon | `exp5_struct_mask_50_s<seed>` |
| 6 | Estruturado por canais, físico | 50% | Leon | `exp6_struct_phys_50_s<seed>` |

Todos os experimentos de poda partem do checkpoint do Exp 1 **da mesma semente**. Ninguém treina outro baseline.

## 3. Dados

- **Base:** MIO-TCD Classification (Luo et al., IEEE TIP 2018), licença CC BY-NC-SA 4.0.
- **Partição:** `data/splits/split.csv`, gerado por `scripts/prepare_split.py` (semente 42). O teste oficial do MIO-TCD não tem rótulos, então treino/val/teste saem das 519.164 imagens de treino rotuladas. Detalhes da auditoria e da limpeza em `docs/AUDITORIA_DADOS.md`.
- **Amostra:** teto de 5.000 imagens por classe, split 70/15/15 por grupo de quase-duplicatas (pHash/md5), sem vazamento entre splits. Total: 46.006 imagens.
- **Entrada:** 112×112, RGB, normalização do ImageNet. Redimensionamento direto (sem corte central, para não cortar o veículo).
- **Aumento de dados (só treino):** flip horizontal + RandomResizedCrop com escala 0,8–1,0.
- **Desbalanceamento:** sem tratamento (cross-entropy pura). Assim o efeito da poda nas classes raras fica visível.

## 4. Modelo e treino

- ResNet-18 com pesos do ImageNet; `fc` trocada para 11 classes.
- **Baseline:** SGD (momentum 0,9, weight decay 5e-4), LR 0,01 com cosine, batch 128, **20 épocas**.
- **Fine-tuning após a poda (Exp 2–6):** poda única (one-shot) e depois **5 épocas**, LR 0,001 com cosine, mesmo otimizador. A máscara fica fixa durante o fine-tuning.
- **Seleção do checkpoint:** melhor F1-macro na **validação**. O teste é usado uma única vez, na avaliação final.
- **Sementes:** escopo atual = 1 semente (0). Sementes 1 e 2 são a demanda D-04.
- Também se registram as métricas logo após a poda, **antes** do fine-tuning, para mostrar quanto o fine-tuning recupera.

## 5. Poda estruturada (Exp 5 e 6)

- Remove 50% dos canais **em cada camada**, escolhendo os filtros de menor norma L1.
- `conv1` e `fc` ficam fora.
- Os grupos de canais vêm do `torch-pruning` (DepGraph), que junta os canais ligados pelas conexões residuais. Consequência: os canais residuais do `layer1` não são podados (estão ligados à `conv1`, que é ignorada).
- **Exp 5 (máscara):** zera filtros da conv e gamma/beta do BatchNorm dos canais escolhidos. Tensores mantêm o tamanho original.
- **Exp 6 (físico):** remove do modelo do Exp 5 já ajustado **os mesmos canais**. O script confere que as saídas dos dois modelos são idênticas (diferença máxima ≤ 1e-4); se não forem, ele aborta.
- **Atenção na comparação com o L1:** 50% dos canais remove cerca de **74% dos parâmetros** (medido: 11,18 M → 2,86 M), porque entrada e saída de cada conv caem pela metade.

## 6. Poda não estruturada L1 (Exp 2–4)

Critérios a definir pelo Gabriel (demanda D-01). Contrato do código em `src/pruning/unstructured.py`.

## 7. Métricas (todas calculadas por `src/evaluate.py`)

| Dimensão | Métrica | Observação |
|---|---|---|
| Preditiva | **F1-macro** (principal), acurácia, precisão/recall/F1 por classe, matriz de confusão | recall das classes raras é a análise central |
| Compressão | `params_total`, `params_nonzero`, `weight_sparsity` | modelos com máscara têm total igual ao baseline |
| Armazenamento | `size_mb` (state_dict puro), `size_zip_mb` (comprimido) | o zip mostra quanto a esparsidade *poderia* economizar |
| Custo | `macs_measured`, `macs_theoretical` | medido = formato das camadas; teórico = só pesos não nulos |
| Eficiência | latência (mediana, média, desvio, p95) e throughput | só via `scripts/benchmark_latency.py` |

**Resultado esperado a não confundir:** esparsidade não é aceleração. O L1 zera pesos mas mantém tensores densos; sem formato esparso, a latência e os MACs medidos quase não mudam.

## 8. Latência

- Medida **somente no notebook do Leon** (Intel Core i5-1235U, sem GPU dedicada), no **Python nativo do Windows**. Não medir em VM, Colab ou Kaggle (hardware varia entre sessões).
- Notebook na tomada, modo de energia "Melhor desempenho", sem outros programas pesados.
- `torch.set_num_threads(4)`, `eval()` + `inference_mode()`, entrada sintética 112×112.
- Batch 1 (tempo de resposta) e batch 32 (vazão); 50 iterações de aquecimento, 300 medições, divididas em 3 rodadas com ordem alternada dos modelos.
- Reportar a **mediana** como valor principal.
- Pontos ainda em discussão: demanda D-03.

## 9. Hardware

- **Treino:** Kaggle (GPU P100/T4) ou Colab. Gabriel: GPU de entrada do desktop dele (modelo a confirmar, D-02).
- Como o treino roda em máquinas diferentes, tempo de treino **não** é métrica. As comparações de custo usam MACs e parâmetros, que não dependem do hardware.

## 10. Organização e reprodutibilidade

- Cada experimento gera em `results/<exp>/`: `<exp>.pt` (state_dict, só no baseline), `<exp>_model.pt` (modelo inteiro), `<exp>_metrics.json`, `<exp>_history.json` e, quando houver, `<exp>_prefinetune_metrics.json` e `<exp>_plan.json`.
- `scripts/aggregate_results.py` junta tudo em `results/summary.csv` e `results/summary.md`. Ninguém copia números à mão.
- Versões fixadas em `requirements.txt`. Sementes fixadas por `src/utils.set_seed`.

## 11. Limitações a declarar no relatório

- Teste oficial sem rótulos → partição própria.
- Amostra com teto por classe (5.000).
- Quase-duplicatas agrupadas por pHash idêntico, sem ID de câmera.
- Latência em CPU de notebook, não em dispositivo embarcado.
- Poda one-shot com fine-tuning curto (5 épocas); poda iterativa fica fora.
- 1 semente no escopo atual (se D-04 não for feita).
