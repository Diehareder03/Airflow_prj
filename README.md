

# 📘 Airflow Data Pipeline Setup Guide

This repository contains an Apache Airflow-based data pipeline that fetches book data from APIs and loads it into PostgreSQL.

---

## 🚀 Prerequisites
Before you begin, ensure that you have:
- **Docker** and **Docker Compose** installed.
- **Git** installed on your machine.

---

## 📥 Clone the Repository
Run the following command to clone the repository:
```sh
 git clone https://github.com/Diehareder03/Airflow_prj.git
```
Navigate into the project directory:
```sh
cd Airflow_prj
```

---

## 🛠️ Install Docker (If Not Installed)
If Docker is not installed on your system, follow these steps:

```sh
# Update package lists
sudo apt update

# Install required dependencies
sudo apt install -y ca-certificates curl gnupg

# Add Docker’s official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
echo \  
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \  
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package lists again
sudo apt update

# Install Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Start Docker in another terminal:
```sh
sudo dockerd
```

---

## 🔧 Start the Airflow Pipeline
Once inside the project directory, run the following command to start the services:
```sh
docker compose up -d --build
```

### 🛑 Fixing Conflicts (If Needed)
If you have existing containers with the same name, remove them first:
```sh
docker stop postgres && docker rm postgres
docker stop airflow-webserver && docker rm airflow-webserver
docker stop airflow-scheduler && docker rm airflow-scheduler
```
Verify that all Airflow containers are removed:
```sh
docker ps -a
```
If you see any remaining containers, remove them using:
```sh
docker rm <container_id>
```

Clean up the Docker system (optional but recommended):
```sh
docker system prune -a
```
Then restart Docker and re-run:
```sh
docker compose up -d --build
```

---

## 🌍 Accessing the Airflow Web UI
Once the services are running, open your browser and go to:
👉 **http://localhost:8080**

### 📌 If the UI Doesn't Open:
1️⃣ Check if Docker is running properly:
```sh
docker ps
```
2️⃣ Check the logs for errors:
```sh
docker logs airflow-webserver
```
3️⃣ Restart Airflow services:
```sh
docker compose restart airflow-webserver
```

If issues persist, stop all Airflow containers:
```sh
docker compose down -v
```
Then rebuild and start them again:
```sh
docker compose up -d --build
```

---

## ✅ Data Validation & DAG Execution
To trigger the data validation DAG, run:
```sh
docker-compose exec airflow-webserver airflow dags trigger data_quality_check
```

---

## 🛑 Stopping the Pipeline
To stop all running services, run:
```sh
docker compose down
```

To remove all unused containers, images, and volumes:
```sh
docker system prune -a
```

---

## 💡 Troubleshooting
If you face any issues, check the logs:
```sh
docker logs airflow-webserver -f
```
If needed, restart the services:
```sh
docker compose restart
```

---

## 🎯 Conclusion
You have successfully set up an Airflow-based data pipeline! 🎉 If you encounter any issues, refer to this guide or troubleshoot using the provided commands.

Happy coding! 🚀

