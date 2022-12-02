# здесь код для визуализации всех основных сущностей (для визуальной отладки)
from cogmap import *
from exemplar import *
from utils import *

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
    plt.close('all')
    fig, ax = plt.subplots()

    title = str(exemplar.eval_exemplar())
    if not exemplar.is_recognition_done():
        title += ":NOT FULL"
    fig.suptitle(title, fontsize=20)

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
        color = exemplar.structure.get_event_color(global_node_id)
        ax.scatter(coord.x, coord.y, c=[color], marker=marker, alpha=0.8, s=200)

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
            parent_point = exemplar.get_point_by_global_node_id(parent_global_id)
            arrow = mpatches.FancyArrowPatch((parent_point.x, parent_point.y), (coord.x, coord.y),
                                             mutation_scale=10)
            ax.add_patch(arrow)

        # рисуем змейку, ассоциированную с этим событием
        local_event_id = exemplar.nodes_local_ids[global_node_id]
        event_color = exemplar.structure.get_event_color(global_node_id)
        marker = 'o'
        LUE_event = exemplar.cogmap.LUE_events[local_event_id]
        for coord in LUE_event.seq:
            ax.scatter(coord.x, coord.y, c=[event_color], marker=marker, alpha=0.2, s=100)



def VIS_struct_as_graph(struct):
    plt.close('all')
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
            global_ids_to_coords[global_node_id] = point
        else:
            u_from_parent = node.u_from_parent
            parent_point = global_ids_to_coords[parent_global_node_id]
            point = parent_point+u_from_parent
            global_ids_to_coords[global_node_id] = point
            arrow = mpatches.FancyArrowPatch((parent_point.x, -parent_point.y), (point.x, -point.y),
                                             mutation_scale=10)
            ax.add_patch(arrow)
        if node.actual_m_hist is not None:
            color = 'green'
        else:
            color = 'red'
        marker = '$' + str(i) + '$'
        ax.scatter(point.x, -point.y, c=color, marker=marker, alpha=0.8, s=200)
    return fig




def VIS_nodes_info_exemplar(exemplar, logger):
    # для каждой ноды гистограмму и на ней отрисовать палочками истинное значение и реальное
    nrows = max(len(exemplar), 2)
    ncols = 2

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
    for index in range(len(exemplar)):
        global_node_id = exemplar.structure.recognition_order[index]
        node_recognition_res = exemplar.nodes_recognition_results[global_node_id]
        real_mass = node_recognition_res.mass
        expected_mass = node_recognition_res.structure_node.mass
        du = my_norm(node_recognition_res.du)
        if node_recognition_res.structure_node.actual_m_hist is None:
            log_str = str(index) + " is not basic. Real_mass = " + str(real_mass) + ", expected = " + str(expected_mass) + ", du=" + str(du)
            logger.add_text(log_str)

        else:
            linewidth=1
            axs[index, 0].set_title("[" + str(index) +"-ый] masses")
            axs[index, 0].hist(node_recognition_res.structure_node.actual_m_hist.sample, density=True)
            axs[index, 0].axvline(x=real_mass, linewidth=linewidth,  color='r')
            axs[index, 0].axvline(x=expected_mass, linestyle='dashed', linewidth=linewidth)
            axs[index, 0].text(x=expected_mass,  y=0.01, s='expected')

            axs[index, 1].set_title("[" + str(index) + "-ый] dus")
            axs[index, 1].hist(node_recognition_res.structure_node.actual_du_hist.sample, density=True)
            axs[index, 1].axvline(x=du, linewidth=linewidth, color='r')
            axs[index, 1].text(x=du, y=0.01, s='real err')

    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    logger.add_fig(fig)
    logger.save()


def VIS_recognition_generation(logger, generation_sorted):
    nrows = 1
    ncols = max(len(generation_sorted), 2)

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)

    i=0
    for exemplar_entry in generation_sorted.entries:
        ax = axs[ i]
        # рисуем когмапу
        cm = plt.get_cmap('gray')
        ax.imshow(exemplar_entry.exemplar.cogmap.pic, cmap=cm, vmin=0, vmax=1)
        # рисуем экземпляр
        VIS_exemplar_as_graph_to_ax(ax, exemplar_entry.exemplar, need_annotations=False)
        i += 1
        ax.set_title("non_triv=" + str(round(exemplar_entry.non_triviality, 2)) )


    logger.add_fig(fig)
    logger.save()

def VIS_nontrivs_of_generation(logger, generation_sorted):
    list_nontrivialities = []
    for exemplar_entry in generation_sorted.entries:
        list_nontrivialities.append(exemplar_entry.non_triviality)
    fig, ax = plt.subplots()
    x = list(range(len(list_nontrivialities)))
    ax.scatter(x, list_nontrivialities, marker='o')
    ax.set_title("non_trivs of generation")
    logger.add_fig(fig)