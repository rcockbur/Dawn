# a command queues up 1-2 abilities
from globals import *
from pathfinding import astar
from path import Path

print("running ability.py")
neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]



class Move():
    def __init__(self, unit, path, target_entity = None):
        self.unit = unit
        self.move_current = unit.move_period_ortho
        self.patience_current = unit.patience_max

        if target_entity is None:
            self.target_entity_id = None
        else:
            self.target_entity_id = target_entity.id
            
        self.path = path
        if self.path.size() == 0: raise RuntimeError("Cannot create move ability with path of size 0")
        self.color = COLOR_PATH_MOVING

    def execute(self):
        if self.path.size() == 0: raise RuntimeError("Cannot execute move ability with path of size 0")

        is_blocked = False
            
        entity = MAP.get_entity_at_tile(self.path.points[0])

        if entity is not None and self.target_entity_id is not None and entity.id == self.target_entity_id:
            return {"complete":True, "success":True}

        if type(entity) in self.unit.cant_move_types:
            is_blocked = True

        # we are blocked
        if is_blocked == True:
            self.patience_current = self.patience_current - 1
            if self.patience_current == 0:
                return {"complete":True, "success":False}
        else:
            self.patience_current = self.unit.patience_max

        if is_blocked == False and self.move_current == 0:
            self.update_move_current(self.path.points[0])
            self.unit.move(self.path.points.pop(0))
            if self.path.size() == 0:
                return {"complete":True, "success":True}
        self.move_current = max(self.move_current - 1, 0)
        return {"complete":False}






    def update_move_current(self, point):
        if self.unit.tile[0] != point[0] and self.unit.tile[1] != point[1]:
            self.move_current = self.unit.move_period_diag
        else:
            self.move_current = self.unit.move_period_ortho

        speed_up_factor = 1
        
        if self.unit.satiation_current <= self.unit.satiation_hungery:
            speed_up_factor += 0.3
            if self.unit.satiation_current <= self.unit.satiation_starving:
                speed_up_factor += 0.3
        else:
            if self.unit.can_mate():
                speed_up_factor += 0.3

        self.move_current = int(self.move_current / speed_up_factor)


class ApproachAbility():
    def __init__(self, unit, path, target_entity):
        self.unit = unit
        self.target_entity_id = target_entity.id
        if path is not None:
            if path.size() == 0: raise RuntimeError("Cannot approach with a size 0 path")
            self.approach = Move(unit, path, target_entity)
        else:
            self.approach = None
        self.approach_started = False


    def execute(self):
        if type(self.approach) == Move:
            results = self.approach.execute()
            if self.unit.is_selected and self.approach_started == False: print("starting approach")
            if results["complete"]:
                if results["success"]:
                    if self.unit.is_selected: print("approach complete")
                    self.approach = None
                else:
                    if self.unit.is_selected: print("approach interrupted")
                    return {"complete":True}

            self.approach_started = True
            return {"complete":False}
        else:
            target_entity = MAP.get_entity_by_id(self.target_entity_id)
            if target_entity is None or target_entity.is_dead == True:
                if self.unit.is_selected: print("target is dead")
                return {"complete":True, "success":False} # done, not successful
            diff_x = abs(target_entity.tile[0] - self.unit.tile[0])
            diff_y = abs(target_entity.tile[1] - self.unit.tile[1])
            if diff_x > 1 or diff_y > 1:
                path = astar(self.unit.tile, target_entity.tile, self.unit.cant_move_types, get_debug_pathfinding())
                if path is not None:
                    self.approach = Move(self.unit, path, target_entity)
                    if self.unit.is_selected: print("target has moved, recalculating")
                    return {"complete":False}
                else:
                    if self.unit.is_selected: print("target can no longer be reached")
                    return {"complete":True, "success":False}
            self.ability_function(target_entity)
            if self.unit.is_selected: print("target has been", self.verb)
            return {"complete":True, "success":True}


class Eat(ApproachAbility):
    def __init__(self, unit, path, target_entity):
        ApproachAbility.__init__(self, unit, path, target_entity)
        self.ability_function = self.unit.eat
        self.color = COLOR_PATH_HUNT
        self.verb = "eaten"
        if hasattr(target_entity, 'mark'):
            target_entity.mark()

class Mate(ApproachAbility):
    def __init__(self, unit, path, target_entity):
        ApproachAbility.__init__(self, unit, path, target_entity)
        self.ability_function = self.unit.mate
        self.color = COLOR_PATH_MATE
        self.verb = "mated with"

