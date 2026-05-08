"""
Main Application Class for Kahoot AI Helper
Orchestrates all components and manages user interface
"""

import logging
from typing import Optional
from datetime import datetime

from config import Config
from database import Database
from ai_assistant import AIAssistant
from game_handler import GameHandler


class KahootAIHelperApp:
    """Main application class"""
    
    def __init__(self, config: Config):
        """Initialize application"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.db = None
        self.ai = None
        self.game_handler = None
        self.running = False
    
    def setup_database(self):
        """Initialize database"""
        self.logger.info("Initializing database...")
        self.db = Database(self.config.db_dir)
        self.db.create_tables()
        self.logger.info("✅ Database initialized")
    
    def setup_components(self):
        """Setup application components"""
        self.logger.info("Setting up components...")
        
        # Initialize AI Assistant
        self.ai = AIAssistant(self.config)
        self.logger.info("✅ AI Assistant loaded")
        
        # Initialize Game Handler
        self.game_handler = GameHandler(self.db, self.ai, self.config)
        self.logger.info("✅ Game Handler ready")
    
    def display_main_menu(self):
        """Display main menu"""
        menu = """
╔════════════════════════════════════════╗
║   🎮 KAHOOT AI HELPER v2.5.0           ║
║                                        ║
║   1. 🎯 Live Game Mode                 ║
║   2. 📚 Challenge Mode                 ║
║   3. 📖 Study Mode                     ║
║   4. 📊 View Statistics                ║
║   5. ⚙️  Settings                      ║
║   6. 📖 Help & Guide                   ║
║   7. 🚪 Exit                           ║
║                                        ║
║   Join Community:                      ║
║   🔗 Discord: discord.gg/kahootalhelper║
║                                        ║
╚════════════════════════════════════════╝
"""
        print(menu)
    
    def handle_live_game(self):
        """Handle live game mode"""
        try:
            print("\n🎮 LIVE GAME MODE")
            print("-" * 40)
            game_pin = input("Enter Game PIN: ").strip()
            
            if not game_pin:
                print("❌ PIN required")
                return
            
            print(f"🔄 Connecting to game {game_pin}...")
            success = self.game_handler.join_game(game_pin)
            
            if success:
                print("✅ Connected successfully!")
                print("📊 Waiting for questions...")
                
                # Game loop
                while True:
                    question = self.game_handler.get_current_question()
                    
                    if not question:
                        print("⏳ Waiting for question...")
                        continue
                    
                    print(f"\n❓ {question['text']}")
                    print(f"⏱️  Time: {question.get('time', 'N/A')} seconds\n")
                    
                    # Get AI answer
                    answer = self.ai.analyze_question(question)
                    confidence = answer.get('confidence', 0)
                    
                    print(f"🤖 AI Answer: {answer['answer']}")
                    print(f"📊 Confidence: {confidence}%\n")
                    
                    # Ask if continue
                    cont = input("Continue? (y/n): ").lower()
                    if cont != 'y':
                        break
                
                print("\n✅ Game ended!")
                score = self.game_handler.get_final_score()
                print(f"🏆 Final Score: {score}")
                
                # Save to database
                self.db.save_game_result({
                    'mode': 'live_game',
                    'pin': game_pin,
                    'score': score,
                    'timestamp': datetime.now()
                })
            else:
                print("❌ Could not connect to game")
        
        except Exception as e:
            self.logger.error(f"Error in live game: {e}")
            print(f"❌ Error: {e}")
    
    def handle_challenge_mode(self):
        """Handle challenge mode"""
        try:
            print("\n📚 CHALLENGE MODE")
            print("-" * 40)
            
            subjects = self.db.get_available_subjects()
            print("\nAvailable Subjects:")
            for i, subject in enumerate(subjects, 1):
                print(f"{i}. {subject}")
            
            choice = input("\nSelect subject: ").strip()
            
            if not choice.isdigit():
                print("❌ Invalid choice")
                return
            
            subject = subjects[int(choice) - 1]
            questions = self.db.get_challenge_questions(subject)
            
            if not questions:
                print(f"❌ No questions found for {subject}")
                return
            
            print(f"\n📖 {subject} Challenge")
            print(f"📊 Total Questions: {len(questions)}\n")
            
            score = 0
            for i, question in enumerate(questions, 1):
                print(f"\n[{i}/{len(questions)}] {question['text']}\n")
                
                options = question['options']
                for j, option in enumerate(options, 1):
                    print(f"{j}. {option}")
                
                # Get AI answer
                answer = self.ai.analyze_question(question)
                print(f"\n💡 AI Suggestion: {answer['answer']}")
                
                user_answer = input("\nYour answer: ").strip()
                
                if user_answer == answer['answer']:
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Wrong! Correct answer: {answer['answer']}")
            
            print(f"\n🏆 Final Score: {score}/{len(questions)}")
            percentage = (score / len(questions)) * 100
            print(f"📊 Accuracy: {percentage:.1f}%")
            
            # Save to database
            self.db.save_game_result({
                'mode': 'challenge',
                'subject': subject,
                'score': score,
                'total': len(questions),
                'timestamp': datetime.now()
            })
        
        except Exception as e:
            self.logger.error(f"Error in challenge mode: {e}")
            print(f"❌ Error: {e}")
    
    def handle_study_mode(self):
        """Handle study mode"""
        print("\n📖 STUDY MODE")
        print("-" * 40)
        print("🔍 Browse and learn from Kahoot quizzes")
        print("💡 Understand correct answers")
        print("📊 Build your knowledge")
        print("\n✨ Feature coming soon!")
    
    def display_statistics(self):
        """Display user statistics"""
        try:
            stats = self.db.get_user_statistics()
            
            print("\n📊 YOUR STATISTICS")
            print("=" * 40)
            print(f"Total Games Played: {stats['total_games']}")
            print(f"Average Score: {stats['avg_score']}")
            print(f"Highest Score: {stats['highest_score']}")
            print(f"Win Rate: {stats['win_rate']}%")
            print("=" * 40)
        
        except Exception as e:
            self.logger.error(f"Error displaying stats: {e}")
            print(f"❌ Could not load statistics")
    
    def display_settings(self):
        """Display settings menu"""
        settings_menu = f"""
⚙️  SETTINGS

Theme: {self.config.theme}
Language: {self.config.language}
AI Model: {self.config.ai_model}
Auto-Answer: {'On' if self.config.auto_answer else 'Off'}
Show Confidence: {'On' if self.config.show_confidence else 'Off'}

Coming soon: Customize these settings!
"""
        print(settings_menu)
    
    def run(self):
        """Run main application loop"""
        self.running = True
        self.setup_components()
        
        while self.running:
            try:
                self.display_main_menu()
                choice = input("Select option (1-7): ").strip()
                
                if choice == '1':
                    self.handle_live_game()
                elif choice == '2':
                    self.handle_challenge_mode()
                elif choice == '3':
                    self.handle_study_mode()
                elif choice == '4':
                    self.display_statistics()
                elif choice == '5':
                    self.display_settings()
                elif choice == '6':
                    print("\n📖 Help & Guide - Visit: https://github.com/nooncheetahstart/Kahoot-tools-AI")
                elif choice == '7':
                    print("\n👋 Thank you for using Kahoot AI Helper!")
                    self.running = False
                else:
                    print("❌ Invalid option")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                print(f"❌ Error: {e}")


if __name__ == '__main__':
    from config import setup_logging, Config
    setup_logging()
    config = Config()
    app = KahootAIHelperApp(config)
    app.setup_database()
    app.run()
