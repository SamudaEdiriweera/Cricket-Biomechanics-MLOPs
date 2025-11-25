import argparse
from src.services.processors.file_service import VideoProcessor

def main():
    parser = argparse.ArgumentParser(description="Cricket Biomechanics Analyzer")
    parser.add_argument("--input", type=str, required=True, help="Path to input video")
    parser.add_argument("--output", type=str, default="output.mp4", help="Path to output video")
    
    args = parser.parse_args()
    
    processor = VideoProcessor()
    processor.process_video(args.input, args.output) 
    
if __name__ == "__main__":
    main()   