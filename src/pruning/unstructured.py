"""Poda nao estruturada L1 (Exp 2, 3 e 4) - RESPONSAVEL: Gabriel.

DEMANDA ABERTA (docs/DEMANDAS.md, D-01): definir antes de implementar
- escopo: global (todas as camadas ordenadas juntas) ou por camada;
- quais camadas ficam fora (sugestao: conv1 e fc, como na poda estruturada);
- registrar a decisao em configs/default.yaml (secao `unstructured`) e em docs/SPEC.md.

Contrato que o restante do pipeline espera (para encaixar em scripts/ e src/evaluate.py):

    plan = select_weights(model, amount, cfg)   # quais pesos zerar
    apply_mask(model, plan)                     # zera os pesos (Exp 2-4)
    fit(model, loaders, cfg["finetune"], device, after_step=mask_hook(plan))
                                                # fine-tuning com mascara FIXA

Cuidados obrigatorios:
- a mascara precisa continuar aplicada durante o fine-tuning (senao os zeros "voltam");
- se usar torch.nn.utils.prune, chamar prune.remove(...) antes de salvar/avaliar:
  sem isso o state_dict guarda weight_orig + weight_mask e o tamanho em MB dobra;
- partir SEMPRE do checkpoint results/exp1_baseline_s<seed>/exp1_baseline_s<seed>.pt
  da mesma semente.
"""


def select_weights(model, amount, cfg):
    raise NotImplementedError("D-01: poda L1 nao estruturada a definir (Gabriel)")


def apply_mask(model, plan):
    raise NotImplementedError("D-01: poda L1 nao estruturada a definir (Gabriel)")


def mask_hook(plan):
    raise NotImplementedError("D-01: poda L1 nao estruturada a definir (Gabriel)")
