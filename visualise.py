# здесь код для визуализации всех основных сущностей (для визуальной отладки)
from cogmap import *
from exemplar import *
from utils import *
from recognise import recognize_basic_struct

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

def VIS_LUE_event(back_pic_binary, ax, LUE_event):
    ax.title.set_text("event "+ str(LUE_event.local_cogmap_id))
    cm = plt.get_cmap('gray')
    ax.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)

    color = 'green'
    marker = 'o'
    for coord in LUE_event.seq:
        ax.scatter(coord.x, coord.y, c=color, marker=marker, alpha=0.8, s=200)

    ax.scatter(LUE_event.point.x, LUE_event.point.y)
    annotation_str = "LUE_id=" + str(LUE_event.local_cogmap_id) + ", mass=" + str(LUE_event.mass)
    ax.annotate(annotation_str, (LUE_event.point.x, LUE_event.point.y), color='blue', xytext=(20, 15), textcoords='offset points',
                ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc=color, alpha=0.6),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95', color='b'))



def VIS_LUE_cogmap_second_generation(cogmap, logger):
    LUE_events_list = list(cogmap.LUE_events.keys())
    num_axs = len(LUE_events_list)
    fig, axs = plt.subplots(1, num_axs, figsize=(8 * num_axs, 8), dpi=60)
    i=0
    for local_event_id in LUE_events_list:
        VIS_LUE_event(cogmap.pic, axs[i], cogmap.LUE_events[local_event_id])
        i+=1
    logger.add_fig(fig)
    logger.save()

def VIS_LUE_cogmap_first_generation(cogmap, logger):
    fig, axs = plt.subplots(1, 3, figsize=(8 * 2, 8), dpi=60)
    cm = plt.get_cmap('gray')

    axs[0].title.set_text("pic")
    axs[0].imshow(cogmap.pic, cmap=cm, vmin=0, vmax=1)

    axs[1].title.set_text("hor_img")
    axs[1].imshow(cogmap.hor_img, cmap=cm, vmin=0, vmax=1)

    axs[2].title.set_text("ver_img")
    axs[2].imshow(cogmap.ver_img, cmap=cm, vmin=0, vmax=1)
    logger.add_fig(fig)
    logger.save()

def VIS_exemplar_as_graph(exemplar,need_annotations):
    fig, ax = plt.subplots()

    title = str(exemplar.eval_exemplar()) + "-exempl "
    if not exemplar.is_recognition_done():
        title += ":NOT FULL"
    fig.title = title

    cm = plt.get_cmap('gray')
    pic = exemplar.cogmap.pic
    ax.imshow(pic, cmap=cm, vmin=0, vmax=1)
    VIS_exemplar_as_graph_to_ax(ax, exemplar, need_annotations)
    return fig

def VIS_exemplar_as_graph_to_ax(ax, exemplar, need_annotations):
    # перебираем все имеющиеся распознанные события:
    for index in range(len(exemplar)):
        global_node_id = exemplar.structure.recognition_order[index]
        node_recognition_res = exemplar.nodes_recognition_results[global_node_id]
        coord = node_recognition_res.point

        # рисуем событие на карте:
        index = exemplar.structure.recognition_order.index(global_node_id) # номер этого события в порядке распознавания
        marker = '$' + str(index) + '$'
        ax.scatter(coord.x, coord.y, c='green', marker=marker, alpha=0.8, s=200)

        # если надо, то еще и делаем к событию сноску с подровностями:
        if need_annotations:
            mass = node_recognition_res.mass
            annotation_text = "global_id="+str(global_node_id) +" mass=" + str(mass)
            ax.annotate(annotation_text, (coord.x, coord.y), color='blue', xytext=(20, 15), textcoords='offset points',
                        ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.6),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95', color='b'))

        # если это не начальное событие, то рисуем входящую стрелку от родителя:
        parent_global_id = node_recognition_res.structure_node.parent_global_node_id
        if parent_global_id is not None:
            parent_point = exemplar.get_point_by_global_node_id(parent_global_id, global_node_id)
            arrow = mpatches.FancyArrowPatch((parent_point.x, parent_point.y), (coord.x, coord.y),
                                             mutation_scale=10)
            ax.add_patch(arrow)


