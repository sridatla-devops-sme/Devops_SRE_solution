import time
import logging
import sys

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    stream=sys.stdout
)
logger = logging.getLogger("memory-app")

def main():
    logger.info("Application starting...")
    data = []
    
    # Allocate 100MB initially
    try:
        data.append(bytearray(100 * 1024 * 1024))
        logger.info("Allocated initial 100MB")
    except Exception as e:
        logger.error(f"Failed to allocate initial memory: {e}")
        return

    # Increase to 500MB in 2 minutes (120 seconds)
    # Target increase: 400MB
    # Per second increase: 400 / 120 = ~3.33MB/s
    # Let's allocate 3.33MB every second
    mb_increment_float = 400 / 120.0
    total_mb_float = 100.0

    while True:
        try:
            # allocate the increment for this second
            increment_bytes = int(mb_increment_float * 1024 * 1024)
            data.append(bytearray(increment_bytes))
            
            total_mb_float += mb_increment_float
            current_mb = int(total_mb_float)
            
            # Log periodically to avoid excessive spam but keep generating logs
            if current_mb % 25 == 0 or current_mb % 25 < 4: 
                # This simple condition will log roughly every 25MB
                logger.info(f"Health check: OK. Current memory allocated: ~{current_mb}MB")
                
            time.sleep(1)
        except MemoryError:
            logger.error("OOM limits exceeded or MemoryError caught.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

if __name__ == "__main__":
    main()
