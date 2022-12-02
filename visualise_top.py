from visualise_objects import *
from recognise import recognize_basic_struct
from struct_builder_utils import get_hists_for_every_basic_node_of_struct
from utils import *
from recognise import *


import matplotlib.pyplot as plt

def VIS_nodes_info_struct(struct, logger, target_maps):
    if logger is None:
        return
    # для каждой ноды 2 гистограммы
    nrows = len(struct)
    ncols = 2

    dict_m, dict_du = get_hists_for_every_basic_node_of_struct(struct, target_maps)

    fig, axs = plt.subplots(nrows=max(len(struct), 2), ncols=ncols)

    for row in range(nrows):
        global_node_id = struct.recognition_order[row]
        node = struct.nodes_dict[global_node_id]
        if node.actual_m_hist is None:
            logger.add_text(str(row)+ "-ый не имеет гистограмм")
        else:
            axs[row, 0].set_title("[" + str(row) +"-ый] masses")
            axs[row, 0].hist(node.actual_m_hist.sample, alpha=0.5)
            target_m_sample = dict_m[global_node_id]
            axs[row, 0].hist(target_m_sample, color='red', label='target', alpha=0.5)
            # axs[row, 0].set_ylim(-0.1,1.1)

            axs[row, 1].set_title("[" + str(row) + "-ый] dus")
            axs[row, 1].hist(node.actual_du_hist.sample, alpha=0.5) #density=True
            target_du_sample = dict_du[global_node_id]
            axs[row, 1].hist(target_du_sample, color='red', label='target', alpha=0.5)
            #axs[row, 1].set_ylim(-0.1, 1.1)

    plt.legend(loc='upper right')
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    logger.add_fig(fig)
    logger.save()


def visualise_classification_properties_of_basic_struct(basic_struct, constrast_cogmaps, target_cogmaps):
    # две наложенные гистограммы: нетривиальность на контрасте и на целевых
    non_trivs_target = []
    non_trivs_contrast = []
    for cogmap in constrast_cogmaps:
        best_done_basic_exemplar, basic_success = recognize_basic_struct(basic_struct, cogmap)
        non_trivs_contrast.append(best_done_basic_exemplar.eval_exemplar())

    for cogmap in target_cogmaps:
        best_done_basic_exemplar, basic_success = recognize_basic_struct(basic_struct, cogmap)
        non_trivs_target.append(best_done_basic_exemplar.eval_exemplar())

    left = 0
    right = basic_struct.max_non_triviality()

    fig, ax = plt.subplots()
    ax.set_xlim(left, right)
    ax.hist(non_trivs_contrast, color='b', label='contrast')
    ax.hist(non_trivs_target,  color='r', label='taget', alpha=0.5)

    plt.legend(loc='upper right')
    return fig


def VIS_detailed_exemplar_of_struct(cogmap, basic_struct, logger):
    logger.add_text("detailed exemplar of struct:----------")

    best_done_basic_exemplar, basic_success = recognize_basic_struct(basic_struct, cogmap)
    fig = VIS_exemplar_as_graph(best_done_basic_exemplar, need_annotations=True)
    logger.add_fig(fig)

    VIS_nodes_info_exemplar(best_done_basic_exemplar, logger)
    logger.add_text("----------")


def VIS_exemplars_of_struct(cogmaps, basic_struct, logger):
    for cogmap in cogmaps:
        best_done_basic_exemplar, basic_success = recognize_basic_struct(basic_struct, cogmap)
        fig = VIS_exemplar_as_graph(best_done_basic_exemplar, need_annotations=False)
        logger.add_fig(fig)
