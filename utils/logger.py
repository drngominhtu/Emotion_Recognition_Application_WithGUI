"""
Logger utility for emotion recognition sessions
"""
import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Optional

class EmotionLogger:
    """Logger for emotion recognition sessions"""
    
    def __init__(self):
        self.is_logging = False
        self.log_data = []
        self.session_start_time = None
        self.output_folder = "output"
        self.csv_filename = ""
        self.json_filename = ""
        self.summary_filename = ""
        
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
    
    def start_logging(self, session_name: str = None) -> bool:
        """Start logging emotion data"""
        try:
            self.session_start_time = datetime.now()
            
            if not session_name:
                timestamp = self.session_start_time.strftime("%Y%m%d_%H%M%S")
                session_name = f"emotion_session_{timestamp}"
            
            # Create file paths
            self.csv_filename = os.path.join(self.output_folder, f"{session_name}.csv")
            self.json_filename = os.path.join(self.output_folder, f"{session_name}.json")
            self.summary_filename = os.path.join(self.output_folder, f"{session_name}_summary.txt")
            
            # Initialize CSV file with headers
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'time_elapsed', 'emotion', 'confidence', 'model_used', 'face_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            
            # Clear previous data
            self.log_data = []
            self.is_logging = True
            
            print(f"Bắt đầu logging: {session_name}")
            return True
            
        except Exception as e:
            print(f"Lỗi khởi tạo logger: {e}")
            return False
    
    def log_emotion(self, emotion: str, confidence: float, model_name: str, face_count: int = 0):
        """Log emotion detection result"""
        if not self.is_logging:
            return
        
        try:
            current_time = datetime.now()
            time_elapsed = (current_time - self.session_start_time).total_seconds()
            
            # Create log entry
            log_entry = {
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'time_elapsed': round(time_elapsed, 3),
                'emotion': emotion,
                'confidence': round(confidence, 4),
                'model_used': model_name,
                'face_count': face_count
            }
            
            # Add to in-memory data
            self.log_data.append(log_entry)
            
            # Append to CSV file
            with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'time_elapsed', 'emotion', 'confidence', 'model_used', 'face_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(log_entry)
            
        except Exception as e:
            print(f"Lỗi ghi log: {e}")
    
    def stop_logging(self) -> Dict:
        """Stop logging and generate summary"""
        if not self.is_logging:
            return {}
        
        try:
            self.is_logging = False
            session_end_time = datetime.now()
            session_duration = (session_end_time - self.session_start_time).total_seconds()
            
            # Generate summary statistics
            summary = self._generate_summary(session_duration)
            
            # Save JSON data
            session_data = {
                'session_info': {
                    'start_time': self.session_start_time.isoformat(),
                    'end_time': session_end_time.isoformat(),
                    'duration_seconds': session_duration,
                    'total_records': len(self.log_data)
                },
                'summary': summary,
                'data': self.log_data
            }
            
            with open(self.json_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(session_data, jsonfile, indent=2, ensure_ascii=False)
            
            # Save text summary
            self._save_text_summary(summary, session_duration)
            
            print(f"Đã lưu log tại: {self.output_folder}")
            return summary
            
        except Exception as e:
            print(f"Lỗi dừng logger: {e}")
            return {}
    
    def _generate_summary(self, duration: float) -> Dict:
        """Generate session summary statistics"""
        if not self.log_data:
            return {}
        
        emotions = [entry['emotion'] for entry in self.log_data]
        confidences = [entry['confidence'] for entry in self.log_data]
        models = [entry['model_used'] for entry in self.log_data]
        
        # Emotion distribution
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        emotion_percentages = {}
        total_records = len(self.log_data)
        for emotion, count in emotion_counts.items():
            emotion_percentages[emotion] = round((count / total_records) * 100, 2)
        
        # Confidence statistics
        avg_confidence = sum(confidences) / len(confidences)
        max_confidence = max(confidences)
        min_confidence = min(confidences)
        
        # Most common emotion
        most_common_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Model usage
        model_counts = {}
        for model in models:
            model_counts[model] = model_counts.get(model, 0) + 1
        
        return {
            'total_records': total_records,
            'duration_minutes': round(duration / 60, 2),
            'avg_records_per_minute': round(total_records / (duration / 60), 2),
            'emotion_distribution': emotion_counts,
            'emotion_percentages': emotion_percentages,
            'most_common_emotion': most_common_emotion,
            'confidence_stats': {
                'average': round(avg_confidence, 4),
                'maximum': round(max_confidence, 4),
                'minimum': round(min_confidence, 4)
            },
            'model_usage': model_counts
        }
    
    def _save_text_summary(self, summary: Dict, duration: float):
        """Save human-readable summary to text file"""
        try:
            with open(self.summary_filename, 'w', encoding='utf-8') as f:
                f.write("EMOTION RECOGNITION SESSION SUMMARY\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Thời gian phiên: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Thời lượng: {summary.get('duration_minutes', 0):.2f} phút\n")
                f.write(f"Tổng số bản ghi: {summary.get('total_records', 0)}\n")
                f.write(f"Tần suất ghi: {summary.get('avg_records_per_minute', 0):.2f} bản ghi/phút\n\n")
                
                f.write("PHÂN PHỐI CẢM XÚC:\n")
                f.write("-" * 30 + "\n")
                emotion_percentages = summary.get('emotion_percentages', {})
                for emotion, percentage in sorted(emotion_percentages.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{emotion:15}: {percentage:6.2f}%\n")
                
                f.write(f"\nCảm xúc phổ biến nhất: {summary.get('most_common_emotion', 'N/A')}\n\n")
                
                f.write("THỐNG KÊ ĐỘ TIN CẬY:\n")
                f.write("-" * 30 + "\n")
                confidence_stats = summary.get('confidence_stats', {})
                f.write(f"Trung bình: {confidence_stats.get('average', 0):.4f}\n")
                f.write(f"Cao nhất:   {confidence_stats.get('maximum', 0):.4f}\n")
                f.write(f"Thấp nhất:  {confidence_stats.get('minimum', 0):.4f}\n\n")
                
                f.write("SỬ DỤNG MODEL:\n")
                f.write("-" * 30 + "\n")
                model_usage = summary.get('model_usage', {})
                for model, count in model_usage.items():
                    f.write(f"{model}: {count} lần\n")
                
                f.write(f"\n\nFiles được tạo:\n")
                f.write(f"- CSV data: {os.path.basename(self.csv_filename)}\n")
                f.write(f"- JSON data: {os.path.basename(self.json_filename)}\n")
                f.write(f"- Summary: {os.path.basename(self.summary_filename)}\n")
                
        except Exception as e:
            print(f"Lỗi lưu text summary: {e}")
    
    def get_current_session_info(self) -> Dict:
        """Get current session information"""
        if not self.is_logging:
            return {}
        
        current_time = datetime.now()
        duration = (current_time - self.session_start_time).total_seconds()
        
        return {
            'is_active': self.is_logging,
            'start_time': self.session_start_time.strftime('%H:%M:%S'),
            'duration_seconds': duration,
            'duration_formatted': f"{int(duration//60):02d}:{int(duration%60):02d}",
            'records_count': len(self.log_data),
            'output_folder': self.output_folder
        }
    
    def is_active(self) -> bool:
        """Check if logging is currently active"""
        return self.is_logging
