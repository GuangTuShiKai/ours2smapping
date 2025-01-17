from graph import *
import numpy as np

dataPath = "data/m2d1.sub.grf.converted"
targetPath = "data/m2d1.grf.converted"
source_graph = SourceGraph(dataPath)
target_graph = TargetGraph(targetPath)
new_predicted_ids = []
new_predicted_probs = []
pea_size = 16
actor_logits = np.array([[-3.21894040e-05, 6.44688771e-05, 3.40090482e-05, -6.85931809e-06,
                 -6.41551451e-05, 4.95707827e-05, -6.60626611e-05, -7.91101120e-05,
                 -2.23353709e-07, 8.03828516e-05, 9.25431959e-05, 8.54916143e-05,
                 -1.55923299e-05, -1.34561751e-05, -2.99295043e-05, 1.00119818e-04],
                [-3.13385463e-05, -1.73362223e-05, -2.46380678e-05,  4.73765795e-05,
                 -1.64606099e-04, -5.45989315e-06, -9.47232184e-05, -1.76012487e-04,
                 5.27910415e-05,  1.80780291e-04,  6.77990611e-05, -1.23656457e-04,
                 -4.16201692e-05,  6.94090068e-06, -1.88830072e-05,  4.11535548e-05],
                [-3.47987458e-04,  1.74165980e-04,  4.97788365e-04, -1.61709235e-04,
                 -2.43635033e-04, -1.71111635e-04, -2.84822978e-04,  2.39660629e-04,
                 -3.83979750e-05, -7.52985943e-05,  2.57448643e-04, -4.17336676e-04,
                 1.96130859e-05,  1.44399397e-04, -3.11456970e-04,  1.58584167e-04],
                [-5.43442322e-04, -3.14142642e-04,  2.94341298e-04, -2.24656236e-04,
                 -2.11060425e-04, -1.03449456e-04, -4.15966642e-04,  1.62778146e-04,
                 -4.11409819e-05, -2.23741357e-04, -1.84820572e-04, -1.02521262e-05,
                 1.79627823e-05,  3.91137030e-04,  3.44239670e-04, -8.30497447e-05]])

for i in range(4):
    # give me an list of preceeding actions, return the feasible mapped nodes
    # set the weight on all infeasible actions to -inf
    infeasible = target_graph.get_infeasible_mapping_node(source_graph, new_predicted_ids, i == 0)
    print("---------------------", i, "--------------------------")
    # print("infeasible node:", infeasible)
    if len(infeasible) == len(target_graph.graph):
        # give up
        infeasible = new_predicted_ids
    for node in infeasible:
        actor_logits[i][node] = -np.inf
    # infeasible = new_predicted_ids


    # sofmax and sample a new action
    new_logits = np.array(actor_logits[i])
    new_logits = new_logits - np.max(new_logits)
    print("new_logits:", new_logits)
    probs = np.exp(new_logits) / np.sum(np.exp(new_logits))
    print("probs:", probs)
    action = np.random.choice(pea_size, 1, p=probs)
    print("action:", action)
    new_predicted_ids.append(action[0])
    new_predicted_probs.append(probs[action[0]])
