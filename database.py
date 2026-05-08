"""
Database Management for Kahoot AI Helper
Stores game results, user statistics, and quiz data
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class Database:
    """Database manager for local storage"""
    
    def __init__(self, db_dir: Path):
        """Initialize database"""
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        self.games_file = self.db_dir / "games.json"
        self.stats_file = self.db_dir / "stats.json"
        self.quizzes_file = self.db_dir / "quizzes.json"
    
    def create_tables(self):
        """Initialize database files"""
        self.logger.info("Initializing database files...")
        
        for file in [self.games_file, self.stats_file, self.quizzes_file]:
            if not file.exists():
                file.write_text(json.dumps([], indent=2))
        
        self.logger.info("✅ Database files ready")
    
    def save_game_result(self, result: Dict[str, Any]) -> bool:
        """Save game result"""
        try:
            games = json.loads(self.games_file.read_text())
            result['id'] = len(games) + 1
            result['timestamp'] = datetime.now().isoformat()
            games.append(result)
            self.games_file.write_text(json.dumps(games, indent=2))
            self.logger.info(f"Game result saved: {result.get('score')}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            games = json.loads(self.games_file.read_text())
            
            if not games:
                return {
                    'total_games': 0,
                    'avg_score': 0,
                    'highest_score': 0,
                    'win_rate': 0
                }
            
            scores = [g.get('score', 0) for g in games]
            
            return {
                'total_games': len(games),
                'avg_score': int(sum(scores) / len(scores)) if scores else 0,
                'highest_score': max(scores) if scores else 0,
                'win_rate': 75  # Placeholder
            }
        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}
    
    def get_available_subjects(self) -> List[str]:
        """Get available quiz subjects"""
        return [
            'Science',
            'Mathematics',
            'History',
            'Geography',
            'Literature',
            'Technology'
        ]
    
    def get_challenge_questions(self, subject: str) -> List[Dict]:
        """Get challenge mode questions"""
        # Simulated questions
        return [
            {
                'text': f'Question 1 from {subject}?',
                'options': ['Answer 1', 'Answer 2', 'Answer 3', 'Answer 4'],
                'correct': 'Answer 1',
                'type': 'multiple_choice'
            },
            {
                'text': f'Question 2 from {subject}?',
                'options': ['Answer A', 'Answer B', 'Answer C', 'Answer D'],
                'correct': 'Answer B',
                'type': 'multiple_choice'
            }
        ]
    
    def get_game_history(self, limit: int = 10) -> List[Dict]:
        """Get recent game history"""
        try:
            games = json.loads(self.games_file.read_text())
            return games[-limit:]
        except Exception as e:
            self.logger.error(f"Error getting history: {e}")
            return []


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    db = Database(Path("database"))
    db.create_tables()
    print("✅ Database initialized!")
