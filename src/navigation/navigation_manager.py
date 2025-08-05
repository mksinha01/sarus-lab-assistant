"""
Navigation manager for Sarus robot

Handles autonomous movement, path planning, obstacle avoidance,
and exploration behaviors using sensor data and motor control.
"""

import asyncio
import logging
import time
import random
import math
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

from ..hardware.motor_controller import MotorController
from ..hardware.sensor_manager import SensorManager
from ..ai.vision_manager import VisionManager
from ..config.settings import SYSTEM_CONFIG
from ..utils.logger import get_logger

class NavigationState(Enum):
    """Navigation states"""
    IDLE = "idle"
    MOVING = "moving"
    TURNING = "turning"
    AVOIDING_OBSTACLE = "avoiding_obstacle"
    EXPLORING = "exploring"
    SEEKING_TARGET = "seeking_target"
    STUCK = "stuck"

class MovementDirection(Enum):
    """Movement directions"""
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"
    STOP = "stop"

@dataclass
class NavigationGoal:
    """Navigation goal definition"""
    target_object: Optional[str] = None
    target_location: Optional[Tuple[float, float]] = None
    exploration_area: Optional[str] = None
    max_duration: float = 300.0  # 5 minutes default
    priority: int = 1  # Higher number = higher priority

class NavigationManager:
    """
    Manages robot navigation including autonomous movement,
    obstacle avoidance, and exploration behaviors
    """
    
    def __init__(self, motor_controller: MotorController, 
                 sensor_manager: SensorManager, 
                 vision_manager: VisionManager):
        self.logger = get_logger(__name__)
        
        # Component references
        self.motor_controller = motor_controller
        self.sensor_manager = sensor_manager
        self.vision_manager = vision_manager
        
        # Configuration
        self.max_speed = SYSTEM_CONFIG.get('max_speed', 0.8)
        self.turn_speed = SYSTEM_CONFIG.get('turn_speed', 0.6)
        self.obstacle_threshold = SYSTEM_CONFIG.get('obstacle_distance_threshold', 30)
        self.emergency_threshold = SYSTEM_CONFIG.get('emergency_stop_distance', 10)
        
        # Navigation state
        self.state = NavigationState.IDLE
        self.current_goal: Optional[NavigationGoal] = None
        
        # Path tracking
        self.position_history: List[Tuple[float, float, float]] = []  # x, y, timestamp
        self.movement_history: List[str] = []
        self.stuck_detection_threshold = 5  # Number of similar positions
        
        # Exploration behavior
        self.exploration_patterns = {
            'random': self._random_exploration,
            'wall_follow': self._wall_follow_exploration,
            'spiral': self._spiral_exploration,
            'systematic': self._systematic_exploration
        }
        self.current_exploration_pattern = 'random'
        
        # Obstacle avoidance
        self.avoidance_behavior = 'simple'  # 'simple', 'advanced'
        self.last_obstacle_time = 0
        self.consecutive_obstacles = 0
        
        # Performance tracking
        self.total_distance_traveled = 0.0
        self.objects_found = []
        self.areas_explored = set()
        
    async def execute_action(self, action: Dict[str, Any]) -> bool:
        """
        Execute a navigation action
        
        Args:
            action: Action dictionary with type and parameters
        
        Returns:
            True if action completed successfully
        """
        try:
            action_type = action.get('type', '')
            
            if action_type == 'movement':
                return await self._execute_movement_action(action)
            elif action_type == 'exploration':
                return await self._execute_exploration_action(action)
            elif action_type == 'seek_object':
                return await self._execute_seek_action(action)
            else:
                self.logger.warning(f"Unknown action type: {action_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to execute navigation action: {e}")
            return False
    
    async def _execute_movement_action(self, action: Dict[str, Any]) -> bool:
        """Execute basic movement command"""
        direction = action.get('direction', 'forward')
        duration = action.get('duration', 2.0)
        speed = action.get('speed', self.max_speed)
        
        self.logger.info(f"🧭 Executing movement: {direction} for {duration}s")
        
        # Check if path is clear before moving
        if direction == 'forward' and not await self._is_path_safe('front'):
            self.logger.warning("Forward path blocked - canceling movement")
            return False
        
        # Execute movement
        if direction == 'forward':
            await self.motor_controller.move_forward(speed, duration)
        elif direction == 'backward':
            await self.motor_controller.move_backward(speed, duration)
        elif direction == 'left':
            await self.motor_controller.turn_left(speed, duration)
        elif direction == 'right':
            await self.motor_controller.turn_right(speed, duration)
        else:
            await self.motor_controller.stop()
        
        # Record movement
        self.movement_history.append(f"{direction}_{duration}")
        await self._update_position_estimate(direction, duration)
        
        return True
    
    async def _execute_exploration_action(self, action: Dict[str, Any]) -> bool:
        """Execute exploration mission"""
        exploration_type = action.get('exploration_type', 'random')
        max_duration = action.get('max_duration', 300.0)
        
        goal = NavigationGoal(
            exploration_area=exploration_type,
            max_duration=max_duration
        )
        
        self.current_goal = goal
        self.state = NavigationState.EXPLORING
        
        self.logger.info(f"🗺️ Starting exploration: {exploration_type} for {max_duration}s")
        return True
    
    async def _execute_seek_action(self, action: Dict[str, Any]) -> bool:
        """Execute object seeking behavior"""
        target_object = action.get('target_object', '')
        max_search_time = action.get('max_search_time', 120.0)
        
        if not target_object:
            self.logger.warning("No target object specified for seek action")
            return False
        
        goal = NavigationGoal(
            target_object=target_object,
            max_duration=max_search_time
        )
        
        self.current_goal = goal
        self.state = NavigationState.SEEKING_TARGET
        
        self.logger.info(f"🎯 Seeking object: {target_object}")
        return True
    
    async def continue_exploration(self, mission_data: Dict[str, Any]) -> bool:
        """
        Continue exploration mission
        
        Args:
            mission_data: Current mission information
        
        Returns:
            True if mission is complete, False to continue
        """
        if self.state != NavigationState.EXPLORING:
            return True  # Mission complete if not exploring
        
        try:
            # Check mission duration
            start_time = mission_data.get('start_time', time.time())
            max_duration = mission_data.get('max_duration', 300.0)
            
            if time.time() - start_time > max_duration:
                self.logger.info("⏰ Exploration mission time limit reached")
                return True
            
            # Check if stuck
            if await self._detect_stuck_condition():
                self.logger.warning("🚫 Robot appears stuck - ending exploration")
                return True
            
            # Perform exploration step
            await self._perform_exploration_step()
            
            # Check for discoveries
            await self._check_for_discoveries(mission_data)
            
            return False  # Continue mission
            
        except Exception as e:
            self.logger.error(f"Error during exploration: {e}")
            return True  # End mission on error
    
    async def _perform_exploration_step(self):
        """Perform one step of exploration behavior"""
        # Get current sensor readings
        nav_data = self.sensor_manager.get_navigation_data()
        obstacles = nav_data.get('obstacles', {})
        
        # Check for immediate obstacles requiring avoidance
        if await self._need_obstacle_avoidance(obstacles):
            await self._perform_obstacle_avoidance(obstacles)
            return
        
        # Continue with exploration pattern
        exploration_func = self.exploration_patterns.get(
            self.current_exploration_pattern, 
            self._random_exploration
        )
        
        await exploration_func()
    
    async def _random_exploration(self):
        """Random exploration pattern"""
        # Choose random direction and duration
        directions = ['forward', 'left', 'right']
        weights = [0.6, 0.2, 0.2]  # Prefer forward movement
        
        direction = random.choices(directions, weights=weights)[0]
        
        if direction == 'forward':
            duration = random.uniform(1.0, 3.0)
            if await self._is_path_safe('front'):
                await self.motor_controller.move_forward(self.max_speed * 0.7, duration)
            else:
                # Turn instead
                turn_direction = random.choice(['left', 'right'])
                await self.motor_controller.turn_left(self.turn_speed, 1.0) if turn_direction == 'left' else await self.motor_controller.turn_right(self.turn_speed, 1.0)
        else:
            duration = random.uniform(0.5, 1.5)
            if direction == 'left':
                await self.motor_controller.turn_left(self.turn_speed, duration)
            else:
                await self.motor_controller.turn_right(self.turn_speed, duration)
        
        # Record movement
        self.movement_history.append(f"{direction}_{duration:.1f}")
        await asyncio.sleep(0.5)  # Brief pause between movements
    
    async def _wall_follow_exploration(self):
        """Wall following exploration pattern"""
        nav_data = self.sensor_manager.get_navigation_data()
        obstacles = nav_data.get('obstacles', {})
        
        front_dist = obstacles.get('front', 999)
        left_dist = obstacles.get('left', 999)
        right_dist = obstacles.get('right', 999)
        
        # Simple wall following logic
        if front_dist < self.obstacle_threshold:
            # Wall ahead, turn away from closer side
            if left_dist < right_dist:
                await self.motor_controller.turn_right(self.turn_speed, 0.8)
            else:
                await self.motor_controller.turn_left(self.turn_speed, 0.8)
        elif right_dist < 40:  # Follow right wall
            # Stay close to right wall
            if right_dist < 20:
                # Too close, turn left slightly
                await self.motor_controller.turn_left(self.turn_speed * 0.5, 0.3)
            else:
                # Good distance, move forward
                await self.motor_controller.move_forward(self.max_speed * 0.6, 1.0)
        else:
            # No wall on right, turn right to find wall
            await self.motor_controller.turn_right(self.turn_speed, 0.5)
        
        await asyncio.sleep(0.3)
    
    async def _spiral_exploration(self):
        """Spiral exploration pattern"""
        # Simple spiral: forward, then increasing turn amounts
        forward_time = 2.0
        turn_time = 0.3
        
        await self.motor_controller.move_forward(self.max_speed * 0.6, forward_time)
        await self.motor_controller.turn_right(self.turn_speed, turn_time)
        
        await asyncio.sleep(0.2)
    
    async def _systematic_exploration(self):
        """Systematic grid-like exploration"""
        # Simple back-and-forth pattern
        if len(self.movement_history) % 8 < 4:
            # Move forward phase
            if await self._is_path_safe('front'):
                await self.motor_controller.move_forward(self.max_speed * 0.7, 2.0)
            else:
                await self.motor_controller.turn_right(self.turn_speed, 1.6)  # 90 degree turn
        else:
            # Turn and move to next row
            await self.motor_controller.turn_right(self.turn_speed, 0.8)
        
        await asyncio.sleep(0.3)
    
    async def _need_obstacle_avoidance(self, obstacles: Dict[str, float]) -> bool:
        """Check if obstacle avoidance is needed"""
        for direction, distance in obstacles.items():
            if distance < self.obstacle_threshold:
                return True
        return False
    
    async def _perform_obstacle_avoidance(self, obstacles: Dict[str, float]):
        """Perform obstacle avoidance maneuver"""
        self.state = NavigationState.AVOIDING_OBSTACLE
        self.consecutive_obstacles += 1
        
        front_dist = obstacles.get('front', 999)
        left_dist = obstacles.get('left', 999)
        right_dist = obstacles.get('right', 999)
        
        self.logger.info(f"🚧 Avoiding obstacle: F={front_dist:.1f}, L={left_dist:.1f}, R={right_dist:.1f}")
        
        # Emergency stop if very close
        if any(dist < self.emergency_threshold for dist in obstacles.values()):
            self.logger.warning("🚨 Emergency stop - obstacle too close!")
            await self.motor_controller.emergency_stop()
            await asyncio.sleep(1.0)
        
        # Choose avoidance strategy
        if front_dist < self.obstacle_threshold:
            # Obstacle ahead - turn toward clearer side
            if left_dist > right_dist:
                self.logger.debug("Turning left to avoid obstacle")
                await self.motor_controller.turn_left(self.turn_speed, 1.0)
            else:
                self.logger.debug("Turning right to avoid obstacle")
                await self.motor_controller.turn_right(self.turn_speed, 1.0)
        
        elif left_dist < self.obstacle_threshold:
            # Obstacle on left - turn right
            await self.motor_controller.turn_right(self.turn_speed, 0.8)
        
        elif right_dist < self.obstacle_threshold:
            # Obstacle on right - turn left
            await self.motor_controller.turn_left(self.turn_speed, 0.8)
        
        # Brief pause after avoidance
        await asyncio.sleep(0.5)
        
        self.state = NavigationState.EXPLORING
        self.last_obstacle_time = time.time()
    
    async def _is_path_safe(self, direction: str) -> bool:
        """Check if path is safe in given direction"""
        return self.sensor_manager.is_path_clear(direction, self.obstacle_threshold)
    
    async def _detect_stuck_condition(self) -> bool:
        """Detect if robot is stuck in a loop or can't make progress"""
        # Check if too many consecutive obstacles
        if self.consecutive_obstacles > 10:
            recent_time = time.time() - self.last_obstacle_time
            if recent_time < 30:  # Many obstacles in short time
                return True
        
        # Check movement history for repetitive patterns
        if len(self.movement_history) > 10:
            recent_moves = self.movement_history[-6:]
            if len(set(recent_moves)) <= 2:  # Only 2 or fewer unique moves
                return True
        
        return False
    
    async def _check_for_discoveries(self, mission_data: Dict[str, Any]):
        """Check for new object discoveries during exploration"""
        try:
            # Get current scene analysis
            scene_description = await self.vision_manager.analyze_scene()
            
            if scene_description:
                # Simple object detection based on keywords
                # In a real implementation, this would use proper object detection
                potential_objects = self._extract_objects_from_description(scene_description)
                
                for obj_name in potential_objects:
                    if obj_name not in [obj['name'] for obj in mission_data.get('discovered_objects', [])]:
                        # New discovery
                        discovery = {
                            'name': obj_name,
                            'description': scene_description,
                            'timestamp': time.time(),
                            'location': 'unknown'  # Would track position in real implementation
                        }
                        
                        mission_data.setdefault('discovered_objects', []).append(discovery)
                        self.objects_found.append(discovery)
                        
                        self.logger.info(f"🔍 Discovered object: {obj_name}")
        
        except Exception as e:
            self.logger.error(f"Error checking for discoveries: {e}")
    
    def _extract_objects_from_description(self, description: str) -> List[str]:
        """Extract potential object names from scene description"""
        # Simple keyword-based object extraction
        # In reality, would use NLP or structured object detection
        
        common_objects = [
            'table', 'chair', 'computer', 'monitor', 'keyboard', 'mouse',
            'book', 'paper', 'pen', 'calculator', 'lamp', 'phone',
            'oscilloscope', 'multimeter', 'microscope', 'beaker', 'circuit'
        ]
        
        found_objects = []
        description_lower = description.lower()
        
        for obj in common_objects:
            if obj in description_lower:
                found_objects.append(obj)
        
        return found_objects
    
    async def _update_position_estimate(self, direction: str, duration: float):
        """Update estimated position based on movement"""
        # Simple dead reckoning - in reality would use odometry/SLAM
        current_time = time.time()
        
        # Estimate distance moved (very rough)
        if direction == 'forward':
            estimated_distance = self.max_speed * duration * 0.5  # meters
            self.total_distance_traveled += estimated_distance
        elif direction == 'backward':
            estimated_distance = -self.max_speed * duration * 0.5
            self.total_distance_traveled += abs(estimated_distance)
        
        # Add to position history (placeholder coordinates)
        estimated_x = len(self.position_history) * 0.1
        estimated_y = random.uniform(-0.5, 0.5)
        
        self.position_history.append((estimated_x, estimated_y, current_time))
        
        # Limit history size
        if len(self.position_history) > 1000:
            self.position_history = self.position_history[-500:]
    
    async def navigate_to_object(self, object_name: str, timeout: float = 60.0) -> bool:
        """
        Navigate toward a specific object
        
        Args:
            object_name: Name of object to find
            timeout: Maximum search time
        
        Returns:
            True if object was reached, False if not found/timeout
        """
        start_time = time.time()
        self.state = NavigationState.SEEKING_TARGET
        
        self.logger.info(f"🎯 Navigating to object: {object_name}")
        
        while time.time() - start_time < timeout:
            try:
                # Look for the object
                detected_object = await self.vision_manager.find_object(object_name)
                
                if detected_object:
                    # Object found - move toward it
                    success = await self._approach_object(detected_object)
                    if success:
                        self.logger.info(f"✅ Successfully reached {object_name}")
                        return True
                else:
                    # Object not visible - explore to find it
                    await self._search_for_object()
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"Error during object navigation: {e}")
                break
        
        self.logger.warning(f"❌ Failed to find/reach {object_name} within {timeout}s")
        return False
    
    async def _approach_object(self, detected_object: Dict[str, Any]) -> bool:
        """Approach a detected object"""
        # Simple approach behavior
        # In reality, would use object position and size for better navigation
        
        # Move forward slowly toward object
        if await self._is_path_safe('front'):
            await self.motor_controller.move_forward(self.max_speed * 0.3, 1.0)
            return True
        else:
            # Obstacle in way - try to go around
            await self.motor_controller.turn_left(self.turn_speed, 0.5)
            return False
    
    async def _search_for_object(self):
        """Search behavior when object is not visible"""
        # Simple search pattern - turn and look
        await self.motor_controller.turn_right(self.turn_speed * 0.5, 0.8)
        await asyncio.sleep(0.3)
    
    def get_navigation_status(self) -> Dict[str, Any]:
        """Get current navigation status"""
        return {
            'state': self.state.value,
            'current_goal': self.current_goal.__dict__ if self.current_goal else None,
            'total_distance_traveled': self.total_distance_traveled,
            'objects_found': len(self.objects_found),
            'movement_history_length': len(self.movement_history),
            'consecutive_obstacles': self.consecutive_obstacles,
            'exploration_pattern': self.current_exploration_pattern,
            'position_history_length': len(self.position_history)
        }
    
    def set_exploration_pattern(self, pattern: str):
        """Set exploration behavior pattern"""
        if pattern in self.exploration_patterns:
            self.current_exploration_pattern = pattern
            self.logger.info(f"🔄 Exploration pattern changed to: {pattern}")
        else:
            self.logger.warning(f"Unknown exploration pattern: {pattern}")
    
    def reset_navigation_state(self):
        """Reset navigation state and history"""
        self.state = NavigationState.IDLE
        self.current_goal = None
        self.movement_history.clear()
        self.position_history.clear()
        self.objects_found.clear()
        self.total_distance_traveled = 0.0
        self.consecutive_obstacles = 0
        
        self.logger.info("🧹 Navigation state reset")
    
    async def emergency_stop_navigation(self):
        """Emergency stop all navigation"""
        self.state = NavigationState.IDLE
        self.current_goal = None
        await self.motor_controller.emergency_stop()
        
        self.logger.warning("🚨 Navigation emergency stop activated")
