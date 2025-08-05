"""
Mission logger for Sarus robot

Handles logging of exploration missions, activities, and generates
reports for robot operations and discoveries.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from ..config.settings import LOGS_DIR, SYSTEM_CONFIG
from ..utils.logger import get_logger

@dataclass
class MissionRecord:
    """Data structure for mission records"""
    mission_id: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    objective: str = "unknown"
    status: str = "active"  # active, completed, failed, aborted
    discovered_objects: List[Dict[str, Any]] = None
    path_taken: List[str] = None
    obstacles_encountered: List[Dict[str, Any]] = None
    commands_received: List[str] = None
    responses_given: List[str] = None
    sensor_data: Dict[str, Any] = None
    summary: Optional[str] = None
    
    def __post_init__(self):
        if self.discovered_objects is None:
            self.discovered_objects = []
        if self.path_taken is None:
            self.path_taken = []
        if self.obstacles_encountered is None:
            self.obstacles_encountered = []
        if self.commands_received is None:
            self.commands_received = []
        if self.responses_given is None:
            self.responses_given = []
        if self.sensor_data is None:
            self.sensor_data = {}

class MissionLogger:
    """
    Logs robot missions, activities, and generates comprehensive reports
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Configuration
        self.logging_enabled = SYSTEM_CONFIG.get('mission_log_enabled', True)
        
        # Database setup
        self.db_path = LOGS_DIR / "missions.db"
        self.json_backup_dir = LOGS_DIR / "mission_backups"
        
        # Ensure directories exist
        self.json_backup_dir.mkdir(exist_ok=True)
        
        # Current mission tracking
        self.current_mission: Optional[MissionRecord] = None
        
        # Initialize database
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for mission storage"""
        if not self.logging_enabled:
            return
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS missions (
                        mission_id TEXT PRIMARY KEY,
                        start_time REAL NOT NULL,
                        end_time REAL,
                        duration REAL,
                        objective TEXT,
                        status TEXT,
                        discovered_objects_json TEXT,
                        path_taken_json TEXT,
                        obstacles_encountered_json TEXT,
                        commands_received_json TEXT,
                        responses_given_json TEXT,
                        sensor_data_json TEXT,
                        summary TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS mission_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        mission_id TEXT,
                        timestamp REAL,
                        event_type TEXT,
                        event_data_json TEXT,
                        FOREIGN KEY (mission_id) REFERENCES missions (mission_id)
                    )
                """)
                
                conn.commit()
            
            self.logger.info("✅ Mission database initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize mission database: {e}")
            self.logging_enabled = False
    
    def start_mission(self, mission_data: Dict[str, Any]) -> str:
        """
        Start a new mission
        
        Args:
            mission_data: Initial mission information
        
        Returns:
            Mission ID
        """
        mission_id = mission_data.get('id', f"mission_{int(time.time())}")
        
        self.current_mission = MissionRecord(
            mission_id=mission_id,
            start_time=time.time(),
            objective=mission_data.get('objective', 'exploration'),
            status='active'
        )
        
        # Log mission start
        self.log_event('mission_start', {'objective': self.current_mission.objective})
        
        self.logger.info(f"🚀 Mission started: {mission_id}")
        return mission_id
    
    def log_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Log a mission event
        
        Args:
            event_type: Type of event (command, movement, discovery, etc.)
            event_data: Event details
        """
        if not self.logging_enabled or not self.current_mission:
            return
        
        timestamp = time.time()
        
        try:
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO mission_events 
                    (mission_id, timestamp, event_type, event_data_json)
                    VALUES (?, ?, ?, ?)
                """, (
                    self.current_mission.mission_id,
                    timestamp,
                    event_type,
                    json.dumps(event_data)
                ))
                conn.commit()
            
            # Update current mission record based on event type
            self._update_mission_from_event(event_type, event_data)
            
        except Exception as e:
            self.logger.error(f"Failed to log mission event: {e}")
    
    def _update_mission_from_event(self, event_type: str, event_data: Dict[str, Any]):
        """Update current mission record with event data"""
        if not self.current_mission:
            return
        
        if event_type == 'command_received':
            command = event_data.get('command', '')
            self.current_mission.commands_received.append(command)
        
        elif event_type == 'response_given':
            response = event_data.get('response', '')
            self.current_mission.responses_given.append(response)
        
        elif event_type == 'movement':
            direction = event_data.get('direction', 'unknown')
            self.current_mission.path_taken.append(direction)
        
        elif event_type == 'object_discovered':
            obj_data = event_data.copy()
            obj_data['timestamp'] = time.time()
            self.current_mission.discovered_objects.append(obj_data)
        
        elif event_type == 'obstacle_encountered':
            obstacle_data = event_data.copy()
            obstacle_data['timestamp'] = time.time()
            self.current_mission.obstacles_encountered.append(obstacle_data)
        
        elif event_type == 'sensor_reading':
            # Update sensor data with latest readings
            self.current_mission.sensor_data.update(event_data)
    
    def log_command(self, command: str, response: str):
        """Log command and response pair"""
        self.log_event('command_received', {'command': command})
        self.log_event('response_given', {'response': response})
    
    def log_movement(self, direction: str, distance: Optional[float] = None, duration: Optional[float] = None):
        """Log robot movement"""
        movement_data = {'direction': direction}
        if distance is not None:
            movement_data['distance'] = distance
        if duration is not None:
            movement_data['duration'] = duration
        
        self.log_event('movement', movement_data)
    
    def log_discovery(self, object_name: str, confidence: float, location: Optional[str] = None):
        """Log object discovery"""
        discovery_data = {
            'object_name': object_name,
            'confidence': confidence
        }
        if location:
            discovery_data['location'] = location
        
        self.log_event('object_discovered', discovery_data)
    
    def log_obstacle(self, distance: float, direction: str, action_taken: str):
        """Log obstacle encounter"""
        obstacle_data = {
            'distance': distance,
            'direction': direction,
            'action_taken': action_taken
        }
        
        self.log_event('obstacle_encountered', obstacle_data)
    
    def log_sensor_data(self, sensor_readings: Dict[str, Any]):
        """Log sensor readings"""
        self.log_event('sensor_reading', sensor_readings)
    
    def complete_mission(self, mission_data: Dict[str, Any], summary: str):
        """
        Complete current mission
        
        Args:
            mission_data: Final mission data
            summary: Mission summary text
        """
        if not self.current_mission:
            self.logger.warning("No active mission to complete")
            return
        
        # Update mission record
        self.current_mission.end_time = time.time()
        self.current_mission.duration = self.current_mission.end_time - self.current_mission.start_time
        self.current_mission.status = 'completed'
        self.current_mission.summary = summary
        
        # Update with any additional data
        if 'discovered_objects' in mission_data:
            self.current_mission.discovered_objects.extend(mission_data['discovered_objects'])
        
        # Save to database
        self._save_mission_to_database()
        
        # Create backup JSON file
        self._create_mission_backup()
        
        # Log completion
        self.log_event('mission_complete', {
            'duration': self.current_mission.duration,
            'objects_found': len(self.current_mission.discovered_objects),
            'obstacles_encountered': len(self.current_mission.obstacles_encountered),
            'summary': summary
        })
        
        self.logger.info(f"✅ Mission completed: {self.current_mission.mission_id}")
        
        # Clear current mission
        completed_mission_id = self.current_mission.mission_id
        self.current_mission = None
        
        return completed_mission_id
    
    def abort_mission(self, reason: str):
        """Abort current mission"""
        if not self.current_mission:
            return
        
        self.current_mission.end_time = time.time()
        self.current_mission.duration = self.current_mission.end_time - self.current_mission.start_time
        self.current_mission.status = 'aborted'
        self.current_mission.summary = f"Mission aborted: {reason}"
        
        self._save_mission_to_database()
        self.log_event('mission_aborted', {'reason': reason})
        
        self.logger.warning(f"🛑 Mission aborted: {self.current_mission.mission_id} - {reason}")
        self.current_mission = None
    
    def emergency_save(self, mission_data: Dict[str, Any]):
        """Emergency save of mission data during shutdown"""
        if not self.current_mission:
            return
        
        self.current_mission.status = 'interrupted'
        self.current_mission.end_time = time.time()
        self.current_mission.duration = self.current_mission.end_time - self.current_mission.start_time
        
        try:
            self._save_mission_to_database()
            self._create_mission_backup()
            self.logger.info(f"💾 Emergency save completed for mission {self.current_mission.mission_id}")
        except Exception as e:
            self.logger.error(f"Emergency save failed: {e}")
    
    def _save_mission_to_database(self):
        """Save current mission to database"""
        if not self.logging_enabled or not self.current_mission:
            return
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO missions 
                    (mission_id, start_time, end_time, duration, objective, status,
                     discovered_objects_json, path_taken_json, obstacles_encountered_json,
                     commands_received_json, responses_given_json, sensor_data_json, summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.current_mission.mission_id,
                    self.current_mission.start_time,
                    self.current_mission.end_time,
                    self.current_mission.duration,
                    self.current_mission.objective,
                    self.current_mission.status,
                    json.dumps(self.current_mission.discovered_objects),
                    json.dumps(self.current_mission.path_taken),
                    json.dumps(self.current_mission.obstacles_encountered),
                    json.dumps(self.current_mission.commands_received),
                    json.dumps(self.current_mission.responses_given),
                    json.dumps(self.current_mission.sensor_data),
                    self.current_mission.summary
                ))
                conn.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to save mission to database: {e}")
    
    def _create_mission_backup(self):
        """Create JSON backup of mission"""
        if not self.current_mission:
            return
        
        try:
            mission_dict = asdict(self.current_mission)
            
            # Add human-readable timestamps
            mission_dict['start_time_str'] = datetime.fromtimestamp(
                self.current_mission.start_time
            ).isoformat()
            
            if self.current_mission.end_time:
                mission_dict['end_time_str'] = datetime.fromtimestamp(
                    self.current_mission.end_time
                ).isoformat()
            
            # Save to JSON file
            backup_file = self.json_backup_dir / f"{self.current_mission.mission_id}.json"
            with open(backup_file, 'w') as f:
                json.dump(mission_dict, f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Failed to create mission backup: {e}")
    
    def get_mission_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent mission history
        
        Args:
            limit: Maximum number of missions to return
        
        Returns:
            List of mission records
        """
        if not self.logging_enabled:
            return []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM missions 
                    ORDER BY start_time DESC 
                    LIMIT ?
                """, (limit,))
                
                missions = []
                for row in cursor.fetchall():
                    mission = dict(row)
                    
                    # Parse JSON fields
                    for field in ['discovered_objects_json', 'path_taken_json', 
                                'obstacles_encountered_json', 'commands_received_json',
                                'responses_given_json', 'sensor_data_json']:
                        if mission[field]:
                            try:
                                mission[field.replace('_json', '')] = json.loads(mission[field])
                            except json.JSONDecodeError:
                                mission[field.replace('_json', '')] = []
                        del mission[field]
                    
                    missions.append(mission)
                
                return missions
                
        except Exception as e:
            self.logger.error(f"Failed to get mission history: {e}")
            return []
    
    def get_mission_statistics(self) -> Dict[str, Any]:
        """Get mission statistics"""
        if not self.logging_enabled:
            return {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_missions,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_missions,
                        COUNT(CASE WHEN status = 'aborted' THEN 1 END) as aborted_missions,
                        AVG(duration) as avg_duration,
                        MAX(duration) as max_duration,
                        MIN(start_time) as first_mission_time,
                        MAX(start_time) as last_mission_time
                    FROM missions
                """)
                
                stats = dict(cursor.fetchone())
                
                # Calculate success rate
                if stats['total_missions'] > 0:
                    stats['success_rate'] = stats['completed_missions'] / stats['total_missions']
                else:
                    stats['success_rate'] = 0.0
                
                # Add current mission info
                if self.current_mission:
                    stats['current_mission_id'] = self.current_mission.mission_id
                    stats['current_mission_duration'] = time.time() - self.current_mission.start_time
                else:
                    stats['current_mission_id'] = None
                    stats['current_mission_duration'] = 0.0
                
                return stats
                
        except Exception as e:
            self.logger.error(f"Failed to get mission statistics: {e}")
            return {}
    
    def generate_daily_report(self, date: Optional[str] = None) -> str:
        """
        Generate daily mission report
        
        Args:
            date: Date in YYYY-MM-DD format, today if None
        
        Returns:
            Formatted daily report
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get missions for the day
        start_timestamp = datetime.strptime(date, '%Y-%m-%d').timestamp()
        end_timestamp = start_timestamp + 86400  # 24 hours
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM missions 
                    WHERE start_time >= ? AND start_time < ?
                    ORDER BY start_time
                """, (start_timestamp, end_timestamp))
                
                missions = cursor.fetchall()
            
            # Generate report
            report_lines = [
                f"=== Sarus Daily Mission Report - {date} ===",
                f"Total missions: {len(missions)}",
                ""
            ]
            
            if not missions:
                report_lines.append("No missions recorded for this date.")
                return "\n".join(report_lines)
            
            completed = sum(1 for m in missions if m['status'] == 'completed')
            total_duration = sum(m['duration'] or 0 for m in missions)
            
            report_lines.extend([
                f"Completed missions: {completed}",
                f"Success rate: {completed/len(missions):.1%}",
                f"Total active time: {total_duration/3600:.1f} hours",
                f"Average mission duration: {total_duration/len(missions)/60:.1f} minutes",
                "",
                "Mission Details:"
            ])
            
            for mission in missions:
                start_time = datetime.fromtimestamp(mission['start_time']).strftime('%H:%M:%S')
                duration = (mission['duration'] or 0) / 60  # Convert to minutes
                status = mission['status']
                
                report_lines.append(f"  {start_time} - {mission['mission_id']} ({status}, {duration:.1f}m)")
                
                if mission['summary']:
                    report_lines.append(f"    Summary: {mission['summary']}")
                
                # Count discoveries
                try:
                    discoveries = json.loads(mission['discovered_objects_json'] or '[]')
                    if discoveries:
                        report_lines.append(f"    Discovered {len(discoveries)} objects")
                except:
                    pass
            
            return "\n".join(report_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to generate daily report: {e}")
            return f"Failed to generate report for {date}: {e}"
    
    def cleanup_old_missions(self, days_to_keep: int = 30):
        """Clean up old mission records"""
        if not self.logging_enabled:
            return
        
        cutoff_time = time.time() - (days_to_keep * 86400)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Delete old mission events
                cursor = conn.execute("""
                    DELETE FROM mission_events 
                    WHERE mission_id IN (
                        SELECT mission_id FROM missions WHERE start_time < ?
                    )
                """, (cutoff_time,))
                events_deleted = cursor.rowcount
                
                # Delete old missions
                cursor = conn.execute("""
                    DELETE FROM missions WHERE start_time < ?
                """, (cutoff_time,))
                missions_deleted = cursor.rowcount
                
                conn.commit()
            
            self.logger.info(f"🧹 Cleaned up {missions_deleted} old missions and {events_deleted} events")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old missions: {e}")
