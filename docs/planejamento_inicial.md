# Pruning em CNNs com MIO-TCD — Resumo e Planejamento

Nov 12, 2026 · @Leon

## 1. Objetivo e escopo

Avaliar como diferentes técnicas e intensidades de pruning afetam uma CNN de classificação em um problema real: classificar veículos em imagens de câmeras de tráfego (MIO-TCD). O que se mede é a relação entre compressão (parâmetros, esparsidade, MB, MACs), eficiência (latência, throughput, memória) e desempenho preditivo (F1-macro, recall por classe).

- **Modelo:** somente CNN — ResNet-18, uma única arquitetura.
- **Tarefa:** classificação multiclasse de recortes (11 classes). Não inclui detecção nem contagem em vídeo.
- **Motivação:** trabalho acadêmico para praticar as técnicas da disciplina. Não afirmamos desempenho em Edge AI; a latência é medida em ambiente convencional e isso é declarado.
- **Pergunta científica central:** o pruning degrada mais as classes raras (bicicleta, moto, não motorizado) do que as frequentes?

| Exp | Técnica | Intensidade | Responsável |
| --- | --- | --- | --- |
| 1 | Modelo denso (baseline) | 0% | Leon |
| 2 | Não estruturado L1 | 30% | Amigo |
| 3 | Não estruturado L1 | 60% | Amigo |
| 4 | Não estruturado L1 | 90% | Amigo |
| 5 | Estruturado por canais, com máscara | 50% | Leon |
| 6 | Estruturado físico (remoção real de canais) | 50% | Leon |

## 2. O que já foi feito: escolha da base

O feedback do Valmir pedia trocar o CIFAR-10 por uma base ligada a um problema real. Baixamos e auditamos as candidatas: integridade dos arquivos, resolução, balanceamento, duplicatas exatas (md5) e quase-duplicatas (pHash) entre treino e teste.

| Base | Resultado da auditoria | Decisão |
| --- | --- | --- |
| **MIO-TCD Classification** (original) | Tar íntegro: 648.959 imagens, 0 corrompidas, rótulos 100% consistentes com `gt_train.csv`. Teste oficial **sem rótulos**. Desbalanceamento de 149:1. 1.048 duplicatas exatas e 4% do treino em grupos de quase-duplicatas. | **Escolhida** |
| GTSRB | Íntegra (51.839 imagens), teste oficial rotulado. Treino tem 1.307 trilhas de \~30 quadros da mesma placa (vazamento se a validação for aleatória). Acurácia perto do teto (\~99%). | Plano B |
| EuroSAT (RGB) | Mais limpa e balanceada, mas 64×64 px e sem split oficial. | Descartada |
| PlantDoc | 9 imagens idênticas com rótulos diferentes entre treino e teste; uma classe com 2 imagens; só 2,6 mil imagens. | Descartada |
| Kaggle "MIO-TCD 50k" | Subconjunto de terceiro sem documentação de amostragem nem licença. | Descartada |
| Kaggle "cardetection" (Roboflow) | É detecção (YOLO), não classificação. \~40% são imagens do GTSRB esticadas para 416 px. Vazamento entre splits (206 de 314 trilhas espalhadas). | Descartada |

**Por que o MIO-TCD:** problema real (monitoramento de tráfego), volume grande, licença clara (CC BY-NC-SA 4.0, citar Luo et al., IEEE TIP 2018) e um desbalanceamento real que torna a análise por classe após a poda uma pergunta relevante.

## 3. Preparação do MIO-TCD (concluída)

Como o teste oficial não tem rótulos, treino, validação e teste saem das 519.164 imagens de treino rotuladas.

**Limpeza:**

- Imagens que são duplicatas exatas (md5) ou quase-duplicatas (pHash idêntico) foram agrupadas.
- Removidas 1.663 imagens de grupos com rótulos conflitantes (ex.: a mesma imagem como car e pickup\_truck).
- Duplicatas exatas reduzidas a uma cópia (1.041 removidas).
- Cada grupo vai inteiro para um único split. Verificado: nenhum grupo em mais de um split.

**Amostra:** teto de 5.000 imagens por classe (as menores entram inteiras), split 70/15/15 por classe, semente 42. Total de 46.006 imagens.

