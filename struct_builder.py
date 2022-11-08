from structure import *
from exemplar import *
from context import *
from cogmap import *
from sampler import *
from struct_builder_utils import get_dammy_struct_from_events_list
from hists import Hist
from struct_relaxer import StructRelaxer


class BasicStructBuilder:
    def __init__(self, dammy_struct, context):
        self.result_struct = Structure()
        self.dammy_struct = dammy_struct
        self.context = context

    def init_first_base_node(self):
        first_node_id = self.dammy_struct.recognition_order[0]
        parent_global_node_id, u_from_parent, mass, LUE_id= self.dammy_struct.get_info_to_recognise_node(first_node_id)
        sample_masses, sample_dus = sample_event_by_LUE_and_mass(self.context.contrast_maps, LUE_id, mass)
        actual_m_hist = Hist(sample_masses)
        actual_du_hist = Hist(sample_dus)
        self.result_struct.add_node(first_node_id, u_from_parent, parent_global_node_id, mass, LUE_id, actual_m_hist=actual_m_hist, actual_du_hist=actual_du_hist)


    def get_basic_struct(self, need_relax, need_readress):
        # создаем первое базовое событие, беря за основу небазовое первое событие из dammy_struct, по которой мы строим сейчас базовую стр-ру
        self.init_first_base_node()

        # перебираем все события self.dammy_struct кроме первого
        for node_global_id in self.dammy_struct.recognition_order[1:]:
            # добавляем новый experimental узел из self.dammy_struct в реузльтирующую структуру
            parent_global_node_id, u_from_parent, mass, LUE_id = self.dammy_struct.get_info_to_recognise_node(node_global_id)
            self.result_struct.add_node(node_global_id, u_from_parent, parent_global_node_id, mass, LUE_id)

            # для него получаем выбоки, обусловленные на всю уже построенную базовую структуру (она = текущая self.result_struct)
            exp_node_masses_sample, exp_node_dus_sample = sample_experimental_node(self.context.train_maps, self.result_struct, target_node_id=node_global_id)

            # делаем этот узел базовым:
            actual_m_hist = Hist(exp_node_masses_sample)
            actual_du_hist = Hist(exp_node_dus_sample)
            self.result_struct.nodes_dict[node_global_id].actual_m_hist =actual_m_hist
            self.result_struct.nodes_dict[node_global_id].actual_du_hist = actual_du_hist

            if need_relax:
                # релаксиурем имеющуюся к этому моменту базовую структуру
                dispersional_relaxer = StructRelaxer(basic_struct=self.result_struct, context=self.context)
                dammy_struct = dispersional_relaxer.get_relaxed_dammy_struct()


                if need_readress:
                    # делаем ре-адрессинг неучтенных узлов относительно учтенных:
                    for parent_id in dammy_struct.recognition_order:
                        # ищем в dammy_struct всех детей этого родителя, которые не учтены
                        for child_node_id, node_exemplar in self.dammy_struct.items():
                            if node_exemplar.parent_global_node_id == parent_id:
                                if child_node_id not in dammy_struct.recognition_order:
                                    # считаем изменение координаты родителя (относительно его родителя) после релаксации:
                                    new_parent_coord = dammy_struct.nodes_dict[parent_id].u_from_parent
                                    old_parent_coord = self.result_struct.nodes_dict[parent_id].u_from_parent
                                    du = Point(new_parent_coord.x-old_parent_coord.x, new_parent_coord.y-old_parent_coord.y)

                                    # это изменение вычитаем из координат ребенка
                                    old_child_coord = self.result_struct.nodes_dict[child_node_id].u_from_parent
                                    new_child_coord = old_child_coord+du
                                    self.result_struct.nodes_dict[child_node_id].u_from_parent = new_child_coord

                # реузльатты релаксации из dammy_struct переносим в result_struct
                for node_id, node_exemplar in self.dammy_struct.items():
                    self.result_struct.nodes_dict[node_id].u_from_parent = node_exemplar.u_from_parent


        return self.result_struct



