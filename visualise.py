# здесь код для визуализации всех основных сущностей (для визуальной отладки)
from cogmap import *

def VIS_LUE_event(back_pic_binary, ax, LUE_event):
    ax.title.set_text("event "+ str(LUE_event.local_cogmap_id))
    cm = plt.get_cmap('gray')
    ax.imshow(back_pic_binary, cmap=cm, vmin=0, vmax=1)

    color = 'green'
    marker = 'o'
    for coord in LUE_event.seq:
        ax.scatter(coord.x, coord.y, c=color, marker=marker, alpha=0.8, s=200)

    ax.scatter(LUE_event.point.x, LUE_event.point.y)
    annotation_str = "LUE_id=" + str() + ", mass=" + str(LUE_event.get_mass())
    ax.annotate(annotation_str, (LUE_event.point.x, LUE_event.point.y), color='blue', xytext=(20, 15), textcoords='offset points',
                ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc=color, alpha=0.6),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.95', color='b'))



def VIS_LUE_cogmap(cogmap):
    num_axs = len(cogmap.LUE_events_list)
    fig, axs = plt.subplots(1, num_axs, figsize=(8 * num_axs, 8), dpi=60)
    for i in range(num_axs):
        VIS_LUE_event(cogmap.pic, axs[i], cogmap.LUE_events_list[i])
    return fig

def VIS_LUE_cogmap1(cogmap):
    fig, axs = plt.subplots(1, 3, figsize=(8 * 2, 8), dpi=60)
    cm = plt.get_cmap('gray')

    axs[0].title.set_text("pic")
    axs[0].imshow(cogmap.pic, cmap=cm, vmin=0, vmax=1)

    axs[1].title.set_text("hor_img")
    axs[1].imshow(cogmap.hor_img, cmap=cm, vmin=0, vmax=1)

    axs[2].title.set_text("ver_img")
    axs[2].imshow(cogmap.ver_img, cmap=cm, vmin=0, vmax=1)
    return fig

def VIS_exemplar(exemplar):
    pass
    """   arrow = mpatches.FancyArrowPatch((prev_event_coord.x, prev_event_coord.y), (coord.x, coord.y),
                                                 mutation_scale=10)
            ax.add_patch(arrow)"""