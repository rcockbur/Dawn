from globals import *
from pathfinding import astar
# from path import Path
print("running ability.py")

class Move():
    def __init__(self, unit, path, target_entity = None, repath_attempts = 1):
        self.unit = unit
        self.move_current = unit.__class__.move_period
        self.patience_current = unit.__class__.patience_max
        self.noun = "wandering"
        self.path = path
        self.color = COLOR_PATH_MOVING
        self.repath_attempts = repath_attempts
        if target_entity is None:
            self.target_entity_id = None
        else:
            self.target_entity_id = target_entity.id
        if len(self.path) == 0: 
            raise RuntimeError("Cannot create move ability with path of size 0")
        

    def execute(self):
        if len(self.path) == 0: 
            raise RuntimeError("Cannot execute move ability with path of size 0")

        entity = MAP.get_entity_at_tile(self.path[0])
        if entity is not None and self.target_entity_id is not None and entity.id == self.target_entity_id:
            return {"complete":True, "success":True}

        is_blocked = False
        if type(entity) in self.unit.__class__.cant_move_types:
            is_blocked = True
        if is_blocked == True:
            self.patience_current = self.patience_current - 1
            if self.patience_current == 0:
                if self.repath_attempts > 0:
                    path = astar(self.unit.tile, self.path[-1], self.unit.__class__.cant_move_types, self.unit.is_selected and get_debug_pathfinding())
                    self.repath_attempts -= 1
                    # print(self.unit.name, "is pathing around", entity.name)
                    if path is not None:
                        self.path = path
                        return {"complete":False}
                    else:
                        print(self.unit.name, "was unable to find a repath, aborting")
                        return {"complete":True, "success":False}
                else:
                    # print(self.unit.name, "has lost patience with", entity.name)
                    return {"complete":True, "success":False}
        else:
            self.patience_current = self.unit.__class__.patience_max

        if is_blocked == False and self.move_current == 0:
            self.update_move_current(self.path[0])
            self.unit.move(self.path.pop(0))
            if len(self.path) == 0:
                return {"complete":True, "success":True}
        self.move_current = max(self.move_current - 1, 0)
        return {"complete":False}

    def update_move_current(self, point):
        if self.unit.tile[0] != point[0] and self.unit.tile[1] != point[1]:
            self.move_current = round(self.unit.__class__.move_period * 1.4)
        else:
            self.move_current = self.unit.__class__.move_period
        speed_up = 1
        if self.unit.in_danger:
            speed_up += 1.0
        else:
            if self.unit.sat_current <= self.unit.__class__.sat_hungery:
                speed_up += 0.3
                if self.unit.sat_current <= self.unit.__class__.sat_starving:
                    speed_up += 0.3
            else:
                if self.unit.can_mate():
                    speed_up += 0.3
        self.move_current = round(self.move_current / speed_up)

class ApproachAbility():
    def __init__(self, unit, path, target_entity):
        self.unit = unit
        self.target_entity_id = target_entity.id
        if path is not None:
            if len(path) == 0: raise RuntimeError("Cannot approach with a size 0 path")
            self.approach = Move(unit, path, target_entity, self.repath_attempts)
        else:
            self.approach = None
        self.approach_started = False
        self.can_execute_at = -1000
        self.chase_attempts_current = 0

    def execute(self):
        if type(self.approach) == Move:
            results = self.approach.execute()
            if results["complete"]:
                if results["success"]:
                    self.approach = None
                else:
                    return {"complete":True}

            self.approach_started = True
            return {"complete":False}
        else:
            target_entity = MAP.get_entity_by_id(self.target_entity_id)
            if target_entity is None or target_entity.is_destroyed == True:
                return {"complete":True, "success":False} # done, not successful
            diff_x = abs(target_entity.tile[0] - self.unit.tile[0])
            diff_y = abs(target_entity.tile[1] - self.unit.tile[1])
            if diff_x > 1 or diff_y > 1:
                if self.chase_attempts_current == self.chase_attempts:
                    return {"complete":True, "success":False}
                else:
                    self.chase_attempts_current += 1
                    path = astar(self.unit.tile, target_entity.tile, self.unit.__class__.cant_move_types, self.unit.is_selected and get_debug_pathfinding())
                    if path is not None:
                        self.approach = Move(self.unit, path, target_entity)
                        return {"complete":False}
                    else:
                        return {"complete":True, "success":False}
            if current_date[DT_HOUR] >= self.can_execute_at:
                r = self.ability_function(target_entity)
                if r["complete"] == True:
                    return {"complete":True, "success":True}
                else:
                    self.can_execute_at = current_date[DT_HOUR] + HOURS_PER_DAY
            return {"complete":False}


class Eat(ApproachAbility):
    def __init__(self, unit, path, target_entity):
        self.repath_attempts = unit.__class__.repath_attempts
        ApproachAbility.__init__(self, unit, path, target_entity)
        self.ability_function = self.unit.eat
        self.color = COLOR_PATH_HUNT
        self.noun = "eating"
        self.chase_attempts = unit.__class__.chase_attempts
        if hasattr(target_entity, 'mark'):
            target_entity.mark()

class Mate(ApproachAbility):
    def __init__(self, unit, path, target_entity):
        self.repath_attempts = unit.__class__.repath_attempts
        ApproachAbility.__init__(self, unit, path, target_entity)
        self.ability_function = self.unit.mate
        self.color = COLOR_PATH_MATE
        self.noun = "mating"
        self.chase_attempts = 2

class Socialize(ApproachAbility):
    def __init__(self, unit, path, target_entity):
        self.repath_attempts = unit.__class__.repath_attempts
        ApproachAbility.__init__(self, unit, path, target_entity)
        self.ability_function = self.unit.socialize
        self.color = COLOR_PATH_SOCIAL
        self.noun = "socializing"
        self.chase_attempts = 0
