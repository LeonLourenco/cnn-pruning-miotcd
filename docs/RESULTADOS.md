# Resultados

**Estado (18/11):** resultados do split v1 **descartados** (vazamento de quase-duplicatas, ver `docs/AUDITORIA_DADOS.md`). Exp 1, 5 e 6 sendo refeitos com o split v2. Esta página é preenchida a partir de `results/summary.md` e `results/analysis_s0.md`, gerados pelos scripts — nenhum número é digitado à mão.

## Lições da rodada com o split v1 (registro de processo)

Os números abaixo **não valem como resultado**; ficam só como histórico do que motivou as correções.

- Baseline 0,896 de F1-macro; Exp 5/6 0,821 (fine-tuning de 5 épocas) e 0,840 (10 épocas). A curva de validação ainda subia com 5 épocas → protocolo mudou para 10 (`docs/SPEC.md`, seção 4).
- A primeira leitura ("as classes raras não sofreram mais") estava errada em três pontos:
  1. **Usava só o recall.** A moto perdia 1,7 p.p. de recall mas 7,6 p.p. de precisão; pelo F1, "não motorizado" tinha a 2ª maior queda.
  2. **Ignorava a incerteza.** Com 262–342 imagens de teste, as quedas das classes raras tinham margem de ±3 a ±8 p.p.: não distinguíveis de zero.
  3. **O teste tinha vazamento:** 9,3% das imagens de teste com quase-cópia no treino.
- O que parecia robusto e será reavaliado no v2: os erros que mais cresceram foram entre classes de veículos parecidos (caminhão articulado → caminhão simples: 84 → 147), e a queda tendia a ser maior nas classes que o baseline já errava mais (correlação 0,49). Hipótese: a poda tira primeiro a capacidade de distinções finas.

## Como ler os resultados do v2

- Métrica principal: F1-macro. Por classe: **F1** (recall e precisão juntos).
- Uma diferença só é afirmada quando o IC 95% do bootstrap pareado não contém zero (`results/analysis_s0.md`).
- Custo: usar `params_effective` e `macs_effective` (o Exp 5 tem o custo efetivo do Exp 6).
- Classes raras: no treino da amostra o desbalanceamento é ~2,9:1, não 149:1 — a conclusão sobre elas vale para esse cenário.
