# Rodando os Exp 2–4 no próprio computador

Guia para o Gabriel (ou quem rodar fora do Kaggle). Protocolo completo em `docs/SPEC.md`; pendências em `docs/DEMANDAS.md`.

## 1. Preparar o ambiente

```bash
git clone https://github.com/LeonLourenco/cnn-pruning-miotcd.git
cd cnn-pruning-miotcd
pip install -r requirements.txt
```

Com GPU NVIDIA, instale antes o PyTorch com CUDA pelo seletor de https://pytorch.org (o `requirements.txt` aceita qualquer versão a partir da 2.3). Anote o modelo da GPU e a versão do PyTorch na demanda D-02.

## 2. Baixar os arquivos grandes (Release do GitHub)

Na página do repositório: **Releases → "Dados e baseline (semente 0) para os Exp 2-4"** (tag `dados-baseline-s0`). Baixe os dois anexos. **Atenção:** o baseline precisa ser o treinado no split v2 (demanda D-06); confira a data do anexo na Release.

| Arquivo | Onde colocar |
|---|---|
| `exp1_baseline_s0.pt` (~43 MB) | `results/exp1_baseline_s0/exp1_baseline_s0.pt` |
| `mio_subset.zip` (~330 MB) | extrair em `data/processed/mio_subset/` (deve ficar `data/processed/mio_subset/<classe>/<id>.jpg`, 11 pastas) |

Com o GitHub CLI: `gh release download dados-baseline-s0 -R LeonLourenco/cnn-pruning-miotcd`.

Nenhum dos dois vai para o Git (`.gitignore`). Não altere `data/splits/split.csv`.

## 3. Conferir dados e pipeline (obrigatório)

```bash
python scripts/audit_data.py --img-root data/processed/mio_subset   # 10 verificações, todas devem dar ok
python -m pytest                                                     # 27 testes
```

O split atual é o **v2** (45.788 imagens; ver `docs/AUDITORIA_DADOS.md`). O zip de imagens é o mesmo do v1 — as 218 imagens a mais no zip são ignoradas. Se a auditoria ou algum teste falhar, não treine: avise o Leon.

## 4. Implementar e rodar a poda L1 (D-01 e D-09)

1. Decida e registre os critérios (global ou por camada; camadas excluídas) em `configs/default.yaml` (seção `unstructured`) e em `docs/SPEC.md` (seção 6).
2. Implemente `src/pruning/unstructured.py` seguindo o contrato descrito no próprio arquivo, e um script `scripts/run_unstructured.py` no molde de `scripts/run_structured.py`: carregar o baseline da mesma semente → podar → avaliar antes do fine-tuning → fine-tuning com `src.train.fit(..., after_step=mask_hook(plan))` → avaliar com `src.evaluate.evaluate_model(..., pred_path=...)` gravando `<exp>_predictions_test.csv` (necessário para `scripts/analyze_results.py`) → salvar.
3. Use **sempre** os hiperparâmetros de `configs/default.yaml` (fine-tuning de **10 épocas**, motivo em `docs/SPEC.md`, seção 4) e os nomes `exp2_l1_30_s0`, `exp3_l1_60_s0`, `exp4_l1_90_s0`.
4. Teste primeiro com `configs/smoke.yaml`.

Referência de tempo: na T4 do Kaggle, cada época leva ~41 s; um experimento de poda com 10 épocas, ~8 min. Numa GPU de entrada pode levar de 2 a 4 vezes mais. Sem GPU não é viável — nesse caso use `notebooks/kaggle_pipeline.ipynb` (`docs/KAGGLE.md`).

## 5. Entregar os resultados

- Commit dos JSON (`results/exp{2,3,4}_*/*.json`) e do código, no padrão de commits do repositório. Os `.pt` não vão para o Git.
- Envie ao Leon os três `*_model.pt` para a medição de latência (D-08), que é feita só no notebook dele. Sugestão: anexá-los a uma nova Release (`modelos-l1-s0`).