| Classe | Treino | Val | Teste |
| --- | --: | --: | --: |
| articulated\_truck, background, bus, car, pedestrian, pickup\_truck, single\_unit\_truck, work\_van (cada) | 3.500 | 750 | 750 |
| bicycle | 1.599 | 342 | 342 |
| motorcycle | 1.383 | 296 | 296 |
| non-motorized\_vehicle | 1.224 | 262 | 262 |

**Resolução de entrada definida: 112×112.** Metade das imagens tem lado menor que 72 px, e 224 px seria ampliar a maioria em 3x ou mais, com \~4x mais custo.

**Arquivos na pasta `cnn-pruning`:**

- `prepare_split.py`: limpeza e split, reprodutível com `--seed 42`.
- `split.csv`: id, classe, split, grupo, largura, altura — a partição oficial do trabalho, usada pelos dois.
- `features.tsv`: cache de md5/pHash/dimensões (acelera rodar o script de novo).
- `MIO-TCD-Classification.tar`: dados originais, não extraídos; o loader pode ler direto do tar.

## 4. Divisão de trabalho

- **Leon:** Exp 1 (baseline), Exp 5 (estruturado com máscara) e Exp 6 (estruturado físico).
- **Amigo:** Exp 2, 3 e 4 (L1 não estruturado em 30%, 60% e 90%).

**Dependências:**

1. **O baseline vem primeiro.** Todos os experimentos de poda partem do mesmo checkpoint denso treinado pelo Leon. Ninguém treina outro baseline.
2. **Exp 5 e Exp 6 usam os mesmos canais.** Seleciona-se 50% dos canais, aplica-se a máscara e faz-se o fine-tuning (Exp 5); depois os mesmos canais são removidos fisicamente do modelo ajustado (Exp 6). A acurácia dos dois deve ser praticamente igual, e a diferença em MB, MACs e latência isola o efeito da remoção física.
3. **A latência é medida por uma pessoa só, numa máquina só**, para os 6 modelos.

**Esforço:** a parte estruturada física é a mais trabalhosa por causa das conexões residuais da ResNet-18 (os canais somados precisam continuar compatíveis). Biblioteca sugerida: `torch-pruning` (DepGraph). A L1 não estruturada usa `torch.nn.utils.prune`.

## 5. Protocolo comum (fechar antes de treinar)

Tudo abaixo é igual para os 6 experimentos. Valores marcados como *proposta* ainda precisam ser confirmados pelos dois.

**Código e ambiente**

- Um repositório único com `data.py` (loader), `train.py` (treino e fine-tuning), `evaluate.py` (métricas) e um arquivo de configuração. Cada um implementa só a sua função de poda.
- Mesmas versões de Python, PyTorch e bibliotecas (fixadas num `requirements.txt`).
- Sementes fixas (Python, NumPy, PyTorch) e `split.csv` como única fonte da partição.

**Dados**

- Entrada 112×112, conversão para RGB, normalização do ImageNet.
- Augmentation só no treino: *proposta* — flip horizontal e pequeno crop/escala aleatórios.
- Tratamento do desbalanceamento: **decidido** — cross-entropy sem pesos nem sampler, mantendo o desbalanceamento natural da amostra. Assim o efeito da poda nas classes raras fica visível.

**Treino do baseline (Exp 1)**

- **Decidido:** ResNet-18 com pesos do ImageNet, última camada trocada para 11 classes.
- **Decidido:** 3 sementes por experimento (ex.: 0, 1, 2); resultados reportados como média ± desvio. Cada semente do baseline gera o seu checkpoint, e cada fine-tuning parte do baseline da mesma semente.
- *Proposta:* SGD com momentum 0,9, LR 0,01 com cosine, weight decay 5e-4, batch 128, 30 épocas.
- Checkpoint escolhido pelo melhor F1-macro na validação.

**Fine-tuning após a poda (Exp 2–6)**

- *Proposta:* mesmo número de épocas para todos (ex.: 10), LR inicial 0,001 com cosine, mesmo otimizador.
- Também registrar as métricas logo após a poda, antes do fine-tuning: mostra quanto o fine-tuning recupera.

**Avaliação (um único `evaluate.py`, no conjunto de teste)**

| Dimensão | Métricas |
| --- | --- |
| Preditiva | F1-macro (principal), recall e precisão por classe, acurácia, matriz de confusão |
| Compressão | parâmetros totais, parâmetros não nulos, % de esparsidade |
| Armazenamento | MB do `state_dict` denso e MB comprimido (zip) — mostra quando a esparsidade vira economia real |
| Custo | MACs/FLOPs (ex.: `thop` ou `fvcore`) |
| Eficiência | latência média e desvio (ms), throughput (img/s), pico de memória |

