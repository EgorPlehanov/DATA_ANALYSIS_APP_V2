from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .workplace import Workplace

from flet import *
import flet.canvas as cv
from typing import Dict

from .node import Node, NodeConfig
from .node_typing import NodeConnect
from .node_connect_point import NodeConnectPoint



class NodeArea(cv.Canvas):
    def __init__(self, page: Page, workplace: "Workplace"):
        super().__init__()
        self.page = page
        self.workplace = workplace

        self.current_scale = 1
        
        self.background_grid = self.create_background_grid()
        self.shapes = self.background_grid

        self.nodes: list[Node] = []
        self.selected_nodes: list[Node] = []

        self.content = GestureDetector(
            content = Stack(
                width = self.width,
                height = self.height,
                controls = self.nodes,                
            ),
            on_tap = self.clear_selection,
            on_scroll = self.scroll_scale_node_area,
            # on_pan_update = self.drag_all
        )

        self.node_connects: Dict[int, NodeConnect] = {}

    
    def create_background_grid(self):
        '''
        Создает фоновую сетку
        '''
        return [
            cv.Line(
                0, i * 50 + 1,
                5000, i * 50 + 1,
                paint = Paint(
                    color = colors.WHITE12,
                    stroke_width = 2,
                    stroke_dash_pattern = [2, 50],
                )
            )
            for i in range(0, 20)
        ]


    def add_node(self, config: NodeConfig):
        """
        Добавить узел
        """
        self.nodes.append(Node(
            page=self.page, node_area=self,
            scale=self.current_scale, config=config
        ))
        self.workplace.node_stats.update_text("nodes", len(self.nodes))
        self.update()

    
    def delete_node(self, node):
        """
        Удалить узел
        """
        self.nodes.remove(node)
        if node in self.selected_nodes:
            self.selected_nodes.remove(node)
        
        self.workplace.node_stats.update_text("nodes", len(self.nodes))
        self.paint_line()


    def delete_node_connect(self, node_id, param_idx):
        '''
        Удаляет соединение между узлами
        '''
        node: Node = next(node for node in self.nodes if node.id == node_id)
        node.clear_contact_point(param_idx)


    def calculate_coord(self, node: Node, point: NodeConnectPoint):
        left_center = node.width // 2
        top_center = node.height // 2

        point_left = point.left + node.POINT_SIZE // 2 - left_center
        point_top = point.top + node.POINT_SIZE // 2 - top_center

        point_left_scl = point_left * self.current_scale + left_center
        point_top_scl = point_top * self.current_scale + top_center

        return node.left + point_left_scl, node.top + point_top_scl
    

    def get_coords(self, connect: NodeConnect):
        '''
        Возвращает координаты начала и конца линии соединения
        '''
        from_node: Node = next((node for node in self.nodes if node.id == connect.from_node_id), None)
        if from_node is None:
            raise Exception('From Node not found')
        from_point: NodeConnectPoint = next((point for point in from_node.connect_points if point.id == connect.from_value_idx), None)
        from_left, from_top = self.calculate_coord(from_node, from_point)
        
        to_node: Node = next((node for node in self.nodes if node.id == connect.to_node_id), None)
        if to_node is None:
            raise Exception('To Node not found')
        to_point: NodeConnectPoint = next((point for point in to_node.connect_points if point.id == connect.to_param_idx), None)
        to_left, to_top = self.calculate_coord(to_node, to_point)

        return from_left, from_top, to_left, to_top
    

    def paint_line(self, line_len = 10, steepness = 70):
        '''
        Рисует линию соединения
        '''
        line_len *= self.current_scale
        steepness *= self.current_scale
        shp = []
        for node in self.nodes:
            for connect in node.connects:
                try:
                    from_left, from_top, to_left, to_top = self.get_coords(connect)
                    if connect.ref_path.current is None:
                        shp.append(cv.Path(
                            ref = connect.ref_path,
                            elements = [
                                cv.Path.MoveTo(from_left, from_top),
                                cv.Path.LineTo(from_left + line_len, from_top),
                                cv.Path.CubicTo(
                                    from_left + steepness, from_top,
                                    to_left - steepness, to_top,
                                    to_left - line_len, to_top,
                                ),
                                cv.Path.LineTo(to_left, to_top),
                            ],
                            paint = Paint(
                                stroke_width = 2,
                                style = PaintingStyle.STROKE,
                                color = connect.color
                            ),
                        ))
                    else:
                        shp.append(connect.ref_path.current)
                        connect.ref_path.current.paint.color = connect.color
                        move_to, line_from_to, cubic_to, line_to_to = connect.ref_path.current.elements[:4]
                        move_to.x,      move_to.y      = from_left,             from_top
                        line_from_to.x, line_from_to.y = from_left + line_len,  from_top
                        cubic_to.cp1x,  cubic_to.cp1y  = from_left + steepness, from_top
                        cubic_to.cp2x,  cubic_to.cp2y  = to_left - steepness,   to_top
                        cubic_to.x,     cubic_to.y     = to_left - line_len,    to_top
                        line_to_to.x,   line_to_to.y   = to_left,               to_top
                except Exception as ex:
                    self.delete_node_connect(connect.to_node_id, connect.to_param_idx)
        
        self.workplace.node_stats.update_text("edges", len(shp))
        
        shp.extend(self.background_grid)
        self.shapes = shp
        self.update()


    def add_selection_node(self, node):
        """
        Добавить выделение
        """
        if node not in self.selected_nodes:
            self.selected_nodes.append(node)
            self.workplace.node_stats.update_text("selected", len(self.selected_nodes))



    def remove_selection_node(self, node):
        """
        Удалить выделение
        """
        if node in self.selected_nodes:
            self.selected_nodes.remove(node)
            self.workplace.node_stats.update_text("selected", len(self.selected_nodes))


    def clear_selection(self, e):
        """
        Очистить выделение со всех выбранных узлов
        """
        for node in reversed(self.selected_nodes):
            node.toggle_selection(None)
        self.selected_nodes = []


    def drag_selection(self, top_delta = 0, left_delta = 0):
        """
        Переместить выделение
        """
        for node in self.selected_nodes:
            node.drag_node(left_delta, top_delta)


    def drag_all(self, e):
        '''
        Переместить все узлы
        '''
        for node in self.nodes:
            node.drag_node(e.delta_x, e.delta_y)
        self.paint_line()
    

    def select_all(self, e):
        '''
        Выделить все узлы
        '''
        for node in self.nodes:
            if not node.is_selected:
                node.toggle_selection(None)


    def delete_selected_nodes(self, e):
        '''
        Удалить выделенные узлы
        '''
        for node in reversed(self.selected_nodes):
            self.delete_node(node)
        

    def invert_selection(self, e):
        '''
        Инвертировать выделение
        '''
        for node in self.nodes:
            node.is_selected = not node.is_selected
            node.set_selection()
        self.update()


    def move_selection_to_start(self, e):
        '''
        Переместить выделенные узлы в начало
        '''
        for idx, node in enumerate(sorted(self.selected_nodes, key=lambda x: x.id)):
            node.top = idx * 30
            node.left = (idx % 5) * 100
        self.paint_line()
    

    def scroll_scale_node_area(self, e: ScrollEvent):
        '''
        Масштабирование узлов
        '''
        scale_min, scale_max, scale_round = 0.1, 2, 2

        scale_delta = round(e.scroll_delta_y / -2000, scale_round)
        new_scale = round(self.current_scale + scale_delta, scale_round)
        if (new_scale < scale_min or new_scale > scale_max):
            return
        
        self.current_scale = new_scale
        self.set_scale(e.local_x, e.local_y, scale_delta)

        self.workplace.node_stats.update_text("scale", self.current_scale)
        self.update()


    def set_scale(self, zoom_x, zoom_y, scale_delta):
        '''
        Установить масштаб узлов
        '''
        for node in self.nodes:
            node.scale = self.current_scale
            
            l_x = (node.left + node.width // 2) - zoom_x
            l_y = (node.top + node.height // 2) - zoom_y

            node.drag_node(
                l_x * scale_delta / self.current_scale,
                l_y * scale_delta / self.current_scale
            )
            self.paint_line()