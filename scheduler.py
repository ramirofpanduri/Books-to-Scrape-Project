from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess


def run_main():
    subprocess.run(["python", "main.py"], check=True)


scheduler = BlockingScheduler()
scheduler.add_job(run_main, 'interval', hours=12)

if __name__ == "__main__":
    print("Scheduler started. It will run every 10 hours.")
    scheduler.start()