**Hardware (decidido para o Leon; em aberto para o amigo)**

- O notebook do Leon (Intel Core i5-1235U, só GPU integrada Iris Xe, sem CUDA) não serve para treinar.
- Treino e fine-tuning do Leon: Kaggle (P100/T4, ~30 h de GPU por semana, dataset fica salvo entre sessões) ou Colab, conforme a necessidade.
- Hardware de treino do amigo: em aberto (desktop dele, a confirmar se tem GPU NVIDIA).
- **Latência, throughput e memória dos 6 modelos: todos medidos no notebook do Leon, em CPU.** É a única máquina fixa e controlada; a GPU do Colab/Kaggle varia entre sessões.
- Como o treino roda em máquinas diferentes, as comparações de custo usam MACs e parâmetros (independentes de hardware); tempo de treino não é métrica do trabalho.

**Medição de latência:** notebook do Leon (i5-1235U, CPU), batch 1 e batch 32, 50 iterações de warm-up, 300 medições, número de threads fixo, carregador na tomada, sem outros processos pesados. Hardware informado no relatório.

**Resultado esperado a não confundir:** o L1 não estruturado zera pesos mas mantém tensores densos, então sem formato esparso não reduz latência nem MACs efetivos. Isso é um achado a reportar, não um erro.

## 6. Planejamento do início ao fim

| Fase | O que fazer | Quem | Entregável | Depende de |
| --- | --- | --- | --- | --- |
| 0. Alinhamento | Ler este documento, fechar as propostas da seção 5 e as decisões da seção 7 | Ambos | Protocolo assinado | — |
| 1. Base de código | Repositório, `data.py` lendo o tar + `split.csv`, `evaluate.py`, config, requirements | Leon (loader) e amigo (avaliação) | Repo rodando ponta a ponta com um treino curto | Fase 0 |
| 2. Baseline | Treinar Exp 1 e avaliar | Leon | `baseline.pt` + métricas | Fase 1 |
| 3a. L1 não estruturado | Podar 30/60/90% a partir do `baseline.pt`, avaliar antes e depois do fine-tuning | Amigo | 3 checkpoints + métricas | Fase 2 |
| 3b. Estruturado | Selecionar 50% dos canais, máscara + fine-tuning (Exp 5), remoção física dos mesmos canais (Exp 6) | Leon | 2 checkpoints + métricas | Fase 2 |
| 4. Medição padronizada | Rodar `evaluate.py` e o benchmark de latência nos 6 modelos no notebook do Leon (CPU) | Leon | Tabela única de resultados | Fases 3a e 3b |
| 5. Análise | Gráficos de compressão × F1-macro, recall por classe × nível de poda, latência × MB; discutir esparsidade vs. aceleração real | Ambos | Figuras e tabelas | Fase 4 |
| 6. Escrita e apresentação | Introdução, base de dados e auditoria, metodologia, resultados, limitações, conclusão | Ambos | Relatório + slides | Fase 5 |

**Checklist por experimento:** checkpoint salvo, configuração usada, semente, métricas em JSON, matriz de confusão e log de treino. Tudo no repositório, com o mesmo padrão de nome (ex.: `exp3_l1_60.pt`, `exp3_l1_60_metrics.json`).

**Limitações a declarar no relatório:** teste oficial sem rótulos (partição própria); amostra com teto por classe; latência medida em CPU de notebook (i5-1235U), não em dispositivo embarcado; agrupamento de quase-duplicatas por pHash idêntico, sem ID de câmera.

## 7. Decisões em aberto

- [ ] Hiperparâmetros do baseline e do fine-tuning (confirmar ou ajustar a proposta da seção 5).
- [x] Pesos do ImageNet no baseline: **sim**.
- [x] Desbalanceamento: **sem tratamento** (cross-entropy pura).
- [ ] L1 não estruturado: poda global ou por camada? Podar a primeira conv e a camada final ou não?
- [ ] Estruturado: 50% em cada camada ou global? Quais camadas ficam de fora (primeira conv, fc)?
- [x] Sementes: **3 por experimento**, média ± desvio.
- [x] Hardware do Leon: treino no Kaggle/Colab; latência dos 6 modelos no notebook do Leon (CPU).
- [ ] Hardware de treino do amigo (desktop dele: confirmar GPU).
- [ ] Prazos de cada fase.
