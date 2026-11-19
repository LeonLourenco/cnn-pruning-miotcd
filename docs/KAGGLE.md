# Rodando no Kaggle

Caminho usado pelo Leon para os Exp 1, 5 e 6 (GPU grátis do Kaggle, ~30 h/semana). **Para o Gabriel é opcional:** por padrão ele roda no próprio computador; este guia serve se ele quiser ou precisar de GPU.

O código vem do GitHub; os dados vêm do dataset **privado** `leonloureno/mio-tcd-subset-46k`. Notebook pronto para importar: `notebooks/kaggle_pipeline.ipynb` (*File → Import Notebook*).

**Tempo medido (T4, semente 0):** ~41 s por época; baseline + Exp 5 e 6 completos em 26 min.

## 1. Subir os dados (uma vez)

1. (Já feito pelo Leon.) Em kaggle.com → *Datasets* → *New Dataset*, envie `data/processed/mio_subset.zip` (~330 MB). Visibilidade: **Private**. Nome sugerido: `mio-tcd-subset-46k`.
2. Compartilhe o dataset com a conta do Gabriel (*Settings → Sharing*).
3. O Kaggle extrai o zip: as imagens ficam em `/kaggle/input/mio-tcd-subset-46k/<classe>/<id>.jpg`.

## 2. Acesso ao repositório

Desde 19/11 o repositório é público e o token não é mais necessário (basta `git clone` sem `{tok}@`). Enquanto era privado: crie um token do GitHub com leitura de conteúdo do repositório (*Settings → Developer settings → Fine-grained tokens*, só este repositório, permissão *Contents: Read*). No notebook do Kaggle: *Add-ons → Secrets*, nome `GH_TOKEN`.

## 3. Notebook (Accelerator: GPU; Internet: On)

```python
from kaggle_secrets import UserSecretsClient
tok = UserSecretsClient().get_secret("GH_TOKEN")
!git clone https://{tok}@github.com/LeonLourenco/cnn-pruning-miotcd.git
%cd cnn-pruning-miotcd
!pip install -q torch-pruning==1.6.0
```

Aponte o config para os dados do Kaggle (não commitar esta mudança):

```python
!sed -i 's#img_root: .*#img_root: /kaggle/input/mio-tcd-subset-46k#' configs/default.yaml
!sed -i 's#num_workers: 2#num_workers: 4#' configs/default.yaml
```

Baseline (Exp 1):

```python
!python -m src.train --seed 0
```

Poda estruturada (Exp 5 e 6), depois do baseline:

```python
!python scripts/run_structured.py --seed 0
```

## 4. Guardar os resultados

A pasta `results/` some quando a sessão acaba. Antes de fechar:

```python
!zip -r /kaggle/working/results_s0.zip results
```

Baixe `results_s0.zip` pela aba *Output* e extraia na pasta `results/` do repositório local. Os `.pt` não vão para o Git (`.gitignore`); os `.json` vão.

Para o Gabriel usar o baseline (D-06): publique `results/exp1_baseline_s0/` como outro dataset privado do Kaggle e compartilhe com ele.