def VIS_struct_as_graph(struct):
    fig, ax = plt.subplots()
    title = "struct (green=basic)"
    fig.title = title

    global_ids_to_coords={}

    for i in range(len(struct.recognition_order)):
        global_node_id = struct.recognition_order[i]
        node = struct.nodes_dict[global_node_id]
        parent_global_node_id = node.parent_global_node_id
        if parent_global_node_id is None:
            point = Point(0, 0)
            global_ids_to_coords[parent_global_node_id] = point
        else:
            u_from_parent = node.u_from_parent
            parent_point = global_ids_to_coords[parent_global_node_id]
            point = parent_point+u_from_parent
            global_ids_to_coords[global_node_id] = point
            arrow = mpatches.FancyArrowPatch((parent_point.x, parent_point.y), (point.x, point.y),
                                             mutation_scale=10)
            ax.add_patch(arrow)
        if node.actual_m_hist is not None:
            color = 'green'
        else:
            color = 'red'
        marker = '$' + str(i) + '$'
        ax.scatter(point.x, point.y, c=color, marker=marker, alpha=0.8, s=200)
    return fig


def VIS_nodes_info_struct(struct, logger):
    # для каждой ноды 2 гистограммы
    nrows = len(struct)
    ncols = 2

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)

    for row in range(nrows):
        global_node_id = struct.recognition_order[row]
        node = struct.nodes_dict[global_node_id]
        if node.actual_m_hist is None:
            logger.add_text(str(row)+ "-ый не имеет гистограмм")
        else:
            axs[row, 0].set_title("[" + str(row) +"-ый] masses")
            axs[row, 0].hist(node.actual_m_hist.sample, density=True, edgecolor="black")
            axs[row, 1].set_title("[" + str(row) + "-ый] dus")
            axs[row, 1].hist(node.actual_du_hist.sample, density=True, edgecolor="red")
    logger.add_fig(fig)
    logger.save()

def VIS_nodes_info_exemplar(exemplar, logger):
    # для каждой ноды гистограмму и на ней отрисовать палочками истинное значение и реальное
    nrows = len(exemplar)
    ncols = 2

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
    for index in range(len(exemplar)):
        global_node_id = exemplar.structure.recognition_order[index]
        node_recognition_res = exemplar.nodes_recognition_results[global_node_id]
        real_mass = node_recognition_res.mass
        expected_mass = node_recognition_res.structure_node.mass
        du = my_norm(node_recognition_res.du)
        if node_recognition_res.structure_node.actual_m_hist is None:
            log_str = str(index) + " is not basic. Real_mass = " + str(real_mass) + ", expected = "+ str(expected_mass) + ", du=" + str(du)
            logger.add_text(log_str)

        else:
            linewidth=1
            axs[index, 0].set_title("[" + str(index) +"-ый] masses")
            axs[index, 0].hist(node_recognition_res.structure_node.actual_m_hist.sample, density=True, edgecolor="black")
            axs[index, 0].axvline(x=real_mass, linewidth=linewidth)
            axs[index, 0].axvline(x=expected_mass, linestyle='dashed', linewidth=linewidth)
            axs[index, 0].text(expected_mass+1.1, 0.1, 'expected')

            axs[index, 1].set_title("[" + str(index) + "-ый] dus")
            axs[index, 1].hist(node_recognition_res.structure_node.actual_du_hist.sample, density=True, edgecolor="red")
            axs[index, 0].axvline(x=du, linewidth=linewidth)
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
    _, bins, _ = ax.hist(non_trivs_contrast, color='b', label='contrast')
    _ = ax.hist(non_trivs_target, bins=bins, color='g', label='taget', alpha=0.5)
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
        fig = VIS_exemplar_as_graph(best_done_basic_exemplar, need_annotations=True)
        logger.add_fig(fig)
